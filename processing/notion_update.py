from decouple import config
import requests
from db_query import df
from notion_check_utils import readDatabase, extract_titles

token = config('NOTION_token')
databaseID = config('NOTION_databaseID')
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def create_page(data: dict, children: list, databaseID: str, headers: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": databaseID}, "properties": data, "children": children}
    res = requests.post(create_url, headers=headers, json=payload)
    return res

def split_text(content, max_length=2000):
    """
    Split the text content into chunks with each having a maximum length of 2000 characters.
    """
    return [content[i:i + max_length] for i in range(0, len(content), max_length)]

existing_pages = readDatabase(databaseID=databaseID, headers=headers)
titles = extract_titles(existing_pages)

for index, row in df.iterrows():
    title = row['title']
    if title not in titles:
        properties = {
            "title": {"title": [{"text": {"content": row['title']}}]},
            "gEVf": {"rich_text": [{"text": {"content": row['subtitle'] if row['subtitle'] is not None else ""}}]},
            "%5Evz%60": {"date": {"start": str(row['date_start']), "end": str(row['date_end'])}},
            "Ydop": {"url": row['url']},
            "%3Eye%7D": {"rich_text": [{"text": {"content": row['country']}}]},
            "%5B%3D%60%3A": {"rich_text": [{"text": {"content": row['name']}}]},
            "j%60Lr": {"rich_text": [{"text": {"content": row['city']}}]}
        }

        children = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": row['title'] if row['title'] is not None else ""}}]
                }
            },            
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": row['subtitle'] if row['subtitle'] is not None else ""}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "venue: " + row['venue'] if row['venue'] is not None else ""}}]
                }
            }
        ]

        # Handle long description text
        description_content = row.get('description', "")
        description_chunks = split_text(description_content)
        for chunk in description_chunks:
            paragraph_block = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}]
                }
            }
            children.append(paragraph_block)

        try:
            response = create_page(properties, children, databaseID, headers)
            if response.status_code == 200:
                print(f"Page for {title} created successfully.")
            else:
                print(f"Failed to create page for {title}. Status Code: {response.status_code}, Reason: {response.text}")
        except Exception as e:
            print(f"Error creating page for {title}: {e}")
    else:
        print(f"Page with title '{title}' already exists. Skipping creation.")
