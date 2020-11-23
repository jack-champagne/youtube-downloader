import youtube_dl
import threading
import util
import os
# Downloader contains a list of functions associated with downloading videos and settings for such.

# Globals
videos_downloaded_today = 0
watchtime_today = 0
lock = threading.Lock()

total_watchtime = 0
total_videos = 0

# Preconditions: URL must be a valid youtube video URL
# Downloads youtube video at specified url and increments videos_downloaded and updates watchtime_today
def download_video(video_url):
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        length = ydl.extract_info(video_url).get('duration')
    lock.acquire()
    global videos_downloaded_today
    global watchtime_today
    videos_downloaded_today += 1
    watchtime_today += length
    lock.release()

def save_stats(my_stats):
    stats = open('local\youtube-stats.txt', 'w+')
    stats.write(str(my_stats['Watchtime'] + watchtime_today) + '\n')
    stats.write(str(my_stats['Videos'] + videos_downloaded_today))

# The stats file is formatted as so:
# Total Watchtime
# Videos Downloaded
#
# Return format...
# {"Watchtime" : int watchtime, "Videos" : int videos}
def load_stats():
    if not os.path.exists('local\youtube-stats.txt'):
        util.create_file('youtube-stats.txt')

    stat_file = open('local\youtube-stats.txt', 'r')
    lines = stat_file.readlines()
    stat_file.close()
    if len(lines) >= 2:
        total_watchtime = int(lines[0])
        total_videos = int(lines[1])
    else:
        stat_file = open('local\youtube-stats.txt', 'w+')
        stat_file.write('\n')
        stat_file.close()
        total_watchtime = 0
        total_videos = 0
    return {"Watchtime" : total_watchtime, "Videos" : total_videos }

# Returns a string displaying all of the youtube downloaded stats :)
def get_stats():
    stat_string = 'Today (watchtime, # of videos) = (' + str(util.get_watchtime(watchtime_today)) + ', ' + str(videos_downloaded_today) + ' videos)'
    return stat_string