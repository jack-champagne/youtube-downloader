import bs4
import requests
import xmltodict

# Simple file that get important information that can identify specific channels or videos

# This gets the UID of a channel by its homepage URL and returns the channel ID
def get_channel_uid(channel):
    page = requests.get(channel)
    page.raise_for_status()
    p_soup = bs4.BeautifulSoup(page.text, features="html.parser")
    uid_tag = p_soup.select('meta[itemProp="channelId"]')[0]
    return uid_tag.get('content')

# Precondition: channel_uid must be a valid channel ID on youtube
# This returns a list of videos urls from a channel in the form ('video_url', 'title')
def get_videos(channel_uid):
    feed_url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_uid
    page = requests.get(feed_url)
    entries = xmltodict.parse(page.content)['feed']['entry']
    videos = []
    for entry in entries:
        videos.append((entry['yt:videoId'], entry['title']))
    return videos

def get_full_video_url(video_id):
    return 'https://www.youtube.com/watch?v=' + video_id

