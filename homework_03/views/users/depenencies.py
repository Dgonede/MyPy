from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from views.users.crud import storage

http_bearer = HTTPBearer(auto_error=False)

def get_user_by_auth_token(
          token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
     print(token)
     user = storage.get_by_token(token = token.credentials)
     if user.password == "Admin":
          return user
     raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Not authenticated"
     ) 

def get_user_by_pass(
          password: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
          
):

     user = storage.get_by_pass(password = password.credentials)
     if user:
          return user
     raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Incorrect password"
     ) 
     