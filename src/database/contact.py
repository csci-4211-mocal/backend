from typing import List
import sqlite3 as sql
from ..models import Contact

connection_str = "mocal.db"

def get_contacts_by_account_id(id: str) -> List[Contact]:
    query = \
        '''
        SELECT id, account_id, contact_id
        FROM contact
        WHERE account_id = %s
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (id,))
    contacts = cursor.fetchall()

    cursor.close()
    connection.close()

    return [ 
        Contact(
            id=contact.id, 
            account_id=contact.account_id, 
            contact_id=contact.contact_id
        )
        for contact in contacts 
    ]

def add_contact(contact: Contact):
    query = \
        '''
        INSERT INTO contact
        (id, account_id, contact_id) VALUES (%s, %s, %s)
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (contact.id, contact.account_id, contact.contact_id))

    cursor.close()
    connection.close()

def delete_contact (account_id: str, contact_id: str):
    query = \
        '''
        DELETE FROM contact
        WHERE account_id = %s
        AND contact_id = %s
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (account_id, contact_id))

    cursor.close()
    connection.close()