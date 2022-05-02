from typing import List
import sqlite3 as sql
from ..models import Event

connection_str = "mocal.db"

def get_events(to_account: str) -> List[Event]:
    '''
    Get event data for account
    '''
    query = \
        '''
        SELECT id, to_account, from_account, data
        FROM event_data
        WHERE to_account = ?
        '''
    
    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (to_account,))
    event_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        Event(
            id=e[0],
            to_account=e[1],
            from_account=e[2],
            data=e[3]
        )
        for e in event_data
    ]


def add_events(event: Event):
    '''
    Add event data for account
    '''
    query = \
        '''
        INSERT INTO event_data
        (id, to_account, from_account, data) VALUES (?, ?, ?, ?);
        '''

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.execute(query, (event.id, event.to_account, event.from_account, event.data))
    connection.commit()

    cursor.close()
    connection.close()


def delete_events(events: List[str]):
    '''
    Delete events
    '''
    query = \
        '''
        DELETE FROM event_data
        WHERE id = ?
        '''
    
    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.executemany(query, [ (e,) for e in events ])

    cursor.close()
    connection.close()