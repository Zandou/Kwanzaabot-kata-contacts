import sys
import sqlite3
from pathlib import Path
from datetime import datetime
from random import *


class Contacts:
    def __init__(self, db_path):
        self.db_path = db_path
        if not db_path.exists():
            print("Migrating db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE contacts(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL
                )
              """
            )
            connection.commit()
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def insert_contacts(self, contacts):
        print("Inserting contacts ...")
        cursor = self.connection.cursor()
        cursor.executemany("""INSERT INTO contacts (name, email) VALUES (?,?)""", contacts)

    def get_name_for_email(self, email):
        print("Looking for email", email)
        cursor = self.connection.cursor()
        start = datetime.now()
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()
        end = datetime.now()

        elapsed = end - start
        print("query took", elapsed.microseconds / 1000, "ms")
        if row:
            name = row["name"]
            print(f"Found name: '{name}'")
            return name
        else:
            print("Not found")


def yield_contacts(num_contacts):
    # TODO: Generate a lot of contacts
    # instead of just 3
    if(not isinstance(num_contacts, int)):
        print("Please enter a valid number")
        return
    
    i=0
    while(i<=num_contacts):
        yield("name-"+str(i),"email-"+str(i)+"@domain.tld")
        i+=1
    
    # yield ("name-1", "email-1@domain.tld")
    # yield ("name-2", "email-2@domain.tld")
    # yield ("name-3", "email-3@domain.tld")


def main():
    num_contacts = int(sys.argv[1])
    db_path = Path("contacts.sqlite3")
    contacts = Contacts(db_path)
    contacts.insert_contacts(yield_contacts(num_contacts))
    charlie = contacts.get_name_for_email(f"email-{num_contacts}@domain.tld")


if __name__ == "__main__":
    main()
