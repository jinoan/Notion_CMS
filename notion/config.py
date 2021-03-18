import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from key import key

NOTION_PAGE_URL = "https://www.notion.so/jinoan/Blog-CMS-37b45a6339e848e28e05fc02c476cbad"
NOTION_TOKEN = key.get_notion_token()
COLLECTION_ID = key.get_collection_id()
