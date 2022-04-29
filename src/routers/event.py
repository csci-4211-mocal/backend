import json
from uuid import uuid4
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from models import Authorization, EventsList, NewEvent, Event
from ..auth import extract_claims
from ..database.account import get_account_by_id
from ..database.contact import add_contact
from database.event import delete_events, get_events, add_events

router = APIRouter()

@router.get('/')
async def get_events(authorization: Authorization):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    events = get_events(account_id)
    if events is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, "No events found")

    return { "events": events }


@router.post('/new')
async def new_event(authorization: Authorization, new_event: NewEvent):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    contact_id = new_event.to_account
    found_contact = get_account_by_id(contact_id)
    if found_contact is not None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Contact already exists")

    payload = new_event.payload
    events_data = json.loads(payload)
    
    events = [ 
        Event(
            id=uuid4(),
            to_account=new_event.to_account,
            from_account=account_id,
            data=json.dumps(e)
        ) 
        for e in events_data 
    ]

    add_events(events)


@router.post('/delete')
async def delete(authorization: Authorization, events_list: EventsList):
    token = authorization.token
    if token is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "No token provided")
    
    claims = extract_claims(token)
    if claims is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    account_id = claims['id']
    if account_id is None:
        return HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    events = events_list.events
    delete_events(events)