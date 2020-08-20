from pytube import YouTube
import shelve
import pprint
import requests
import re

# Define add channels method
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

## END FUNCTIONS --BEGIN BODY

# Load current list of youtubers
with shelve.open('my-content') as db:
    channels = db.get('channels')
    if channels == None:
        channels = []
    recent_videos = db.get('recent')
    if recent_videos == None:
        recent_videos = []

# Ask for any youtuber recommendations to add to download list
    print('Would you like to add any youtubers to the watchlist? (y/n)')

    valid_input = False
    while not valid_input:
        response = input()
        if response in ['y', 'Y']:
            valid_input = True
            new_channels(channels)
            continue
        if response in ['n', 'N']:
            valid_input = True
            continue
        else:
            valid_input = False
            print('Please enter a valid key.')

# Save new youtubers to shelve
    db['channels'] = channels


# Check each youtuber for newest video 
    print('Ok, checking for new videos for:')
    pprint.pprint(channels)  

    url_regex = re.compile(r'("commandMetadata":{"webCommandMetadata":{"url":"(\/watch\?v=.+?)"{1})')

    local_watchtime = 0
    videos_downloaded = 0
    for channel in channels:

        page = requests.get(channel + '/videos') # Get current list of videos
        page.raise_for_status()
        matched_vid = url_regex.search(page.text)
        new_vid_url = "https://www.youtube.com" + matched_vid.group(2)

        # Check to see if video has not been downloaded
        if new_vid_url not in recent_videos:
            recent_videos.append(new_vid_url)
        else:
            print('No new videos from: ' + channel)
            continue
    
        # Download video
        yt = YouTube(new_vid_url)
        print('Downloading: ' + yt.title + '\nFrom: ' + yt.author)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        stream.download('./downloads/')
        print('Download successful.')

        print('Added ' + str(yt.length) + ' seconds to downloaded videos today')
        local_watchtime += yt.length
        videos_downloaded += 1

    # Print total watch time
    print('Done downloading ' + str(videos_downloaded) + ' video(s).')
    total_watchtime = db.get('watchtime')
    if total_watchtime == None:
        total_watchtime = 0
    total_watchtime += local_watchtime

    # Get minutes and seconds for display
    mins = total_watchtime // 60
    seconds = total_watchtime % 60
    sec_str = ''
    if seconds < 10:
        sec_str = '0' + str(seconds)
    else:
        sec_str = str(seconds)
    print('Total video watchtime: ' + str(mins) + ":" + sec_str)

    # Save shelve
    db['watchtime'] = total_watchtime
    db['channels'] = channels
    db['recent'] = recent_videos

    print('Video profile saved. Goodbye')
    exit(0)