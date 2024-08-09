import glob
import os
import allin1
import pandas as pd

from Song_Scheduling.GA_schedular import GA_schedule
from Song_Scheduling.LP_schedular import LP_sched
from Utils.key_detection import find_key
# from Utils.transition import mix_songs
from Initial_Research.transition_test import mix_songs


SONGLIST = "Test_songs"

# class Song:
#     def __init__(self, order, path, artist, bpm, key):
#         self.order = order
#         self.path = path
#         self.artist = artist
#         self.bpm = bpm
#         self.key = key

#     def __repr__(self):
#         return f"Order: {self.order}, Path: {self.path}, BPM: {self.bpm}, Key: {self.key}"


def main():

    # Getting songs from a given directory
    mp3_files = sorted(glob.glob(os.path.join(SONGLIST, '*.mp3')))

    print(sorted(mp3_files))

    # Running allin1 on each song to obtain song info
    song_info = allin1.analyze(mp3_files,  out_dir='./test_song_info', keep_byproducts=True)

    # Obtaining a list of the song bpms
    bpms = [result.bpm for result in song_info]

    # Obtaining the key of each song
    keys = find_key(mp3_files)

    # Find the optimum order of the list of songs
    # song_order = GA_schedule(bpms=bpms, keys=keys) # Or can use LP sched
    song_order = LP_sched(bpm_list=bpms, key_list=keys)

    # Storing obtained data into a df
    data = {
        'order': song_order,
        'path': mp3_files,
        'info': song_info,
        'bpm': bpms,
        'key': keys
    }
    print(data)
    df = pd.DataFrame(data)

    print(df)

    
    mix_songs(df)
    




    return 
    


if __name__ == '__main__':

    main()


'''../Songs/Drake,Sexyy red,SZA - Rich Baby Daddy.mp3
../Songs/Lit Reno - STOP BREATHING!.mp3
../Songs/Drake,21 Savage,Project Pat - Knife Talk.mp3
../Songs/Lilith1.mp3
../Songs/xihu.mp3
../Songs/Lil Uzi Vert - Just Wanna Rock.mp3
../Songs/Travis Scott,Kendrick Lamar - goosebumps.mp3
../Songs/艾志恒Asen,Maikon Flocka Flame - Butterflies.mp3
../Songs/Lil Durk,J. Cole - All My Life.mp3
../Songs/¥$,Kanye West,Ty Dolla $ign - VULTURES (feat. Bump J).mp3
../Songs/20min.mp3
../Songs/艾志恒Asen - DAY1.mp3
../Songs/Drake - In My Feelings.mp3'''