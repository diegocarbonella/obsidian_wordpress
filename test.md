---
tags:
  - Drupal
post_id: "-1191"
---

# H1 Title
## H2 Title
### H3 Title
#### H4 Title
##### H5 Title
###### H6 Title

---

# Code block (indentation)

    def replace_with_img_tag(match):

        filedata = markdown.markdown(raw_markdown_no_yaml)
        filedata = markdown.markdown(filedata, extensions=['fenced_code','attr_list'])
        pattern = r'!\[\[(.*?)\]\]'
        updated_content = re.sub(pattern, replace_with_img_tag, filedata)

        return {
            "post_id" : post_id,
            "processed_markdown" : updated_content,
            "raw_markdown" : raw_markdown,
            "tags" : tags_array,
        }

    def sendPost(postData):
        url = mainurl + "/wp-json/wp/v2/posts" 
        if postData["post_id"] > -1:
            url = mainurl + "/wp-json/wp/v2/posts/" + str(postData["post_id"])
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            json=postData
        )
        return response

# Code block (backticks)

```python
    def replace_with_img_tag(match): 
        filename = match.group(1)  # Extract the filename from the match 
        return f'<img src="{wordpress_path}{filename}"/>'
```

Normal text *strong text* and _italic_ text.