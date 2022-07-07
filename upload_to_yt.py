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


video_id, details = upload_to_youtube("file_example_MP3_700KB.mp4", "title", "description", ["tag1", "tag2"], "category")
