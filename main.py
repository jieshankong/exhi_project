import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to the scripts that need to be run
spiders_path = Path('exhibitions/spiders')
db_clean_script = Path('processing/db_insert_date_clean.py')
notion_update_script = Path('processing/notion_update.py')

# List of spider scripts
spider_scripts = ['hamburger-kunsthalle', 'mdbk', 'staedelmuseum']

def run_spider(spider_script):
    try:
        subprocess.check_output(['scrapy', 'crawl', spider_script])
        logging.info(f'Successfully ran spider {spider_script}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error running spider {spider_script}: {e.output.decode()}')
        return False
    return True

def run_script(script_path):
    try:
        subprocess.check_output(['python3', script_path])
        logging.info(f'Successfully ran script {script_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error running script {script_path}: {e.output.decode()}')
        raise e

def main():
    # Get the directory in which main.py is located
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Change the current working directory to that directory
    os.chdir(dir_path)

    # Run all the spiders
    for spider_script in spider_scripts:
        if not run_spider(spider_script):
            logging.error(f'Spider {spider_script} failed, continuing with others...')

    # Run db_insert_date_clean.py
    try:
        run_script(db_clean_script)
    except subprocess.CalledProcessError:
        logging.error(f'{db_clean_script} failed, stopping the process.')
        return

    # Run notion_update.py
    try:
        run_script(notion_update_script)
    except subprocess.CalledProcessError:
        logging.error(f'{notion_update_script} failed, stopping the process.')
        return

    logging.info('All scripts ran successfully.')

if __name__ == '__main__':
    main()
