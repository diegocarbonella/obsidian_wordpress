# Obsidian WordPress image uploader and content poster

Simple Python script to upload markdown files as WordPress post. 
Using WordPress API to post content and SFTP to upload files to WP server.

## Example usage

``python3 main.py --md_path='/home/MyMarkdownFile.md' --opt='ui'``

## Installation

1. git clone ...
2. Install required python modules.
3. Setup env vars. See example.ENV_VARS.py as an example. The name of the file should be ENV_VARS.py in order to make it work.
4. Execute ``python3 main.py --md_path='/home/MyMarkdownFile.md' --opt='ui'``

## Usage options

--md_path = Path to markdown file
--opt = Upload and processing options. u = upload post, i = upload images sftp

## Requirements 

- Python3 
- Access to WordPress API (user and password).
- Optional: SFTP access to server.

## Future improvements

- Add tags/categories to posts.
- Upload existing content feature.
- Bulk upload and sync.
- Upload files using WordPress API. 