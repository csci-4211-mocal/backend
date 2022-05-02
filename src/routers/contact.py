from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from uuid import uuid4

from ..models import Authorization, Contact, NewContact

from ..auth import extract_claims
from ..database.contact import get_contacts_by_account_id, add_contact, delete_contact
from ..database.account import get_account_by_id
router = APIRouter()

@router.get('/')
async def get_contacts(authorization: Authorization):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    contacts = get_contacts_by_account_id(account_id)
    if contacts is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, "No contacts found")

    return { "contacts": contacts }
    

@router.post('/new')
async def new_contact(authorization: Authorization, new_contact: NewContact):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    contact_id = new_contact.id
    found_contact = get_account_by_id(contact_id)
    if found_contact is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid contact")
    
    contact = Contact()
    contact.id = uuid4()
    contact.account_id = account_id
    contact.contact_id = contact_id
    
    add_contact(contact)

    
@router.post('/delete')
async def delete(authorization: Authorization, contact: NewContact):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    contact_id = contact.id
    found_contact = get_account_by_id(contact_id)
    if found_contact is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid contact")

    delete_contact(account_id, found_contact.id)