import logging

import azure.functions as func

from github import Github
from github import RateLimit
from datetime import datetime
import sys
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import yaml
import pandas as pd
with open("config.yaml") as f:
    config = yaml.safe_load(f)
# We need to use some type of service account for the github
my_github_credential = config["key"]

g = Github(my_github_credential, per_page = 100) #100 is maximum

todaymd = datetime.today().strftime('%m%d')

# If no argument listed for file name, use Tags_Search_Terms.txt
topic_file=config["topic_file"]

readFile = open(topic_file, 'r')

# Data files will automatically be put in the 'DateExtracts' Folder
print ("date\ttopic\trepo\tstars\twatchers\tforks\tissues")

lines = readFile.readlines()

container_client = ContainerClient.from_connection_string(config["connection_string"], config["container_name"])
for line in lines:
    term = line.strip()
    file_name= term + 'Extract' + todaymd + '.csv' #modify to go to blob storage

    
    outFile_df = pd.DataFrame(columns = ['date','repo','stars','watchers','forks','issues'])
    repositories = g.search_repositories(query="%s stars:>=2000" % term)
    
    for repo in repositories:
        stars=repo.stargazers_count
        forks=repo.forks_count
        watchers=repo.watchers_count
        open_issues=repo.open_issues_count
    
        append_line = [datetime.today().strftime('%Y-%m-%d'), repo.full_name, stars, watchers, forks, open_issues]
        outFile_df.loc[len(outFile_df)]=append_line
    
    outFile_df.to_csv(file_name, index = False)

    blob_client = container_client.get_blob_client(file_name)
    with open(file_name, "rb") as data:
        blob_client.upload_blob(data)
        os.remove(file_name)
    #outFile.close()
    
#readFile.close()