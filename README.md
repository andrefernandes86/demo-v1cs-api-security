# Vulnerable API

This is a deliberately vulnerable API designed for educational purposes to simulate common security flaws such as SQL Injection, insecure authentication, and XSS.

## Features
- User registration and login
- CRUD operations for posts
- Common security vulnerabilities for testing

## Deployment Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd vulnerable-api
   ```

2. **Install Dependencies Locally**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the Application Locally**:
   ```bash
   python3 app.py
   ```
   - Use `http://127.0.0.1:5000` to test endpoints.

4. **Package the Application for Lambda**:
   ```bash
   mkdir package
   pip install -r requirements.txt -t ./package
   cp app.py ./package
   cd package
   zip -r ../api.zip .
   ```

5. **Deploy on AWS**:
   - Create a Lambda function and upload `api.zip`.
   - Set the handler to `app.lambda_handler`.
   - Use API Gateway to create REST API endpoints and integrate them with Lambda.

6. **Test Your API Gateway**:
   Use the stage URL provided by API Gateway to test your endpoints.
