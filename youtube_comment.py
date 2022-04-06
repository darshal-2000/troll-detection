# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import googleapiclient.discovery
import requests

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "Youtube developer key"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=10,
        order="relevance",
        videoId="j1kINK_Vx_M"
    )
    response = request.execute()

    print(type(response))

    '''json_object = json.dumps(response, indent=4)'''
    '''print(json_object)'''

    URL='http://127.0.0.1:5000/istroll'

    for i in response.get('items'):
        PARAMS = {'comment' : i.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')}
        r = requests.get(url=URL, params=PARAMS)
        print(r.json())

if __name__ == "__main__":
    main()
