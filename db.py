import json
import sqlite3

# read in our data from the json file
fighters = json.load(open('./data/fighters.json'))
events = json.load(open('./data/events.json'))

# create a connection to our local database
connection = sqlite3.connect('ufc.db')

# create a cursor to execute queries
cursor = connection.cursor()

# lets make sure the fighter table exists
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS fighter
    (name text, wins integer, losses integer, draws integer, height integer, stance text, dob text, url text, slpm real, stracc real, sapm real, strdef real, tdavg real,tdacc real, tddef real, subavg real)
""",
)

# add fighters to the fighter table
for fighter in fighters:
    cursor.execute(
        """
        INSERT INTO fighter (name, wins, losses, draws, height, stance, dob, url, slpm, stracc, sapm, strdef, tdavg, tdacc, tddef, subavg)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            fighter['name'],
            fighter['wins'],
            fighter['losses'],
            fighter['draws'],
            fighter['height'],
            fighter['stance'],
            fighter['dob'],
            fighter['fighter_url'],
            fighter['stats']['SLpM'],
            fighter['stats']['StrAcc'],
            fighter['stats']['SApM'],
            fighter['stats']['StrDef'],
            fighter['stats']['TDAvg'],
            fighter['stats']['TDAcc'],
            fighter['stats']['TDDef'],
            fighter['stats']['SubAvg'],
        ),
    )

# lets make sure the event table exists
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS event
    (title text, date text, location text, completed boolean)
    """,
)

# add events to the event table
for event in events:
    cursor.execute(
        """
    INSERT INTO event (title, date, location, completed)
         VALUES (?,?,?,?)
         """,
        (event['title'], event['date'], event['location'], event['completed']),
    )

# commit our changes to the database
connection.commit()

# close our connection to the database
connection.close()
