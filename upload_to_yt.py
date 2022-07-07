# INSTRUCTIONS https://www.youtube.com/watch?v=-zx6odbKMCw
# Generating YouTube API Keys
# 
#     Log into https://console.cloud.google.com
#     Create a new Project
#     Search for “YouTube Data API V3”
#     Click Credentials
#     Click Create Credentials
# 
# For user data: 5. Select OAuth Client ID 6. Select that you will call API from “Web Server” 7. Download or copy your API key from the Credentials tab
# 
# For non-user data 5. Select API Key 6. Paste the key into a file



from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


def upload_to_youtube(video_file, title, description, tags, category):
    channel = Channel()
    channel.login("client_secret.json", "credentials.storage")
    video = LocalVideo(file_path=video_file)
    video.set_title(title)
    video.set_description(description)
    video.set_tags(tags)
    video.set_category(category)
    video.set_default_language("en-US")
    video.set_embeddable(True)
    video.set_public_stats_viewable(True)
    video = channel.upload_video(video)
    return video.id, video

# example usage
video_file = "file_example.mp4"
title = "Title"
description = "Description"
tags = ['tag1','tag2','ect']
category = "gaming"
video_id, details = upload_to_youtube( video_file, title, description, tags, category)
print(video_id)
print(details)

