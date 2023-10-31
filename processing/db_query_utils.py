from decouple import config
import psycopg2
import pandas as pd

# Establish the connection
connection = psycopg2.connect(
    host=config('DATABASE_HOST'),
    database=config('DATABASE_NAME'),
    user = config('DATABASE_USER')
)

df = pd.read_sql("""
SELECT e.title
	,e.subtitle
	,d.date_start
	,d.date_end
	,e.venue
	,o.name
	,o.city
	,o.country
	,e.description
    ,e.url
    ,e.img
FROM exhibition AS e
INNER JOIN date_clean AS d
ON e.id = d.id
INNER JOIN organizer AS o
ON e.organizer_id = o.organizer_id
WHERE d.date_start IS NOT NULL
                 """, connection)

connection.close()

#df = df.head(3)
#print(df)