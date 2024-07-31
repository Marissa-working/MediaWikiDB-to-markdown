import re
import os

def remove_section_ids(file_path):
    # Define a regular expression pattern to match section IDs
    pattern = re.compile(r'\{#.*?\}')
    
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all section IDs to be removed
    section_ids = pattern.findall(content)
    
    # Print out the section IDs that will be removed
    if section_ids:
        print(f'Found section IDs in file {file_path}:')
        for section_id in section_ids:
            print(f'  {section_id}')
    
    # Remove section IDs
    cleaned_content = re.sub(pattern, '', content)
    
    # Write the cleaned content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def process_markdown_files(directory):
    # Walk through all directories and files starting from the specified directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            #print(filename)
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                remove_section_ids(file_path)

# Specify the directory containing your Markdown files
directory = './markdown_files'
process_markdown_files(directory)
