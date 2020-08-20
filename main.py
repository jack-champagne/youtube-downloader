from pytube import YouTube
import shelve
import pprint
import requests
import bs4
import re

# Define add channels method
def new_channels(chans):
    print('Please enter youtube channel url you would like to add or press enter to stop')
    response = input()
    while response != '':
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
        print('Downloading: ' + yt.title + '\nFrom: ' + channel)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        stream.download('./downloads/')
        # # Name video the title

    # Print total watch time

    # Save shelve
