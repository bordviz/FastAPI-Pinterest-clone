<img src="https://github.com/BORDVIZ/FastAPI-Pinterest-clone/blob/main/static/Pinterest-logo.png" alt="" height="400" align="right">

# FastAPI Pinterst clone

> REST API Pinterest API clone with FastAPI 
>
> Implemented endpoints:
> - Register 
> - Login
> - Refresh token 
> - Get verify mail
> - Send verify code
> - Get current user profile
> - Get user subscribers
> - Get user subscriptions
> - Subscribe to user
> - Unsubscribe from user
> - Update user avatar
> - Delete user avatar
> - Get user by id
> - Get image
> - Post image
> - Create post
> - Add like to post
> - Search post
> - Get new posts
> - Get post by id

<br clear="right">

### Project Stack: 
 - FastAPI
 - PostgreSQL
 - Bcrypt
 - JWT
 - Alembic
 - Pydantic
 - Uvicorn
 - Celery
 - Redis
 - FastAPI-Cache2

### Start the application
1. Create a virtual environment and install dependencies
2. Run `pip install -r requirements.txt` in the terminal
3. Create .env file (change the value of the variables to your own)
```
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = postgres
DB_USER = postgres
DB_PASS = postgres

SECRET = secret
REFRESH_SECRET = secret
ALGORITHM = HS256

REDIS_HOST = localhost
REDIS_PORT = 6379

EMAIL_SEND = example@gmail.com 
EMAIL_PASS = 111222333

SMTP_HOST = smtp.gmail.com
SMTP_PORT = 465

IMAGE_PLACEHOLDER = http://localhost:8000
```

### Application launch
1. Go to the `src` folder
2. Run `uvicorn main:app --reload` in the terminal

<img src="https://github.com/BORDVIZ/FastAPI-Pinterest-clone/blob/main/static/swagger.png" alt="">
