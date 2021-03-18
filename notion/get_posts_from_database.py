# get_posts_from_database.py

import os
import datetime
import config
from notion.client import NotionClient
from textwrap import indent

client = NotionClient(config.NOTION_TOKEN)
contents_collection = client.get_collection(config.COLLECTION_ID)
posts = contents_collection.get_rows()

def parse_blocks(blocks):
    text = ''
    for block in blocks.children:
        # Handles H1
        if (block.type == 'header'):
            text = text + '# ' + block.title + '\n\n'
        # Handles H2
        if (block.type == 'sub_header'):
            text = text + '## ' + block.title + '\n\n'
        # Handles H3
        if (block.type == 'sub_sub_header'):
            text = text + '### ' + block.title + '\n\n'
        # Handles Code Blocks
        if (block.type == 'code'):
            text = text + '```' + block.language.lower() + '\n' + block.title + '\n```\n\n'
        # Handles Callout Blocks
        if (block.type == 'callout'):
            text = text + '> ' + block.icon + ' ' + block.title + '\n\n'
        # Handles Quote Blocks
        if (block.type == 'quote'):
            text = text + '> ' + block.title + '\n\n'
        # Handles Bookmark Blocks
        if (block.type == "bookmark"):
            text = text + "🔗 [" + block.title + "](" + block.link + ")\n\n"
        # Handles Images
        if (block.type == 'image'):
            text = text + '![' + block.id + '](' + block.source + ')\n\n'
        # Handles Bullets
        if (block.type == 'bulleted_list'):
            text = text + '- ' + block.title + '\n\n'
        # Handles Dividers
        if (block.type == 'divider'):
            text = text + '---' + '\n\n'
        # Handles Basic Text, Links, Single Line Code
        if (block.type == 'text'):
            text = text + block.title + '\n\n'
        # Handles Children
        if block.children.__len__() > 0:
            text = text + indent(parse_blocks(block), '  ')
    return text

for post in posts:
    # Handle Frontmatter
    text = """---
title: %s
date: %s
category: %s
thumbnail: { %s }
draft: %s
---\n\n""" % (post.title,
          post.date.strftime("%Y-%m-%d %H:%M:%S"),
          post.category,
          "thumbnailSrc" if not post.thumbnail else post.thumbnail[0],
          "true" if post.draft else "false")

    # Handle Title
    text = text + '# ' + post.title + '\n\n'
    text = text + parse_blocks(post)
    title = post.title.replace(' ', '-')
    title = title.replace(',', '')
    title = title.replace(':', '')
    title = title.replace(';', '')
    title = title.lower()
    try:
        os.makedirs('../content/blog/' + title)
    except:
        pass
    file = open('../content/blog/' + title + '/index.md', 'w')
    print('Wrote A New Page')
    print(text)
    file.write(text)