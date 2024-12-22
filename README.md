# E-commerce-Website

1. **User Registration & Authentication**:
   - Created an API for user registration, with password validation (rejecting weak passwords).
   - Implemented JWT authentication for secure login and token issuance.

2. **Product Management API**:
   - Developed APIs for CRUD operations on products (name, price,)
   - Secured the product API using JWT tokens, ensuring only authorized users can modify data.

3. **JWT Authentication**:
   - Integrated `rest_framework_simplejwt` for issuing and validating tokens.
   - **Test**: Ensured that JWT tokens are required for accessing secured endpoints.

4. **Testing & Debugging**:
   - Automated tests were written for both user registration and product management APIs.
  
5. **Caching**:

  - Used Django's built-in caching mechanism to cache product lists and details, reducing database load for frequently 
  accessed resources.
