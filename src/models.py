from pydantic import BaseModel

class Account():
    id: str
    username: str
    password: str

class Contact():
    id: str
    account_id: str
    contact_id: str

    def __init__(self, id, account_id, contact_id) -> None:
        self.id=id
        self.account_id=account_id
        self.contact_id=contact_id

class Event():
    id: str
    to_account: str
    from_account: str
    data: str

    def __init__(self, id, to_account, from_account, data) -> None:
        self.id=id
        self.to_account=to_account
        self.from_account=from_account
        self.data=data

class Credentials(BaseModel):
    username: str
    password: str

class Authorization(BaseModel):
    token: str

class NewContact(BaseModel):
    id: str

class NewEvent(BaseModel):
    token: str
    to_account: str
    payload: str

class DeleteEvent(BaseModel):
    token: str
    event_id: str