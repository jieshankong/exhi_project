from decouple import config
import psycopg2

# Database connection parameters
host = config('DATABASE_HOST')
database = config('DATABASE_NAME')
user = config('DATABASE_USER')
# password = "your_password"

# SQL command to create the organizer table
create_table_command = """
CREATE TABLE IF NOT EXISTS organizer (
    organizer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);
"""

try:
    # Establish a connection to the database
    connection = psycopg2.connect(host=host, database=database, user=user)
    # connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
    
    # Create a cursor object
    cursor = connection.cursor()
    
    # Execute the SQL command to create the table
    cursor.execute(create_table_command)
    
    # Commit the changes
    connection.commit()
    
    print("Table 'organizer' created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
