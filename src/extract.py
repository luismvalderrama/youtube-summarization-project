import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd

load_dotenv()

G_API_KEY = os.getenv("G_API_KEY")
USERNAME = os.getenv("USERNAME")


def get_channel_id(username_or_url):
    youtube = build("youtube", "v3", developerKey=G_API_KEY)

    # Make the request
    request = youtube.search().list(
        part="snippet", q=username_or_url, type="channel", maxResults=1
    )
    response = request.execute()

    # Extract the channel ID from the response
    if "items" in response and len(response["items"]) > 0:
        channel_id = response["items"][0]["id"]["channelId"]
        print(f"Channel ID: {channel_id}")
        return channel_id
    else:
        print("Channel not found.")
        return None


# Example usage
username_or_url = USERNAME
channel_id = get_channel_id(username_or_url)


def get_uploads_id(channel_id):
    youtube = build("youtube", "v3", developerKey=G_API_KEY)

    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        uploads_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        print(f"The upload ID for all of channel's videos is {uploads_id}.")
        return uploads_id
    else:
        print("Upload ID for channel videos has not been found.")
        return None


upload_id = get_uploads_id(channel_id)


def get_video_ids(upload_id):
    youtube = build("youtube", "v3", developerKey=G_API_KEY)

    request = youtube.playlistItems().list(
        part="contentDetails", maxResults=50, playlistId=upload_id
    )
    response = request.execute()

    video_ids = []

    for i in range(len(response["items"])):
        video_ids.append(response["items"][i]["contentDetails"]["videoId"])

    page_turn_token = response.get("nextPageToken")
    more_pages = True

    while more_pages:
        if page_turn_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="contentDetails",
                maxResults=50,
                playlistId=upload_id,
                pageToken=page_turn_token,
            )
            response = request.execute()

            for i in range(len(response["items"])):
                video_ids.append(response["items"][i]["contentDetails"]["videoId"])

                page_turn_token = response.get("nextPageToken")

    return video_ids


get_video_ids(upload_id)
