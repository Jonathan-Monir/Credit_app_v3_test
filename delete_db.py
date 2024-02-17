import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('setups.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Specify the name of the table you want to delete
table_name = 'hotel'

# Construct the SQL query to drop the table
drop_query = f"DROP TABLE IF EXISTS {table_name}"

# Execute the query to drop the table
cursor.execute(drop_query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print(f"The table '{table_name}' has been deleted successfully.")