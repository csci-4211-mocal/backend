from typing import List
import sqlite3 as sql
from ..models import Account

connection_str = "mocal.db"

def get_account_by_id(id: str) -> Account:
    '''
    Get account by ID
    '''
    query = \
        '''
        SELECT id, username, password
        FROM account
        WHERE id = %s
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (id,))
    found_account = cursor.fetchone()
    if found_account is None:
        return None

    account = Account()
    account.id = found_account[0]
    account.username = found_account[1]
    account.password = found_account[2]

    cursor.close()
    connection.close()

    return account

def get_account_by_username(username: str) -> Account:
    '''
    Get account by username
    '''
    query = \
        '''
        SELECT id, username, password
        FROM account
        WHERE username = %s
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (id,))
    found_account = cursor.fetchone()
    if found_account is None:
        return None

    account = Account()
    account.id = found_account[0]
    account.username = found_account[1]
    account.password = found_account[2]

    cursor.close()
    connection.close()

    return account

def new_account(account: Account):
    '''
    New account
    '''
    query = \
        '''
        INSERT INTO account
        (id, username, password) VALUES (%s, %s, %s)
        '''
    
    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (account.id, account.username, account.password))
    
    cursor.close()
    connection.close()