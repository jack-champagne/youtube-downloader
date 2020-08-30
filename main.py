import shelve
import pprint
import requests
import re
import youtube_dl
import threading
import os
import sys

def download(video_url):
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        length = ydl.extract_info(video_url).get('duration')
    lock.acquire()
    global videos_downloaded
    videos_downloaded += 1
    global today_watchtime
    today_watchtime += length
    recent_videos.append(video_url)
    print('Finished downloading ' + str(videos_downloaded))
    lock.release()


def new_channels(chans):
    print('Please enter youtube channel url you would like to add or press enter to stop')
    response = input()
    while response != '':
        # Clean up dirty inputs
        if response.endswith('/'):
            response = response[:-1]
        if response.endswith('/videos'):
            response = response[:-7]

        chans.append(response)
        response = input()

    print('Channel(s) added successfully')
    return chans
# Fix this method so that it is clearer


def refresh_catalogue():
    videos_to_download = check_for_new_videos()

    # Multi-thread downloads videos
    threads = []
    for video in videos_to_download:
        print('Generating ' + video + ' thread')
        threads.append(threading.Thread(target=download, args=(video,)))
    print('Starting dl threads')
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    print('Killed dl threads')
    

# Returns list of youtubers with new videos
def check_for_new_videos():
    videos_to_download = []
    print('Ok, checking for new videos for:')
    pprint.pprint(channels)
    url_regex = re.compile(r'("commandMetadata":{"webCommandMetadata":{"url":"(\/watch\?v=.+?)"{1})')
    for channel in channels:
        page = requests.get(channel + '/videos')  # Get current list of videos
        page.raise_for_status()
        matched_vid = url_regex.search(page.text)
        new_vid_url = "https://www.youtube.com" + matched_vid.group(2)
        # Check to see if video has not been downloaded
        global recent_videos
        if new_vid_url not in recent_videos:
            videos_to_download.append(new_vid_url)
        else:
            print('No new videos from: ' + channel)
    print('Downloading videos from these channels:')
    pprint.pprint(videos_to_download)
    return videos_to_download


def get_watchtime(watchtime_s):
    seconds = watchtime_s % 60
    watchtime_s //= 60
    minutes = watchtime_s % 60
    watchtime_s //= 60
    hours = watchtime_s % 24
    watchtime_s //= 24
    days = watchtime_s
    return str(days) + ' days ' + str(hours) + ':' + str(minutes) + ':' + str(seconds)


def main():
    if (len(sys.argv) == 2):
        if (sys.argv[1] == 'auto'):
            refresh_catalogue()
            exit
    # Load database info
    ytdb = shelve.open('my-content')
    global channels
    channels = ytdb.get('channels')
    if channels is None:
        channels = []
    global recent_videos
    recent_videos = ytdb.get('recent')
    if recent_videos is None:
        recent_videos = []
    pprint.pprint(recent_videos)
    global watchtime
    watchtime = ytdb.get('watchtime')
    if watchtime is None:
        watchtime = 0

    # Print current channels
    print('List of current channels:', end='')
    pprint.pprint(channels)

    # Ask for input
    valid_input = False
    while not valid_input:
        print(r'''Please select an option:
    [A]dd youtubers
    [D]ownload recent videos
    [R]emove youtubers
    [C]lear recent video database
    [Q]uit''')
        response = input()
        if response in ['r', 'R']:
            print('Removing youtubers')
            name = input()
            if name in channels:
                channels.remove(name)
                ytdb['channels'] = channels

        elif response in ['c', 'C']:
            recent_videos = []

        elif response in ['q', 'Q']:
            valid_input = True
            print('Youtubers saved, goodbye.')

        elif response in ['d', 'D']:
            refresh_catalogue()

        elif response in ['a', 'A']:
            channels = new_channels(channels) # Kind of ugly ngl. It appends within the function
            ytdb['channels'] = channels

        else:
            valid_input = False
            print("Please enter a valid key")
    ytdb['channels'] = channels
    ytdb['recent'] = recent_videos
    global videos_downloaded
    print(str(videos_downloaded) + ' video(s) downloaded today.')
    global today_watchtime
    print('Downloaded today: ' + get_watchtime(today_watchtime))
    watchtime += today_watchtime
    print('Total watchtime: ' + get_watchtime(watchtime))
    ytdb['watchtime'] = watchtime
    print('Video profile saved. Goodbye')


today_watchtime = 0
channels = []
recent_videos = []
watchtime = 0
videos_downloaded = 0
lock = threading.Lock()
if not os.path.isdir('downloads'):
    os.mkdir('downloads')

os.chdir('downloads')
if __name__ == '__main__':
    main()
