import sqlite3

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertStitchedImg(img, panoId):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_blob_query = """INSERT INTO STITCHED
                            (Stitched_img) VALUES (?)"""
  empPhoto = convertToBinaryData(img)
  # Convert data into tuple format
  c.execute(sqlite_insert_blob_query, (empPhoto, ))
  print("Image and file inserted successfully as a BLOB into a table")

  c.execute("SELECT stitched_id FROM STITCHED")
  ids = c.fetchall()
  ids = ids[-1]
  id = ids[0]
  c.execute("UPDATE PANORAMAS SET STITCHED_ID = ? WHERE PANORAMA_ID = ?", (id, panoId))
  c.close() 
  conn.commit()

def insertPanorama(name, stitchedId):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """INSERT INTO PANORAMAS
                            (Panorama_name, STITCHED_ID) VALUES (?, ?)"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (name, stitchedId))
  print("Panorama inserted")
  c.close() 
  conn.commit() 

def insertImg(id, img, name):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_blob_query = """INSERT INTO PHOTOS
                            (PANORAMA_ID, Photo, Photo_name) VALUES (?, ?, ?)"""
  empPhoto = convertToBinaryData(img)
  # Convert data into tuple format
  c.execute(sqlite_insert_blob_query, (id, empPhoto, name))
  print("Image inserted")
  c.close() 
  conn.commit() 

def changeData(name, data):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """UPDATE SETUP SET """+name+""" = ? WHERE setup_name = 'setup';"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (data, ))
  print("Data inserted")
  c.close() 
  conn.commit() 

def getParams():
  conn = sqlite3.connect('.tornilloTron.db')
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

def getPanoramas():
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """SELECT * FROM PANORAMAS"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query)
  print("Panoramas obtained")
  params = c.fetchall()
  c.close() 
  conn.commit()
  return params

def getStitched(id):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """SELECT * FROM STITCHED WHERE STITCHED_ID = ?"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (id, ))
  print("Stitched obtained")
  params = c.fetchall()
  c.close() 
  conn.commit()
  return params[0]

def getImgs(id):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """SELECT * FROM PHOTOS WHERE PANORAMA_ID = ?"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (id, ))
  print("Imgs obtained")
  params = c.fetchall()
  c.close() 
  conn.commit()
  return params

def deleteImage(id):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """DELETE FROM PHOTOS WHERE PHOTO_ID = ?"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (id, ))
  print("Img removed")
  c.close() 
  conn.commit()

def deletePanorama(id):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """DELETE FROM PANORAMAS WHERE PANORAMA_ID = ?"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (id, ))
  print("Panorama removed")
  c.close() 
  conn.commit()

def deleteStitched(id):
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_query = """DELETE FROM STITCHED WHERE STITCHED_ID = ?"""
  # Convert data into tuple format
  c.execute(sqlite_insert_query, (id, ))
  sqlite_insert_query = """UPDATE PANORAMAS SET STITCHED_ID = ? WHERE STITCHED_ID = ?"""
  c.execute(sqlite_insert_query, (int(-1), id))
  print("Stitched removed")
  c.close() 
  conn.commit()

def createDataBase():
  conn = sqlite3.connect('.tornilloTron.db')
  c = conn.cursor()

  # Create table - STITCHED
  c.execute('''CREATE TABLE STITCHED
              ( STITCHED_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                Stitched_img blob)''')

  # Create table - PANORAMAS
  c.execute('''CREATE TABLE PANORAMAS
              ( PANORAMA_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                Panorama_name text, 
                STITCHED_ID INTEGER,
                FOREIGN KEY(STITCHED_ID) REFERENCES STITCHED(STITCHED_ID))''')
          
  # Create table - PHOTOS
  c.execute('''CREATE TABLE PHOTOS
              ( PHOTO_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                PANORAMA_ID INTEGER,
                Photo_name text, 
                Photo blob,
                FOREIGN KEY(PANORAMA_ID) REFERENCES PANORAMAS(PANORAMA_ID)
                )''')

  # Create table - SETUP
  c.execute('''CREATE TABLE SETUP
              ( SETUP_NAME text NOT NULL PRIMARY KEY,
                OFFSET INTEGER,
                SPEED_STEP INTEGER,
                INITIAL_SPEED INTEGER,
                SAMPLE_SIZE INTEGER,
                SIZE_STEP INTEGER,
                SPINDLE_SIZE INTEGER,
                PLATFORM INTEGER
                )''')
  print("DB Created")

  c = conn.cursor()
  print("Connected to SQLite")
  sqlite_insert_blob_query = """INSERT INTO SETUP
                            (SETUP_NAME, OFFSET, SPEED_STEP, INITIAL_SPEED, SAMPLE_SIZE, SIZE_STEP, SPINDLE_SIZE, PLATFORM) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
  # Convert data into tuple format
  c.execute(sqlite_insert_blob_query, ("setup", 0, 0, 0, 0, 0, 0, 0))
  print("Data inserted")
  c.close() 

  conn.commit()