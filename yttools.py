# yttools.py
from dotenv import load_dotenv
load_dotenv()
import os
from googleapiclient.discovery import build


def search_youtube(query: str) -> str:
    """Search YouTube for videos matching a query and return candidate results.
    Use this first to find videos. Returns a numbered list where each line has the video's title, channel, its video_id, and its URL.
    Pass a video_id to get_video_stats to look up that video's view count and other statistics.

    Args:
        query: what to search for, e.g. "Machine learning tutorials".
    """
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"), static_discovery=True)
    request = youtube.search().list(
        part="snippet", q=query, maxResults=5, type="video"
    )
    response = request.execute()

    lines = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"].replace("&amp;", "&")
        channel = item["snippet"]["channelTitle"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        lines.append(
            f"- {title} | channel: {channel} | video_id: {video_id} | url: {url}"
        )
    return "Search results: \n" + "\n".join(lines)


def get_video_stats(video_id: str) -> str:
    """Return view count, like count, and publish date for a single YouTube video.

    Use this after search_youtube, passing a video_id from its results, to look up how popular a specific video is.

    Args:
        video_id: the ID of one video, e.g. "kqtD5dpn9C8".
    """
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"), static_discovery=True)
    request = youtube.videos().list(
        part="snippet,statistics", id=video_id
    )
    response = request.execute()

    if not response["items"]:
        return f"No video found with id '{video_id}'."

    item = response["items"][0]
    title = item["snippet"]["title"].replace("&amp;", "&")
    published = item["snippet"]["publishedAt"][:10]
    views = item["statistics"].get("viewCount", "unavailable")
    likes = item["statistics"].get("likeCount", "unavailable")
    url = f"https://www.youtube.com/watch?v={video_id}"

    return (
        f"'{title}' | views: {views} | likes: {likes} | "
        f"published: {published} | url: {url}"
    )


def compare_videos(video_ids: list[str]) -> str:
    """Compare several YouTube videos side by side on views, likes, and engagement.

    Use this when the user wants to compare multiple videos or find what several top videos have in common. Pass a list of video_ids from search_youtube.
    Returns a structured comparison including a like-to-view engagement ratio for each video.

    Args:
        video_ids: a list of video IDs, e.g. ["kqtD5dpn9C8", "_uQrJ0TkZlc"].
    """
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"), static_discovery=True)
    request = youtube.videos().list(
        part="snippet,statistics", id=",".join(video_ids)
    )
    response = request.execute()

    if not response["items"]:
        return "No videos found for the given IDs."

    lines = ["Comparison: "]
    for item in response["items"]:
        title = item["snippet"]["title"].replace("&amp;", "&")
        channel = item["snippet"]["channelTitle"]
        published = item["snippet"]["publishedAt"][:10]
        views = int(item["statistics"].get("viewCount", 0))
        likes = int(item["statistics"].get("likeCount", 0))
        ratio = (likes / views * 100) if views else 0
        url = f"https://www.youtube.com/watch?v={item['id']}"
        lines.append(
            f"- {title} | channel: {channel} | views: {views} | likes: {likes} | "
            f"engagement ratio: {ratio:.2f}% | published: {published} | url: {url}"
        )
    return "\n".join(lines)