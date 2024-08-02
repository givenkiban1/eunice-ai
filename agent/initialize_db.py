import sqlite3
import pytz


# Connect to the database (or create it if it doesn't exist)
connection = sqlite3.connect('business_bookings.db')

# Create a cursor object
cursor = connection.cursor()

# Create the bookings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        service_name TEXT NOT NULL,
        booking_date TIMESTAMP NOT NULL,
        confirmed BOOLEAN DEFAULT FALSE,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Bookings table created successfully.")