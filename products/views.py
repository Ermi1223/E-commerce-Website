import logging
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, UserSerializer
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


logger = logging.getLogger(__name__)

# Registration View
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    try:
        username = request.data['username']
        password = request.data['password']
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'message': 'User already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login View (JWT Generation)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Get username and password from the request body
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user:
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })
    return Response({'detail': 'Invalid credentials'}, status=400)


# Fetch current authenticated user's details
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    try:
        # Log the headers for debugging
        logger.debug(f"Request Headers: {request.headers}")
        
        # Ensure the token is extracted from the request
        auth_header = request.headers.get('Authorization')
        if auth_header:
            logger.debug(f"Authorization Header: {auth_header}")
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching current user: {str(e)}")
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Update User View
@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        # Ensure that the user is trying to update their own information
        if request.user.id != user_id:
            return Response({'message': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except User.DoesNotExist:
        return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Delete User View
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        # Ensure that the user is trying to delete their own account
        if request.user.id != user_id:
            return Response({'message': 'You can only delete your own profile.'}, status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    except User.DoesNotExist:
        return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Product CRUD Operations

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Product created successfully!', 'product_id': product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])  # Add JWT Authentication
@permission_classes([AllowAny])
def get_products(request):
    page = request.GET.get('page', 1)
    products = cache.get(f'products_page_{page}')

    if not products:
        products = Product.objects.all()
        cache.set(f'products_page_{page}', products, timeout=300)

    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product(request, product_id):
    product = cache.get(f'product_{product_id}')
    if not product:
        try:
            product = Product.objects.get(id=product_id)
            cache.set(f'product_{product_id}', product, timeout=300)
        except ObjectDoesNotExist:
            return Response({'message': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except ObjectDoesNotExist:
        return Response({'message': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({'message': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
