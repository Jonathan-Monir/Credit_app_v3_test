import contract
import price_cost
import invoice
import file_uploader
import sqlite3
import streamlit as st

# Connect to a SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store the list
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mylist (
        id INTEGER PRIMARY KEY,
        value INTEGER NOT NULL
    )
''')

value = st.number_input("input",1,5)

if st.button("submit"):
    
    # Insert data into the table
    values = range(value)
    for value in values:
        cursor.execute('INSERT INTO mylist (value) VALUES (?)', (value,))

    # Commit the changes
    conn.commit()

    # Query data
    cursor.execute('SELECT * FROM mylist')
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        st.write(row)

    # Close the connection
    conn.close()

