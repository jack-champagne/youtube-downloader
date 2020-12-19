import sys
import catalogue
import downloader
import os

# Pretty gross main method imo
def start():
    # Local folder contains configuration and save information
    if not os.path.exists('local'):
        os.mkdir('local')
    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    my_catalogue = catalogue.load_catalogue()
    my_stats = downloader.load_stats()

    if (len(sys.argv) == 2):
        if (sys.argv[1] == 'auto'):
            catalogue.download_new(my_catalogue)
            catalogue.save_catalogue(my_catalogue)
            downloader.save_stats(my_stats)
            exit(0)

    print(
        '''========= Welcome to Youtube-Downloader ==========
        Here are your stats
        * Total Watchtime = %d minutes
        * Total Videos = %d videos''' % (my_stats.get('Watchtime') / 60.0, my_stats.get('Videos'))
    )
    new_page()

    display_menu(my_catalogue)
    
    catalogue.save_catalogue(my_catalogue)
    downloader.save_stats(my_stats)

def display_menu(my_cat):
    # Ask for input
    running = True
    while running:

        # Print user menu options
        print(
        '''\tPlease select an option:
        * [A]dd channels
        * [D]ownload recent videos
        * [R]emove channels
        * [C]lear video catalogue
        * [V]iew channels
        * [Q]uit''')

        response = input()
        new_page()
        if response in ['r', 'R']:
            my_cat['Channels'] = catalogue.delete_channel(my_cat['Channels'])

        elif response in ['c', 'C']:
            my_cat['Downloaded'] = []
            print("Downloaded videos cleared!")

        elif response in ['q', 'Q']:
            print("Goodbye!")
            running = False

        elif response in ['d', 'D']:
            catalogue.download_new(my_cat)

        elif response in ['a', 'A']:
            my_cat['Channels'] += catalogue.add_new_channels()

        elif response in ['v', 'V']:
            print('SUBSCRIBED CHANNELS:\n')

            if len(my_cat['Channels']) != 0:
                print('\n'.join(my_cat['Channels']))
            else:
                print('No channels found!')

        elif response in ['p', 'P']:
            print('PAUSED')

        elif response in  ['s', 'S']:
            print(downloader.get_stats())

        else:
            print('Invalid Input: ' + response)

        new_page()


def new_page():
    print('==================================================')

start()