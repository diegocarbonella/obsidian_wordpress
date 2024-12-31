# Obsidian WordPress image uploader and content poster

Simple Python script to upload markdown files as WordPress post. 
Using WordPress API to post content and SFTP to upload files to WP server.

## Example usage

``python3 main.py --mdp='/home/MyMarkdownFile.md' --opt='ui'``

## Installation

1. Execute ``git clone https://github.com/diegocarbonella/obsidian_wordpress``
2. Install required python modules.
3. Setup env vars. See example.ENV_VARS.py as an example. The name of the file should be ENV_VARS.py in order to make it work.
4. Execute ``python3 main.py --mdp='/home/MyMarkdownFile.md' --opt='ui'``

## Usage options

```
Path to markdown file
--mdp='/home/MyMarkdownFile.md'

Upload and processing options. u = upload post, i = upload images sftp, v = verbose
--opt='ui'
```

## Requirements 

- Python3 
- Access to WordPress API (user and password).
- Optional: SFTP access to server.

## Future improvements

- Add tags/categories to posts.
- Upload existing content feature.
- Bulk upload and sync.
- Upload files using WordPress API. 