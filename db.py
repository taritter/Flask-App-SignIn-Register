"""
This file includes a simple database class, which provides methods:

    execute_query:  Takes a query as a string and executes it with a current
                    database connection. Doing things this way is not advised,
                    since it introduces vulnerability to injection attack.
                    We do it this way for instructional purposes only!

    setup:          A utility to create a fresh instance of the database,
                    and to populate it with some records for testing.

Here we use SQLite directly rather than an ORM (object relational mapper, e.g.,
SQLAlchemy) because it's easier for students to see what's going on in SQL
queries.
"""

import sqlite3
from password import hash_pw
from password import authenticate
from password import check_password
from datetime import datetime


class Db:
    """Database class for account environment. """

    # SQL query to create `account` table
    CREATE_TABLE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account (
        id integer PRIMARY KEY,
        username text NOT NULL,
        pw_hash text NOT NULL,
        level integer NOT NULL,
        created_at datetime NOT NULL,
        last_login datetime NOT NULL
    );"""

    INSERT_ACCOUNT = """INSERT INTO account
        (id, username, pw_hash, level, created_at, last_login)
        VALUES (?, ?, ?, ?, ?, ?);"""
    
    SELECT_USER = """SELECT * FROM account where username=?"""


    UPDATE_LAST_LOGIN = """UPDATE account SET last_login=? WHERE id=?"""

    UPDATE_LEVEL = """UPDATE account SET level=? WHERE id=?"""


    @staticmethod
    def login(username, password):
        """
        Get a connection to the database
        :return: sqlite3.Connection
        """
        db = sqlite3.connect('accounts.sqlite')
        db.execute(Db.CREATE_TABLE_ACCOUNT)
        cursor=db.cursor()
        cursor.execute(Db.SELECT_USER, (username,))
        user = cursor.fetchone()
        if user == None:
            return None
        if authenticate(user[2], password):
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute(Db.UPDATE_LAST_LOGIN, (current_time, user[0]))
            db.commit()
            return user
        else:
            return None
        
    @staticmethod
    def register(username, password):
        db = sqlite3.connect('accounts.sqlite')
        db.execute(Db.CREATE_TABLE_ACCOUNT)
        cursor = db.cursor()
        
        cursor.execute(Db.SELECT_USER, (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # username already exists
            cursor.close()
            db.close()
            return 0
        elif not check_password(password):
            return 1
        
        cursor.execute(f"SELECT COUNT(*) FROM account")
        length = cursor.fetchone()[0]
        level = 0
        pw_hash = hash_pw(password)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(Db.INSERT_ACCOUNT, (length, username, pw_hash, level, current_time, current_time))
        cursor.execute(Db.SELECT_USER, (username,))
        new_user = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        print(f"username {username} and pass {password}")
        return new_user
            

    @staticmethod
    def level_update(username, level):
        db = sqlite3.connect('accounts.sqlite')
        db.execute(Db.CREATE_TABLE_ACCOUNT)
        cursor = db.cursor()
        cursor.execute(Db.SELECT_USER, (username,))
        user = cursor.fetchone()
        db.execute(Db.UPDATE_LEVEL, (level, user[0]))
        cursor.execute(Db.SELECT_USER, (username,))
        new_user = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        return new_user