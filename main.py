import pysftp
from urllib.parse import urlparse
import os
import re
import argparse
import markdown
import requests
import json
import re
import yaml
from requests.auth import HTTPBasicAuth
from pathlib import Path
from urllib.parse import urlparse
from ENV_VARS import *

def get_filenames(md_file):

    with open(md_file, 'r') as file:
        filedata = file.read()

    pattern = r'!\[\[(.*?)\.png\]\]'

    # Find all image names in the file
    image_names = re.findall(pattern, filedata)

    arr = []

    for image_name in image_names:
        full_image_name = image_name
        arr.append(full_image_name)

    return arr


class Sftp:
    def __init__(self, hostname, username, password, port=22):
        """Constructor Method"""
        # Set connection object to None (initial value)
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""

        try:
            # Get the sftp connection object
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {self.hostname} as {self.username}.")

    def disconnect(self):
        """Closes the sftp connection"""
        self.connection.close()
        print(f"Disconnected from host {self.hostname}")

    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            print(
                f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]"
            )

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            self.connection.get(remote_path, target_local_path)
            print("download completed")

        except Exception as err:
            raise Exception(err)

    def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            print(
                f"uploading to {self.hostname} as {self.username} [(remote path: {remote_path});(source local path: {source_local_path})]"
            )

            # Download file from SFTP
            self.connection.put(source_local_path, remote_path)
            print("upload completed")

        except Exception as err:
            raise Exception(err)


# Function to generate the replacement HTML
def replace_with_img_tag(match):
    filename = match.group(1)  # Extract the filename from the match
    return f'<img src="{wordpress_path}{filename}"/>'


def processMarkdown(mdp):

    with open(mdp, 'r') as file:
        raw_markdown = file.read()
    
    yaml_pattern = r'^---\n(.*?)\n---'  # Regex to capture everything between '---' lines
    match = re.search(yaml_pattern, raw_markdown, re.DOTALL)
    raw_markdown_no_yaml = re.sub(yaml_pattern, '', raw_markdown, flags=re.DOTALL)
    post_id = -1
    tags_array = []

    if match:
        yaml_data = yaml.safe_load(match.group(1))
        tags_array = yaml_data.get('tags', [])
        post_id = yaml_data.get('post_id', '-1')
        try:
            post_id = int(post_id)
        except ValueError:
            raise Exception("post_id should be integer.") 
    else:
        print("No YAML front matter found in the file.")

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

    # Make the POST request
    response = requests.post(
        url,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
        json=postData  # Automatically converts the dictionary to JSON
    )

    return response


def sftpupload(mdp):

    parsed_url = urlparse(SFTPTOGO_URL)

    sftp = Sftp(
        hostname=parsed_url.hostname,
        username=parsed_url.username,
        password=parsed_url.password,
    )

    # Connect to SFTP
    sftp.connect()

    arr = get_filenames(mdp)

    for image_name2 in arr:
        local_path = images_path + f"{image_name2}.png"
        remote_path_file = remote_path + f"{image_name2}.png"
        sftp.upload(local_path, remote_path_file)

    # Lists files of SFTP location after upload
    #print(f"List of files at location {remote_path}:")
    #print([f for f in sftp.listdir(remote_path)])

    # Download files from SFTP
    #sftp.download(remote_path, os.path.join(remote_path, local_path + '.backup'))

    # Disconnect from SFTP
    sftp.disconnect()

################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

def main():

    parser = argparse.ArgumentParser(description="Process some paths.")
    parser.add_argument('--mdp', type=str, help="Path to the markdown file.")
    parser.add_argument('--opt', type=str, help="Options: u = upload post, i = upload images, d = draft.")
    parser.add_argument('--cat', type=str, help="Post Categories.")
    args = parser.parse_args()

    mdp = args.mdp
    opt = args.opt
    cat = args.cat
    UPLOAD_POST = False
    UPLOAD_IMAGES = False
    VERBOSE = False
    STATUS = 'publish'
    CATEGORIES = []

    if mdp == None:
        print('Please provide a valid path.')
        return

    if opt == None:
        print('Please provide options.')
        return

    if cat != None:
        CATEGORIES = list(map(int, cat.split(',')))

    if opt.find("u") > -1:
        UPLOAD_POST = True

    if opt.find("i") > -1:
        UPLOAD_IMAGES = True

    if opt.find("v") > -1:
        VERBOSE = True

    if opt.find("d") > -1:
        STATUS = 'draft'

    if UPLOAD_POST:
        print("Uploading post...")
        content = processMarkdown(mdp)
        title = Path(mdp).stem

        postData = {
            "content": content["processed_markdown"],
            "title" : title,
            "slug" : title,
            "status" : STATUS,
            "categories" : CATEGORIES,
            "post_id" : content["post_id"] 
        }

        response = sendPost(postData)
        responseData = json.loads(response.text)

        if response.status_code == 200 or response.status_code == 201:
            print("Post updated successfully!")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    if UPLOAD_IMAGES:
        print("Uploading images...")
        sftpupload(mdp)

    print("Finish script.")

mdp = ''
main()