# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from datetime import datetime
from decouple import config

# import datetime
# class TimestampPipeline:
#     def process_item(self, item, spider):
#         item['timestamp'] = datetime.datetime.now().isoformat()
#         return item
    
# Combine date_start and date_end (the ISO 8601 string ("2023-10-13T00:00:00+02:00")) to date_str
class ISOstringCleaningPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        applicable_spiders = ["hamburger-kunsthalle"]

        if spider.name in applicable_spiders:
            date_start_value = adapter.get('date_start')
            date_end_value = adapter.get('date_end')

            # Extract and format start and end dates
            start_date = date_start_value[0].split('T')[0] if date_start_value else None
            end_date = date_end_value[0].split('T')[0] if date_end_value else None

            # Combine and set the date_str
            adapter['date_str'] = start_date + "to" + end_date if start_date and end_date else None

        return item

# Convert date string (e.g. "29.6.23 - 14.1.24") to a datetime object
class DateNrstringCleanPipeling:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        applicable_spiders = ["louisianna"]

        if spider.name in applicable_spiders:
            date_value = adapter.get('date')
            if date_value:
                dates = date_value[0].split(' - ')
                if len(dates) == 2:
                    start_date_str, end_date_str = dates

                    # Convert to datetime objects
                    start_date = self.parse_date(start_date_str)
                    end_date = self.parse_date(end_date_str)

                    # Format dates into YYYY-MM-DD
                    adapter['start_date'] = start_date.strftime('%Y-%m-%d') if start_date else None
                    adapter['end_date'] = end_date.strftime('%Y-%m-%d') if end_date else None

        return item

    def parse_date(self, date_str):
        try:
            # Assuming the year is in two digits and belongs to 2000s
            return datetime.strptime(date_str, '%d.%m.%y')
        except ValueError:
            return None
            

# Saving data to a postgre database
class PostgresExportPipeline:

    def __init__(self):
        ## Connection Details
        hostname = config('DATABASE_HOST')
        username = config('DATABASE_USER')
        #password = '*******' # your password
        database = config('DATABASE_NAME')

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create exhi table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS exhibition(
            id serial PRIMARY KEY, 
            url text,
            img text,
            title text,
            subtitle text,
            date_str text,
            venue text,
            organizer_id int,
            description text,
            UNIQUE(title, organizer_id)
        )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            ## Define insert statement
            self.cur.execute(""" INSERT INTO exhibition (
                url,
                img, 
                title, 
                subtitle, 
                date_str,
                venue,
                organizer_id,
                description
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    )
                    ON CONFLICT (title, organizer_id)
                    DO UPDATE SET 
                        date_str = EXCLUDED.date_str
                    """, (
                item["url"],
                item["img"],
                item["title"],
                item['subtitle'],
                item['date_str'],
                item['venue'],
                item['organizer_id'],
                str(item["description"])
            ))

            ## Execute insert of data into database
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()  # Rollback in case of error
            raise  # Optional: re-raise the exception if you want it to be propagated
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()