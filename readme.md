# README
The project focuses on the collection of information on art exhibitions from various (in Europa located) museums.
This should enable art lovers to plan and visit exhibitions spontaneously and efficiently.

## For end user
Here are [Calendar view](https://www.notion.so/jsequaljs/fa70fdae978049db80b145b32485a489?v=ee1206773f6e4e64ab073a0c063a7da7) and 
[Gallery view](https://www.notion.so/jsequaljs/fa70fdae978049db80b145b32485a489?v=83ddd91a2cae4f51850133af49ef5279).
You can use filter to select country or city.

Organizer list (to be continued)
- Hamburger Kunsthalle
- Städel Museum
- Museum der bildenden Künste Leipzig

## For developers:
### Technology
By using web scraping ([Scrapy](https://docs.scrapy.org/en/latest/)) as part of an ELT workflow, data is extracted from museum websites, stored in an PostgreSQL database, cleansed and prepared for visualization. This data is then visualized primarily in a calendar view by Notion ([Notion API](https://developers.notion.com/reference/intro)). 

### Execution
To run `main.py`, you'll need to have Python installed on your system (or cloud system) and ensure that all dependencies required by your scripts are also installed.

> The best practice is to deploy the whole project in cloud system and schedule the exucution.

Here are the steps to execute `main.py`. 
1. **Navigate to the directory containing `main.py`**: Use the `cd` command to navigate to the directory where your `main.py` file is located.

   For example, if your `main.py` is located at `C:\Users\YourName\Projects\exhi_project`, you would type:
   ```sh
   cd C:\Users\YourName\Projects\exhi_project
   ```
   Adjust the command to the path where your `main.py` is located.

2. **Install all dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Add `.env` File**: Add your secrets, such as the Notion API Key and PostgreSQL credentials, to a `.env` file.

4. **Activate the virtual environment** (if you're using one): Before running the script, if you are using a virtual environment (`venv` as mentioned in your directory structure), you need to activate it.

   On Windows:
   ```sh
   .\venv\Scripts\activate
   ```
   On macOS/Linux:
   ```sh
   source venv/bin/activate
   ```

5. **Run `main.py`**: Once you are in the correct directory and your virtual environment is activated (if applicable), you can run `main.py` using the following command:
   ```sh
   python3 main.py
   ```

6. **Monitor the output**: As `main.py` runs, it will log the status of each script. Keep an eye on the terminal for any error messages or logs that indicate the progress of the script executions.

### Contribute
If you want to contribute new spider for a new website of exhibitions, you can do this:

1. **Navigate to the spiders directory**: Use the `cd` command to navigate to the directory where all the spiders are located.

   For example, if you are already in `...\exhi_project`, you would type:
   ```sh
   cd exhibitions\spiders
   ```

2. **Created spider 'museum_x'**: You can use template 'basic' in Scrapy. For example:
   ```sh
   scrapy genspider hamburger-kunsthalle www.hamburger-kunsthalle.de
   ```
   I always use the word in the url for the name, like here "hamburger-kunsthalle".
   
   Or you can copy paste one of the existed spider and change the spider name both in `class` and `name=`.
   
   Add organizer metadata manually. For example:
   ```python
   organizer_DETAILS = {
       "name": "Hamburger Kunsthalle",
       "city": "Hamburg",
       "country": "Germany"
    }
    ```

    Build you spider.

3. **Cleaning process before loading data to database**: You can implement initial cleaning in `exhibitions/pipeline.py`to handle the most common or straightforward date formats. Please use "item[date_str]" to save start and end dates of the exhibition together. Don't forget to update "ITEM_PIPELINES" in `exhibitions/settings.py`.

4. **Cleaning process after loading data**: To clean complicated date values in "date_str" you just need to update `processing/db_clean_utils.py`.
