# FastAPI (Learning Project)

This is a FastAPI project I am building while learning modern web development with:

- **FastAPI** - Modern Python web framework
- **SQLAlchemy ORM** - Database abstraction layer
- **PostgreSQL** - Production-ready database
- **OAuth2 with JWT** - Secure authentication
- **Password hashing** - Security best practices

## 🚀 Features Implemented

### 🔐 Authentication & Security
- OAuth2 password flow with JWT tokens
- Password hashing using bcrypt
- Role-based access control (Admin/User)
- Secure token-based authentication

### 📊 Database & Models
- PostgreSQL database setup
- SQLAlchemy ORM with relationships
- User model with roles and authentication
- Todo model with user ownership

### 🎯 API Endpoints

#### Authentication Routes (`/auth`)
- `POST /auth/` - Create new user account
- `POST /auth/token` - Login and get JWT token
- User registration with role assignment

#### Todo Management Routes
- `GET /` - Get user's own todos
- `GET /todos/{id}` - Get specific todo
- `POST /createTodo` - Create new todo
- `PUT /todo/updateTodo/{id}` - Update todo
- `DELETE /todo/{id}` - Delete todo
- - Admin authorization with id

#### Admin Routes (`/auth`)
- `GET /auth/todo` - Get all todos (Admin only)
- `DELETE /admin/todo/{todo_id}` - Delete todo (Admin only)
- Admin authorization with role checking

#### User Routes (`/user`)
- `GET /user/` - Get user details
- `PUT /user/changePassword` - Update user password
- Admin authorization with id

### 🔒 Security Features
- JWT token expiration (20 minutes)
- Password hashing with bcrypt
- User role verification
- Protected routes with dependencies
- Secure user data isolation

## 🛠️ Technical Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: OAuth2 + JWT
- **Security**: bcrypt password hashing
- **Validation**: Pydantic models
