import re
import os

def process_markdown_file(file_path):
    # Define a regular expression pattern to match `\` at the end of a line
    pattern = re.compile(r'\\\s*\n')

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()
    
    # Replace `\` at the end of a line with a new line
    cleaned_content = pattern.sub('<br>', original_content)
    
    # Print out the changes
    if original_content != cleaned_content:
        print(f'Changes in file: {file_path}')
        # Split content into lines for better readability
        original_lines = original_content.splitlines()
        cleaned_lines = cleaned_content.splitlines()
        
        for i, (orig_line, clean_line) in enumerate(zip(original_lines, cleaned_lines)):
            if orig_line != clean_line:
                print(f'Line {i+1}:')
                print(f'  Original: {orig_line}')
                print(f'  Modified: {clean_line}')
        # Handle extra lines if the cleaned content is longer
        if len(cleaned_lines) > len(original_lines):
            for i, clean_line in enumerate(cleaned_lines[len(original_lines):], start=len(original_lines)):
                print(f'Line {i+1}:')
                print(f'  Added: {clean_line}')
        print()  # New line for separation

    # Write the cleaned content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def process_markdown_files(directory):
    # Walk through all directories and files starting from the specified directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                process_markdown_file(file_path)

# Specify the directory containing your Markdown files
directory = './markdown_files'
process_markdown_files(directory)
