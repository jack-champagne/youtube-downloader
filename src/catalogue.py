"""
Catalogue manages the list of recently downloaded videos so that we know what is new and what is old
it also maintains a list of channels that we are "subscribed" to through the bot's inner workings.

author: Jack Champagne
date: 12/19/2020
"""

import os
import threading
import downloader
import pprint

import youtube_info
import util

# Function: download_new
# Arguments: Youtube catalogue --> {"Videos" : [<List of recent videos>], "Channels":[<List of subscribed channels]}
# 
# Overview:
# * We retrieve a list of *new* videos by checking each channel's feed and comparing against previously downloaded videos
# * For each *new* video we want to download it by creating a thread to handle the video download, the way the download happens concurrently
# Done!
# 
# Prequisties:
# * Stable internet connection
# * Directory "downloads" exists in the current directory
# * my_cat is a valid Youtube Catalogue
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


# Function: get_new_videos
# Arguments: Youtube catalogue --> {"Videos" : [<List of recent videos>], "Channels":[<List of subscribed channels]}
# 
# Overview:
# * We retrieve a list of subsribed channels to read each one's feed.
# * We check that most recent video from a channel's feed is not already downloaded.
# * Return list of videos that have not been downloaded yet from respective channels
# 
# Prequisties:
# * Stable internet connection
# * my_cat is a valid Youtube Catalogue
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


# Function: add_new_channels
# Arguments: None
# 
# Overview:
# * Handle and clean user input for slightly different urls to make it easier to understand the local file(s) and stats.
# * Keep adding channels until user hits enter twice in a row.
# 
# Prequisties:
# * None
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


# Function: delete_channels
# Arguments: current channel list from Youtube Catalogue
# 
# Overview:
# * "Unsubscribe" from unwanted channels by typing out the url of the channel to be deleted
# * Can be cancelled by pressing enter
# * Handles if given channel is not a valid subscribed channel
# 
# Prequisties:
# * channels is a correct channel list
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
        

# Function: load_catalogue
# Arguments: None
# 
# Overview:
# * Loads in local/my-content.txt for reading
# * Gets list of already downloaded videos from first line (comma separated)
# * Gets list of subscribed channels from second line
# * If file has not been formatted yet, create the format by creating a linefeed and creating empty lists for catalogue
# 
# Prequisties:
# * local directory exists
# * my-content.txt is not being used by another process
# * contents of my-content.txt is properly formatted (2 lines, both comma separated)
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


# Function: save_catalogue
# Arguments: Youtube catalogue to save
# 
# Overview:
# * Opens local\my-content and writes downloaded videos and subsribed channels to their respective lines (comma separated)
# 
# Prequisties:
# * local\my-content.txt exists
# * local\my-content.txt is not being used by another process.
def save_catalogue(my_cat):
    yt_save = open('local\my-content.txt', 'w+')
    yt_save.write(','.join(my_cat['Downloaded']) + '\n')
    yt_save.write(','.join(my_cat['Channels']))