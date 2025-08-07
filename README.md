# Finora - AI-Powered Pricing Intelligence Platform

A complete Flask web application with SQLite database integration for Finora, featuring user authentication, demo requests, dashboard functionality, and a modern responsive design.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or download the project files**
2. **Install Flask** (if not already installed):
   \`\`\`bash
   pip install flask
   \`\`\`

3. **Run the application**:
   \`\`\`bash
   python app.py
   \`\`\`

4. **Open your browser** and navigate to:
   - **Home Page**: http://localhost:5000/
   - **Demo Request**: http://localhost:5000/demo
   - **Login**: http://localhost:5000/login
   - **Sign Up**: http://localhost:5000/signup
   - **Dashboard**: http://localhost:5000/dashboard (requires login)

## 📁 Project Structure

\`\`\`
finora-website/
├── app.py                 # Main Flask application
├── finora.db             # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── base.html         # Base template with header/navigation
│   ├── home.html         # Landing page
│   ├── demo.html         # Demo request form
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   ├── dashboard.html    # User dashboard
│   ├── admin_users.html  # Admin user management
│   ├── admin_demo_requests.html # Admin demo requests
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/               # Static assets
│   ├── css/
│   │   └── styles.css    # Complete CSS styling
│   └── js/
│       ├── base.js       # Base functionality
│       ├── demo.js       # Demo form handling
│       ├── auth.js       # Authentication logic
│       ├── home.js       # Home page interactions
│       └── dashboard.js  # Dashboard functionality
└── README.md             # This file
\`\`\`

## 🗄️ Database Schema

### Users Table
\`\`\`sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    company TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    newsletter BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT 0
);
\`\`\`

### Demo Requests Table
\`\`\`sql
CREATE TABLE demo_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    company_size TEXT NOT NULL,
    industry TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\`\`\`

### User Sessions Table
\`\`\`sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
\`\`\`

## 🌟 Features

### 🏠 **Home Page** (`/`)
- Hero section with animated statistics
- Features showcase
- Call-to-action sections
- Responsive design with smooth scrolling

### 📋 **Demo Request** (`/demo`)
- Comprehensive demo request form
- Real-time form validation
- Success modal with confirmation
- Data saved to SQLite database

### 🔐 **Authentication System**
- **Sign Up** (`/signup`) - User registration with password hashing
- **Login** (`/login`) - User authentication with session management
- **Logout** - Secure session termination
- **Auto-redirect** - Logged-in users redirected to dashboard
- **Password Security** - SHA-256 password hashing
- **Session Management** - Secure user sessions

### 📊 **Dashboard** (`/dashboard`)
- **Protected Route** - Requires user authentication
- **User Statistics** - Personalized metrics and data
- **Animated Counters** - Interactive data visualization
- **Quick Actions** - Easy access to key features
- **User Profile** - Display user information

### 👨‍💼 **Admin Panel** (Development Mode)
- **User Management** (`/admin/users`) - View all registered users
- **Demo Requests** (`/admin/demo-requests`) - View all demo submissions
- **Statistics Dashboard** - User and request analytics
- **Only available in debug mode**

### 🛠 **Backend Features**
- **SQLite Database** - Persistent data storage
- **Password Hashing** - Secure SHA-256 password encryption
- **Session Management** - Flask session-based authentication
- **Form Validation** - Server-side input validation
- **Error Handling** - Custom 404 and 500 error pages
- **API Endpoints** - RESTful API for frontend communication

## 🔧 API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /demo` - Demo request page
- `GET /login` - Login page
- `GET /signup` - Sign up page

### Authentication Endpoints
- `POST /api/login` - User authentication
- `POST /api/signup` - User registration
- `POST /api/logout` - User logout

### Protected Endpoints (Require Login)
- `GET /dashboard` - User dashboard
- `GET /api/user-stats` - Dashboard statistics
- `GET /api/user-profile` - User profile data

### Form Endpoints
- `POST /api/demo-request` - Submit demo request

### Admin Endpoints (Debug Mode Only)
- `GET /admin/users` - View all users
- `GET /admin/demo-requests` - View all demo requests

## 💻 Usage Examples

### Running the Application
\`\`\`bash
# Start the Flask development server
python app.py

# The server will start on http://localhost:5000
# Database will be automatically created as finora.db
# Press Ctrl+C to stop the server
\`\`\`

### User Registration Flow
1. Navigate to http://localhost:5000/signup
2. Fill out the registration form
3. Password is automatically hashed and stored
4. User is redirected to login page
5. After login, user is redirected to dashboard

### Testing Authentication
1. **Sign Up**: Create a new account
2. **Login**: Use your credentials to log in
3. **Dashboard**: Automatically redirected after successful login
4. **Logout**: Click logout to end session
5. **Protection**: Try accessing `/dashboard` without login (redirected to login)

### Admin Panel Access
1. Ensure the app is running in debug mode
2. Navigate to http://localhost:5000/admin/users
3. View all registered users and their information
4. Navigate to http://localhost:5000/admin/demo-requests
5. View all demo requests with detailed information

## 🔒 Security Features

- **Password Hashing**: SHA-256 encryption for all passwords
- **Session Security**: Flask session-based authentication
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Server-side form validation
- **Route Protection**: Authentication required for sensitive pages
- **Error Handling**: Secure error pages without sensitive information

## 🎨 Design Features

- **Modern Dark Theme** with gradient backgrounds
- **Responsive Design** that works on mobile, tablet, and desktop
- **Smooth Animations** and hover effects
- **Interactive Forms** with real-time validation
- **Professional Typography** and spacing
- **Accessible Design** with proper ARIA labels
- **Loading States** and error handling
- **Flash Messaging System** for user feedback

## 🚀 Production Deployment

### For Production Use:
1. **Change Password Hashing**: Use bcrypt instead of SHA-256
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   \`\`\`

2. **Environment Variables**: Set up proper environment variables
   \`\`\`bash
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=your-database-url
   \`\`\`

3. **Database Migration**: Use PostgreSQL or MySQL for production
4. **Email Verification**: Implement email verification for new users
5. **Password Reset**: Add password reset functionality
6. **Rate Limiting**: Implement rate limiting for API endpoints
7. **HTTPS**: Set up SSL/HTTPS for secure connections
8. **Logging**: Add proper logging and monitoring

### Environment Variables:
\`\`\`bash
# Create a .env file for production
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
EMAIL_API_KEY=your-email-service-key
FLASK_ENV=production
\`\`\`

## 🛠 Database Management

### View Database Contents
\`\`\`bash
# Install sqlite3 command line tool
# Then run:
sqlite3 finora.db

# View tables
.tables

# View users
SELECT * FROM users;

# View demo requests
SELECT * FROM demo_requests;

# Exit
.quit
\`\`\`

### Reset Database
\`\`\`bash
# Delete the database file to reset
rm finora.db

# Restart the application to recreate tables
python app.py
\`\`\`

## 🧪 Testing

### Test User Registration
1. Go to `/signup`
2. Fill form with test data
3. Check `/admin/users` to see the new user
4. Verify password is hashed in database

### Test Authentication Flow
1. Register a new user
2. Try accessing `/dashboard` (should redirect to login)
3. Login with credentials
4. Should redirect to dashboard
5. Logout and verify session is cleared

### Test Demo Requests
1. Go to `/demo`
2. Fill out demo request form
3. Check `/admin/demo-requests` to see the submission
4. Verify data is saved correctly

## 📱 Browser Support

- **Chrome** (latest)
- **Firefox** (latest)
- **Safari** (latest)
- **Edge** (latest)
- **Mobile browsers** (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for demonstration purposes. Feel free to use and modify for your own projects.

## 🆘 Support

If you encounter any issues:

1. Check the console for error messages
2. Ensure Python 3.7+ is installed
3. Verify Flask is properly installed
4. Check that all files are in the correct directories
5. Make sure port 5000 is not in use by another application
6. Check database permissions (finora.db should be writable)

## 🎯 Next Steps

- [ ] Implement bcrypt password hashing
- [ ] Add email verification system
- [ ] Implement password reset functionality
- [ ] Add user profile management
- [ ] Create advanced admin dashboard
- [ ] Add email notifications
- [ ] Implement real-time notifications
- [ ] Add API documentation
- [ ] Set up automated testing
- [ ] Add monitoring and analytics
- [ ] Implement caching system
- [ ] Add data export functionality

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**

**Ready to transform pricing strategies with AI-powered intelligence!**
\`\`\`

```plaintext file="requirements.txt"
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
