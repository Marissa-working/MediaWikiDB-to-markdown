import sqlite3
import pandas as pd
import os
import shutil

con = sqlite3.connect("wiki.sqlite")
df = pd.read_sql_query("""
    SELECT page.page_title, cl_type, cl_to, cl_from
    FROM categorylinks
    JOIN page ON page.page_id = categorylinks.cl_from
""", con)
con.close()

# Define the root directory where Markdown files will be organized
source_directory = './markdown'
target_directory = './markdown'

# Function to create directories and move files
def organize_files(df, source_dir, target_dir):
    def process_node(node_df, current_path):
        for _, row in node_df.iterrows():
            cl_type = row['cl_type']
            cl_from = row['cl_from']
            page_title = row['page_title']
            
            if cl_type == 'subcat':
                # if the subcatalog is itself
                if page_title == os.path.basename(current_path):
                    continue
                if df[df['cl_to'] == page_title].empty:
                    continue
                # Create a directory for the subcategory
                subcat_dir = os.path.join(current_path, page_title.replace(' ', '_').replace('/', '.'))
                os.makedirs(subcat_dir, exist_ok=True)
                
                # Process subcategories and pages
                subcat_df = df[df['cl_to'] == page_title]
                process_node(subcat_df, subcat_dir)
            
        for _, row in node_df.iterrows():
            cl_type = row['cl_type']
            page_title = row['page_title']

            if cl_type == 'page':
                new_page_title = page_title.replace(' ', '_').replace('/', '.')
                src_file = os.path.join(source_dir, f"{new_page_title}.md")
                dst_file = os.path.join(current_path, f"{new_page_title}.md")
                
                if os.path.exists(src_file):
                    shutil.move(src_file, dst_file)
                else:
                    print(f"File {src_file} not found, should be in {dst_file}")

    # Start processing from the root category
    root_df = df[df["cl_to"] == 'Category_Root']
    process_node(root_df, os.path.join(target_dir, 'Category_Root'))

# Organize the files based on the DataFrame
organize_files(df, source_directory, target_directory)
