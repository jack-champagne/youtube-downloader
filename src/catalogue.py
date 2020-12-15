import os
import threading
import downloader
import pprint

import youtube_info
import util

# Catalogue manages the list of recently downloaded videos so that we know what is new and what is old
# it also maintains a list of channels that we are "subscribed" to through the bot's inner workings.

# Catalogue checks the web for new videos from channels
def download_new(my_cat):
    videos_to_download = get_new_videos(my_cat)

    os.chdir('downloads')
    # Multi-threaded downloading videos
    threads = []
    for video in videos_to_download:
        full_url = youtube_info.get_full_video_url(video)
        print("Downloading: " + full_url)
        threads.append(threading.Thread(target=downloader.download_video, args=(full_url,)))
        my_cat['Downloaded'].append(video)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    os.chdir('..')
    print('All videos downloaded, back to main menu')


# Precondition: Stable internet connection (lol)
# Return list of new videos from each channel.
def get_new_videos(my_cat):
    chans = my_cat["Channels"]
    videos_to_download = []
    print('Checking for videos from these channels: ', end='')
    pprint.pprint(chans)

    for channel in chans:
        chan_ID = youtube_info.get_channel_uid(channel)
        recent_videos = youtube_info.get_videos(chan_ID)

        most_recent_vid = recent_videos[0][0]

        recently_downloaded = my_cat['Downloaded']
        # Check to see if most recent video is downloaded
        if most_recent_vid not in recently_downloaded:
            videos_to_download.append(most_recent_vid)
        else:
            print('No new videos from: ' + channel)
    return videos_to_download


# ADD channels to check new videos from (subscribe to a channel)
# 
# Returns...
# ["New channel urls", "as a list"]
def add_new_channels():
    new_channels = []
    print('Please enter youtube channel URL you would like to add or press enter to stop')
    response = input()
    while response != '':
        # Clean up dirty inputs
        if response.endswith('/'):
            response = response[:-1]
        if response.endswith('/videos'):
            response = response[:-7]

        new_channels.append(response)
        response = input()
    print('Channel(s) added successfully')
    return new_channels


# Takes in current channels subscribed to and will remove channels according to user input
# 
# Returns...
# New list of current channels
def delete_channel(channels):
    print('Please type channel url you would like to unsubscribe from or press enter to stop')
    chan = None
    while chan not in channels:
        chan = input()
        if chan == '':
            print('Returning to main menu.')
            return channels
        if chan not in channels:
            print('Not found, please try again')
    
    channels.remove(chan)
    print('Channel: ' + chan + ' removed.')
    return channels
        

# Reads file for channels and recently downloaded vids Format:
# Video URLs (CSV)
# Channels URLS (CVS)
# 
# Return format...
# Dictionary {"Channels" : ["Channel urls"], "Downloaded" : ["Video urls"]}
def load_catalogue():
    if not os.path.exists(r'local\my-content.txt'):
        util.create_file('my-content.txt')

    yt_file = open('local\my-content.txt', 'r')
    lines = yt_file.readlines()
    yt_file.close()
    if len(lines) >= 2:
        recently_downloaded = lines[0].replace('\n', '').split(',')
        if '' in recently_downloaded:
            recently_downloaded.remove('')
        channels = lines[1].split(',')
    else:
        yt_file = open('local\my-content.txt', 'w')
        yt_file.write('\n')
        yt_file.close()
        recently_downloaded = []
        channels = []
    return {"Channels" : channels, "Downloaded" : recently_downloaded }


# Takes in my_cat and saves to appropriate file
def save_catalogue(my_cat):
    yt_save = open('local\my-content.txt', 'w+')
    yt_save.write(','.join(my_cat['Downloaded']) + '\n')
    yt_save.write(','.join(my_cat['Channels']))