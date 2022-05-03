import json
from uuid import uuid4
from fastapi import APIRouter, status, Request
from fastapi.exceptions import HTTPException

from ..models import Authorization, NewEvent, DeleteEvent, Event
from ..auth import extract_claims
from ..database.account import get_account_by_id, get_account_by_username
from ..database.contact import add_contact
from ..database.event import delete_events, get_all_events, add_events

router = APIRouter()

@router.post('/all')
async def get_events(authorization: Authorization):
    token = authorization.token
    if token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    events = get_all_events(account_id)
    if events is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No events found")

    return { "events": events }


@router.post('/new')
async def new_event(new_event: NewEvent):
    token = new_event.token
    if token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    contact_username = new_event.to_account
    found_contact = get_account_by_username(contact_username)
    if found_contact is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Contact doesn't exist")

    payload = new_event.payload
    
    event = Event(
        id=str(uuid4()),
        to_account=found_contact.id,
        from_account=account_id,
        data=payload
    ) 

    add_events(event)


@router.post('/delete')
async def delete(delete_event: DeleteEvent):
    token = delete_event.token
    if token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    delete_events(delete_event.event_id)