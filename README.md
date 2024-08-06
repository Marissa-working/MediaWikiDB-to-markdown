# MediaWiki to Markdown Exporter

This repository contains scripts and tools for exporting all pages from a MediaWiki database to Markdown format using Pandoc. The process involves extracting newest page content and titles from a MediaWiki SQLite/MySQL database (version >= 1.35) and converting it into Markdown files.

## Prerequisites

- Python 3.x
- Pandoc
- SQLite3 (or MySQL, depending on your database)

## Determine Your MediaWiki Version

1. Go to the main page of your wiki.
2. Click on 'Special pages' in the sidebar under 'Tools'.
3. Click on 'Version' under 'Wiki data and tools' to find your MediaWiki version and PHP details.

## Locate Your Database

1. Find `LocalSettings.php` on your wiki server.
2. Look for `$wgDBtype` to determine if your database is SQLite or MySQL.
3. For SQLite, check `$wgSQLiteDataDir` for the database location.

References:
- [LocalSettings.php](https://www.mediawiki.org/wiki/Manual:LocalSettings.php)
- [Database Access](https://www.mediawiki.org/wiki/Manual:Database_access)

## Use the Right Query to Get Each Page Title and Page Content

To better understand the relationships between tables, I recommend visualizing your data using a specific wiki page before running any queries. Don't forget to filter your database by namespace:
| Number | Canonical name | Localized name |
|--------|----------------|----------------|
| -2     | Media          | Media          |
| -1     | Special        | Special        |
| 0      | (Main)         |                |
| 1      | Talk           | Talk           |
| 2      | User           | User           |
| 3      | User talk      | User talk      |
| 4      | Project        | Project        |
| 5      | Project talk   | Project talk   |
| 6      | File           | File           |
| 7      | File talk      | File talk      |
| 8      | MediaWiki      | MediaWiki      |
| 9      | MediaWiki talk | MediaWiki talk |
| 10     | Template       | Template       |
| 11     | Template talk  | Template talk  |
| 12     | Help           | Help           |
| 13     | Help talk      | Help talk      |
| 14     | Category       | Category       |
| 15     | Category talk  | Category talk  |

### MediaWiki Database Schema & Visualization References

- [Page Table](https://www.mediawiki.org/wiki/Manual:Page_table)
- [Revision Table](https://www.mediawiki.org/wiki/Manual:Revision_table)
- [Text Table](https://www.mediawiki.org/wiki/Manual:Text_table)
- [Database Layout Diagram](https://www.mediawiki.org/w/index.php?title=Manual:Database_layout/diagram&action=render)
- [MediaWiki Namespaces](https://www.mediawiki.org/wiki/Help:Namespaces)
- [Sqlite browser to visualize your data](https://sqlitebrowser.org/)

### If Your MediaWiki Version is < 1.35

According to the MediaWiki Manual Page, to retrieve the text of an article, MediaWiki first searches for `page_title` in the `page` table. Then, `page.page_latest` is used to search the `revision` table for `rev_id`, and `revision.rev_text_id` is obtained in the process. The value obtained for `rev_text_id` is used to search for `old_id` in the `text` table to retrieve the text.

Your query will look like `old_export_titles_and_contents.sql`:

```sql
SELECT page.page_title, text.old_text
FROM page
JOIN revision ON page.page_latest = revision.rev_id
JOIN text ON revision.rev_text_id = text.old_id
WHERE page.page_namespace = 0;
```

### For MediaWiki Version >= 1.35

Unfortunately, according to MediaWiki Manual Page, revision.rev_text_id is removed in MediaWiki version 1.35. This column was replaced by content.content_address which can be retrieved by getting the slot_content_id for the corresponding revision in the slots table.

For MediaWiki 1.35 and newer, use the following query:
```sql
SELECT page.page_title, text.old_text
FROM page
JOIN revision ON page.page_latest = revision.rev_id
JOIN slots ON revision.rev_id = slots.slot_revision_id
JOIN content ON slots.slot_content_id = content.content_id
JOIN text ON content.content_address = text.old_id
WHERE page.page_namespace = 0;
```

However, in my case, content.content_address looks like tt:old_id. So I use SUBSTR to remove the tt: in content.content_address. This is the reason why visualizing your database is important.
```sql
SELECT page.page_title, text.old_text
FROM page
JOIN revision ON page.page_latest = revision.rev_id
JOIN slots ON revision.rev_id = slots.slot_revision_id
JOIN content ON slots.slot_content_id = content.content_id
JOIN text ON CAST(SUBSTR(content.content_address, 4) AS INTEGER) = text.old_id
WHERE page.page_namespace = 0;
```

## Usage 

**Extract MediaWiki pages and Convert to Markdown**:

(I found markdown_github in pandoc fits better than markdown.)
Create a Python script (e.g., convert_wiki_to_markdown.py) with the following code:
```python    
import sqlite3
import subprocess
import os

# Function to convert wikitext to Markdown using Pandoc
def convert_to_markdown(wikitext_content):
    process = subprocess.Popen(['pandoc', '-f', 'mediawiki', '-t', 'markdown_github'], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE)
    markdown_content, _ = process.communicate(input=wikitext_content.encode('utf-8'))
    return markdown_content.decode('utf-8')

# Function to save content to a Markdown file
def save_to_markdown_file(title, content):
    # Replace spaces and other special characters in title for filename
    sanitized_title = title.replace(' ', '_').replace('/', os.sep)
    filename = f"markdown_files{os.sep}{sanitized_title}.md"

    # Create necessary directories
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write content to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Create a SQL connection to your SQLite database
con = sqlite3.connect("your_database.db")
cur = con.cursor()

# Query to join page and revision tables to get page titles and their latest content(Put the correct version query here)
cur.execute("""
    SELECT page.page_title, text.old_text
    FROM page
    JOIN revision ON page.page_latest = revision.rev_id
    JOIN slots ON revision.rev_id = slots.slot_revision_id
    JOIN content ON slots.slot_content_id = content.content_id
    JOIN text ON CAST(SUBSTR(content.content_address, 4) AS INTEGER) = text.old_id
    WHERE page.page_namespace = 0;
""")

# Fetch all results
wiki_pages = cur.fetchall()
special_files = []

# Convert each page's content to Markdown and save to file
for page in wiki_pages:
    title = page[0]
    content_wikitext = page[1]
    # Convert and save the content
    content_markdown = convert_to_markdown(content_wikitext)
    save_to_markdown_file(title, content_markdown)

# Close the connection
con.close()
```
## Drawbacks
The image or pdf files are not converted. TO DO.....

## References

- [MediaWiki Database layout Manual](https://www.mediawiki.org/wiki/Manual:Database_layout)
- [How to know the MediaWiki Version Discussion](https://www.mediawiki.org/wiki/Topic:Pxovvjcr9goluynq)
- [MediaWiki Same Page Title Problem Discussion](https://www.mediawiki.org/wiki/Topic:Qhyh9ku9eom60wz2)
