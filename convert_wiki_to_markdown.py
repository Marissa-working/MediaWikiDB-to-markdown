import sqlite3
import subprocess
import os

# Function to convert wikitext to Markdown using Pandoc
def convert_to_markdown(wikitext_content):
    process = subprocess.Popen(['pandoc', '-f', 'mediawiki', '-t', 'markdown'], 
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

# Query to join page and revision tables to get page titles and their latest content
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

