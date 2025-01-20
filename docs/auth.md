# Django Authentication System Documentation

By Paul Lilian (info@paullilian.dev)

## Environment Setup

Security is crucial for our application, so we'll need to set up our environment variables carefully. Create a `.env` file in your project root with the following structure. Remember to replace the placeholder values with your actual configuration:

```env
# Django Settings
SECRET_KEY=your_django_secret_key

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Cloudflare R2 Storage
CLOUDFLARE_R2_ACCESS_KEY_ID=your_r2_access_key
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_r2_secret_key
CLOUDFLARE_R2_BUCKET_NAME=your_bucket_name
CLOUDFLARE_R2_ENDPOINT_URL=your_r2_endpoint_url
CLOUDFLARE_R2_REGION=your_r2_region

# Email Settings
EMAIL_HOST=your_email_host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_COMMERCE_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_default_sender
SERVER_EMAIL=your_server_email

# Google OAuth2
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# API Documentation
SPECTACULAR_TITLE=Your_API_Title
```

## Project Features

I've built this system with a few key features that work together seamlessly:

The authentication system is built on Django's robust foundation but extends it with modern features needed for a React-based frontend application. It uses JWT (JSON Web Tokens) for authentication, which is perfect for React applications because it's stateless and can handle multiple clients efficiently.

The email-based user management system moves away from traditional username-based authentication, providing a more modern user experience. When users register, they receive a verification email that helps maintain the quality of our user base and reduces spam accounts.

For file handling, I've integrated Cloudflare R2 storage, which provides a cost-effective and reliable solution for handling user uploads like profile pictures. This integration ensures our application remains scalable and performant even as our user base grows.

## React Integration Guide

Let's walk through integrating this backend with your React application. I'll explain each part in detail.

### 1. Setting Up Google Login

Here's how to implement Google authentication in your React application:

```jsx
import { useEffect } from "react";

const GoogleLogin = () => {
  useEffect(() => {
    // Load Google's script
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const handleCredentialResponse = async (response) => {
    try {
      const res = await fetch("http://localhost:8000/auth/google/onetap/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id_token: response.credential,
        }),
      });

      const data = await res.json();

      // Store the JWT tokens securely
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
    } catch (error) {
      console.error("Google login failed:", error);
    }
  };

  return (
    <div
      id="g_id_onload"
      data-client_id={process.env.REACT_APP_GOOGLE_CLIENT_ID}
      data-context="signup"
      data-ux_mode="popup"
      data-callback="handleCredentialResponse"
      data-auto_prompt="false"
    />
  );
};

export default GoogleLogin;
```

### 2. API Integration

Creating a service for handling authentication in your React app:

```javascript
// services/auth.js

class AuthService {
  constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";
  }

  async login(email, password) {
    const response = await fetch(`${this.apiUrl}/auth/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();
    this.setTokens(data);
    return data;
  }

  async register(userData) {
    const response = await fetch(`${this.apiUrl}/auth/registration/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || "Registration failed");
    }

    return response.json();
  }

  async refreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    if (!refresh_token) {
      throw new Error("No refresh token available");
    }

    const response = await fetch(`${this.apiUrl}/auth/token/refresh/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refresh_token }),
    });

    if (!response.ok) {
      throw new Error("Token refresh failed");
    }

    const data = await response.json();
    this.setTokens(data);
    return data;
  }

  setTokens(data) {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
  }

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }
}

export const authService = new AuthService();
```

### 3. Protected Routes Setup

Here's a robust implementation of protected routes in React:

```jsx
// components/PrivateRoute.jsx
import { Navigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { authService } from "../services/auth";

const PrivateRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const validateToken = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          setIsAuthenticated(false);
          setIsLoading(false);
          return;
        }

        // Verify token validity here
        await authService.verifyToken();
        setIsAuthenticated(true);
      } catch (error) {
        // Token is invalid or expired
        try {
          await authService.refreshToken();
          setIsAuthenticated(true);
        } catch (refreshError) {
          setIsAuthenticated(false);
        }
      } finally {
        setIsLoading(false);
      }
    };

    validateToken();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>; // Or your loading component
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default PrivateRoute;
```

## API Endpoints

Your React application can interact with these endpoints:

```javascript
// Authentication
`${API_URL}/auth/registration/` // Register new user
`${API_URL}/auth/login/` // Login with email/password
`${API_URL}/auth/google/` // Standard Google OAuth2
`${API_URL}/auth/google/onetap/` // Google One Tap
`${API_URL}/auth/token/refresh/` // Get new access token
`${API_URL}/auth/user/`// Password Management // Get current user info
`${API_URL}/auth/password/reset/` // Request password reset
`${API_URL}/auth/password/reset/confirm/`// User Management // Confirm password reset
`${API_URL}/auth/user/` // Update user profile
`${API_URL}/auth/user/avatar/`; // Upload user avatar
```

## File Storage with Cloudflare R2

When implementing file uploads in your React application, here's a secure approach:

```javascript
async function uploadFile(file, type = "avatar") {
  const formData = new FormData();
  formData.append(type, file);

  try {
    const response = await fetch(`${API_URL}/auth/user/${type}/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    return await response.json();
  } catch (error) {
    console.error("File upload error:", error);
    throw error;
  }
}
```

## Production Considerations

Before deploying to production, make sure to:

1. Set up proper environment variables for both your Django backend and React frontend
2. Enable HTTPS for all communications
3. Update CORS settings to allow only your production domains
4. Configure proper error logging and monitoring
5. Set up proper backup systems for your database and file storage
6. Implement rate limiting on your authentication endpoints
7. Set up proper CSP (Content Security Policy) headers

## Need Help?

If you run into any issues:

1. Check the API documentation at `/api/docs/`
2. Test the Google authentication flow at `/test/google/`
3. Contact me at info@paullilian.dev

Remember to handle errors gracefully in your React application and provide good feedback to users when authentication-related actions fail.
