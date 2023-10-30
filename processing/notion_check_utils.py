import pandas as pd
import requests, json
from decouple import config

## https://thienqc.notion.site/Notion-API-Python-ca0fd21bc224492b8daaf37eb06289e8
## https://www.python-engineer.com/posts/notion-api-python/
## https://developers.notion.com/reference/intro

# https://www.notion.so/jsequaljs/fa70fdae978049db80b145b32485a489?v=8d31544961884ca2b76dc2f684690227&pvs=4
# https://www.notion.so/my-integrations

token = config('NOTION_token')
databaseID = config('NOTION_databaseID')
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def readDatabase(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./full-properties.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
    return data

def extract_titles(existing_pages):
    titles = set()
    for page in existing_pages.get('results', []):
        title_property = page.get('properties', {}).get('title', {}).get('title', [])
        if title_property:
            title_text = title_property[0].get('text', {}).get('content', '')
            titles.add(title_text)
    return titles

readDatabase(databaseID=databaseID, headers=headers)
# titles = extract_titles(existing_pages)
# print(titles)

# def archive_page(page_id):
#     update_url = f"https://api.notion.com/v1/pages/{page_id}"
#     payload = {
#         "archived": True
#     }
#     res = requests.patch(update_url, headers=headers, json=payload)
#     return res

# # Get a list of all page IDs in the database
# def get_page_ids(database_id):
#     read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
#     res = requests.post(read_url, headers=headers)
#     page_ids = [page['id'] for page in res.json()['results']]
#     return page_ids

# page_ids = get_page_ids(databaseID)
# for page_id in page_ids:
#     response = archive_page(page_id)
#     print(response.status_code)