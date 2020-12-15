# Takes a watchtime in seconds and returns a formatted string
def get_watchtime(watchtime_s):
    seconds = watchtime_s % 60
    watchtime_s //= 60
    minutes = watchtime_s % 60
    watchtime_s //= 60
    hours = watchtime_s % 24
    watchtime_s //= 24
    days = watchtime_s
    return str(days) + ' days ' + '{:02}'.format(hours) + ':' + '{:02}'.format(minutes) + ':' + '{:02}'.format(seconds)

# Creates a file in the local dir
def create_file(filename):
    file = open('local\\' + filename, 'w+')
    file.close()