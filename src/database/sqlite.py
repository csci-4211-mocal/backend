import sqlite3 as sql

connection_str = 'mocal.db'

def setup():
    '''
    Initial setup for DB
    '''
    query = \
        '''
        CREATE TABLE IF NOT EXISTS
        account (
            id TEXT PRIMARY KEY not null,
            username TEXT not null,
            password TEXT not null
        );
        
        CREATE TABLE IF NOT EXISTS
        contact (
            id TEXT PRIMARY KEY not null,
            account_id TEXT not null,
            contact_id TEXT not null
        );

        CREATE TABLE IF NOT EXISTS
        event_data (
            id TEXT PRIMARY KEY not null,
            to_account TEXT not null,
            from_account TEXT not null,
            data TEXT not null
        );
        '''
        

    connection = sql.connect(connection_str)
    cursor = connection.cursor()

    cursor.executescript(query)

    cursor.close()
    connection.close()