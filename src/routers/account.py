from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from uuid import uuid4

from ..database.account import get_account_by_id, get_account_by_username, new_account
from ..auth import extract_claims, generate_token
from ..models import Account, Authorization, Credentials

router = APIRouter()

@router.post('/info')
async def get_account_data(authorization: Authorization):
    token = authorization.token
    if token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")

    claims = extract_claims(token)
    account_id = claims['id']
    if account_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token provided")

    print(account_id)

    account = get_account_by_id(account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No account found")

    refresh_token = generate_token(account_id)
    if refresh_token is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not generate refresh token")

    return { "info": account, "token": refresh_token }


@router.post('/login')
async def login(credentials: Credentials):
    username = credentials.username
    password = credentials.password

    found_account = get_account_by_username(username)
    if found_account is not None:
        if password != found_account.password:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")

        token = generate_token(found_account.id)
        return { "info": found_account, "token": token }

    account = Account()
    account.id = str(uuid4())
    account.username = username
    account.password = password
    new_account(account)
    token = generate_token(account.id)

    return { "info": account, "token": token }