from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from typing import Dict, List, Union

from coreBackend.schemas import CustomResponse
from apps.users.schemas import UserDetailSchema

# define router
router = Router()

# get user model & define jwt auth
User = get_user_model()
auth = JWTAuth()


# define apis

@router.get('', response=Union[List[UserDetailSchema], CustomResponse])
def list_users(request):
    try:
        return User.objects.all()
    except Exception as e:
        return {"error": str(e)}
