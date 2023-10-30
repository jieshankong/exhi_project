from decouple import config
import psycopg2

# Database connection
host = config('DATABASE_HOST')
database = config('DATABASE_NAME')
user = config('DATABASE_USER')
# password = "your_password"


# Retrieve organizer_id if exists or insert new organizer and get its ID.
def get_or_insert_organizer(organizer_details, connection):
    
    # Step 1: Check if organizer already exists
    connection = psycopg2.connect(host=host, database=database, user=user)
    cursor = connection.cursor()
    cursor.execute("SELECT organizer_id FROM organizer WHERE name = %s;", (organizer_details['name'],))
    result = cursor.fetchone()

    # Step 2: If organizer exists
    if result:
        organizer_id = result[0]
    else:
        # Step 3: If organizer does not exist
        cursor.execute("INSERT INTO organizer (name, city, country) VALUES (%s, %s, %s) RETURNING organizer_id;", 
                    (organizer_details['name'], organizer_details['city'], organizer_details['country']))
        organizer_id = cursor.fetchone()[0]
        connection.commit()
    
    cursor.close()
    
    # Step 4: Make organizer_id available
    return organizer_id