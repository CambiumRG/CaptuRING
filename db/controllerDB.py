import sqlite3


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def changeData(name, data):
    conn = sqlite3.connect('.CaptuRING.db')
    c = conn.cursor()
    print("Connected to SQLite")
    sqlite_insert_query = """UPDATE SETUP SET """ + \
        name+""" = ? WHERE setup_name = 'setup';"""
    # Convert data into tuple format
    c.execute(sqlite_insert_query, (data, ))
    print("Data inserted")
    c.close()
    conn.commit()


def getParams():
    conn = sqlite3.connect('.CaptuRING.db')
    c = conn.cursor()
    print("Connected to SQLite")
    sqlite_insert_query = """SELECT * FROM SETUP WHERE setup_name = 'setup';"""
    # Convert data into tuple format
    c.execute(sqlite_insert_query)
    print("Data obtained")
    params = c.fetchall()
    c.close()
    conn.commit()
    return params[0]


def createDataBase():
    conn = sqlite3.connect('.CaptuRING.db')
    c = conn.cursor()

    # Create table - SETUP
    c.execute('''CREATE TABLE SETUP
              ( SETUP_NAME text NOT NULL PRIMARY KEY,
                OFFSET INTEGER,
                SPEED_STEP INTEGER,
                INITIAL_SPEED INTEGER,
                SAMPLE_SIZE INTEGER,
                SIZE_STEP INTEGER,
                SPINDLE_SIZE INTEGER,
                PLATFORM INTEGER,
                SAMPLE_SIZE_Y INTEGER,
                SIZE_STEP_Y INTEGER
                )''')
    print("DB Created")

    c = conn.cursor()
    print("Connected to SQLite")
    sqlite_insert_blob_query = """INSERT INTO SETUP
                            (SETUP_NAME, OFFSET, SPEED_STEP, INITIAL_SPEED, SAMPLE_SIZE, SIZE_STEP, SPINDLE_SIZE, PLATFORM, SAMPLE_SIZE_Y, SIZE_STEP_Y) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    # Convert data into tuple format
    c.execute(sqlite_insert_blob_query, ("setup", 0, 0, 0, 0, 0, 0, 0, 0, 0))
    print("Data inserted")
    c.close()

    conn.commit()
