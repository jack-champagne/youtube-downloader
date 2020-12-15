import sys
import catalogue
import downloader
import os
import pprint

# Pretty gross main method imo
def start():
    # Local folder contains configuration and save information
    if not os.path.exists('local'):
        os.mkdir('local')
    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    my_catalogue = catalogue.load_catalogue()
    my_stats = downloader.load_stats()

    # TODO: Reimplement after rewrite.
    if (len(sys.argv) == 2):
        if (sys.argv[1] == 'auto'):
            catalogue.download_new(my_catalogue)
            exit(0)

    print(
        '''========= Welcome to Youtube-Downloader ==========
        Here are your stats
        * Total Watchtime = %d minutes
        * Total Videos = %d videos''' % (my_stats.get('Watchtime'), my_stats.get('Videos'))
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
        if response in ['r', 'R']:
            new_page()
            my_cat['Channels'] = catalogue.delete_channel(my_cat['Channels'])
            new_page()

        elif response in ['c', 'C']:
            new_page()
            my_cat['Downloaded'] = []
            print("Downloaded videos cleared!")
            new_page()

        elif response in ['q', 'Q']:
            new_page()
            print("Goodbye!")
            running = False

        elif response in ['d', 'D']:
            new_page()
            catalogue.download_new(my_cat)
            new_page()

        elif response in ['a', 'A']:
            new_page()
            my_cat['Channels'] += catalogue.add_new_channels()
            new_page()

        elif response in ['v', 'V']:
            new_page()
            print('SUBSCRIBED CHANNELS:\n')

            if len(my_cat['Channels']) != 0:
                print('\n'.join(my_cat['Channels']))
            else:
                print('No channels found!')
            new_page()

        elif response in ['p', 'P']:
            print('PAUSED')

        elif response in  ['s', 'S']:
            print(downloader.get_stats())

        else:
            new_page()
            print('Invalid Input: ' + response)
            new_page()
        

def new_page():
    print('==================================================')

start()