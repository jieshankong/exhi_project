from db_clean_utils import clean_date
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

# Database connection
host = config('DATABASE_HOST')
database = config('DATABASE_NAME')
user = config('DATABASE_USER')
# password = "your_password"

# Connect to the database
engine = create_engine(f'postgresql://{user}@{host}/{database}')
#engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')

# Read data from PostgreSQL
query = "SELECT id, date_str FROM exhibition;"
df = pd.read_sql(query, engine)

# Apply the cleaning function
df[['date_start', 'date_end']] = df['date_str'].apply(lambda x: clean_date(x)).tolist()

# Drop the original date_str column
df.drop(columns=['date_str'], inplace=True)

#Overwrite data in the "date_clean" table
df.to_sql('date_clean', engine, if_exists='replace', index=False)

print("Data cleaning and insertion completed successfully.")