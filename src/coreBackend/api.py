# shopMaster360/api.py
from ninja import Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI
from apps.users.schemas import SignInSchema
from django.contrib.auth import authenticate, login, logout, get_user_model

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


# Attach routers
# Ensure routers are only attached once
api.add_router("/users/", "apps.users.api.router")

# get user model
User = get_user_model()


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # is not request.user.is_authenticated
    email: str = None


@api.get("/hello")
def hello(request):
    print(request)
    return {"message": "Hello world"}


@api.get("/me", response=UserSchema, auth=JWTAuth())
def me(request):
    return request.user


@api.post("/login")
def login_view(request, payload: SignInSchema):
    user = authenticate(request, username=payload.email,
                        password=payload.password)
    if user is not None:
        login(request, user)
        return {"success": True}
    return {"success": False, "message": "Invalid credentials"}


@api.post("/register")
def register(request, payload: SignInSchema):
    try:
        User.objects.create_user(
            username=payload.email, email=payload.email, password=payload.password)
        return {"success": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}


@api.post("/logout", auth=JWTAuth())
def logout_view(request):
    logout(request)
    return {"message": "Logged out"}
