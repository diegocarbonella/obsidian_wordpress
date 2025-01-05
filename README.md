# Obsidian WordPress image uploader and content poster

Python script to upload markdown files as WordPress posts. 
Use WordPress API to post content and SFTP to upload images to WordPress server.

## Example usage

```
 # The content of the file will be the markdown file content. 
 # The name of the file will be the WordPress post title.
 # Upload post and images.
 python3 main.py --mdp='/home/Last update about NEW features.md' --opt='ui'
 # Upload only post, draft mode, categories.
 python3 main.py --mdp='/home/NEWS about last update.md' --opt='ud' --cat=89,78
```

## Installation

1. Execute ``git clone https://github.com/diegocarbonella/obsidian_wordpress``
2. Install required python modules.
3. Setup environment variables. See example.ENV_VARS.py as an example. The name of the file should be ENV_VARS.py in order to make it work.
4. Execute ``python3 main.py --mdp='/home/MyMarkdownFile.md' --opt='ui'``

## Script execution options

```
Path to markdown file
--mdp='/home/MyMarkdownFile.md'

Upload and processing options. u = upload post, i = upload images sftp, v = verbose, d = draft post
--opt='ui'

Send WordPress categories. Send categories ids.
--cat=8,9
```

## Obsidian markdown file yaml propertis

It is possible to read the yaml [properties](https://help.obsidian.md/Editing+and+formatting/Properties) of the Obsidian markdown files.
- post_id = the WordPress post id. Useful to update content.
- tags = WIP.
- short_description = WIP.
- custom_title = WIP.

## Requirements 

- Python3 
- Access to WordPress API (user and password).
- Optional: SFTP access to server to upload images/files.

## Future improvements

- Bulk upload and sync.
- Upload files using WordPress API. 
- Link to other notes.