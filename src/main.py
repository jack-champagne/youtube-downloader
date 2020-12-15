import sys
import catalogue
import downloader
import os

# Pretty gross main method imo
def start():
    # Local folder contains configuration and save information
    if not os.path.exists('local'):
        os.mkdir('local')

    my_catalogue = catalogue.load_catalogue()
    my_stats = downloader.load_stats()

    # TODO: Reimplement after rewrite.
    if (len(sys.argv) == 2):
        if (sys.argv[1] == 'auto'):
            catalogue.download_new(my_catalogue)
            exit(0)

    print(
        '''==== Welcome to Youtube-Downloader ====
        Here are your stats
        * Total Watchtime = %d minutes
        * Total Videos = %d videos''' % (my_stats.get('Watchtime'), my_stats.get('Videos'))
    )
    print('=======================================')

    display_menu(my_catalogue)

    
    catalogue.save_catalogue(my_catalogue)
    downloader.save_stats(my_stats)

def display_menu(my_cat):
    # Ask for input
    running = True
    while running:

        # Print user menu options
        print(
        r'''Please select an option:
        [A]dd channels
        [D]ownload recent videos
        [R]emove channels
        [C]lear video catalogue
        [V]iew channels
        [Q]uit''')

        response = input()
        if response in ['r', 'R']:
            my_cat['Channels'] = catalogue.delete_channel(my_cat['Channels'])

        elif response in ['c', 'C']:
            my_cat['Downloaded'] = []

        elif response in ['q', 'Q']:
            running = False

        elif response in ['d', 'D']:
            catalogue.download_new(my_cat)

        elif response in ['a', 'A']:
            if len(my_cat['Channels']) != 0:
                my_cat['Channels'].append(catalogue.add_new_channels())
            else:
                my_cat['Channels'] = catalogue.add_new_channels()

        elif response in ['v', 'V']:
            if len(my_cat['Channels']) != 0:
                print(my_cat['Channels'])
            else:
                print('No channels found!')

        elif response in ['p', 'P']:
            print('PAUSED')

        elif response in  ['s', 'S']:
            print(downloader.get_stats())

        else:
            continue

start()