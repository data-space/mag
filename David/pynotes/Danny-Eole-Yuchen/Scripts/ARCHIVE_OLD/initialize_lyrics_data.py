# author: Eole CERVENKA
# date: 03/08/2016

import pandas as pd
import numpy as np
import pickle
import sqlite3
import itertools

lyrics_path = '/home/eolus/Documents/MA755_data/LyricsData'
pickle_path = '/home/eolus/Documents/MA755_data/myPickles'

# Access MXM data stored in SQLite using Python and Pandas
con = sqlite3.connect(lyrics_path +'/mxm_dataset.db')
c = con.cursor()

# Get set of track_id
c.execute('SELECT DISTINCT track_id FROM lyrics')
data_track_id = c.fetchall()
set_track_id = set(itertools.chain.from_iterable(data_track_id))

# Convert to list of track_id to use as DataFrame index
list_track_id = []
list_track_id.extend(set_track_id)

# Load df_stem from the pickle file (STEM | MOOD)
df_stem = pd.read_pickle(pickle_path+'/df_stem.pkl')

# Put unique stemmed words into a set for faster look-ups
stemmed_set = set(pd.unique(df_stem.Stemmed.ravel()))

# Create list of `lyrics_df` column names [<WORD#1>, ... ,<WORD#N>, 'COUNT_OTHER']
column_names = []
for word in stemmed_set:
	column_names.append(word.upper())
column_names.append('COUNT_OTHER')

# Initialize pd.dataframe `lyrics_df` : INDEX = TRACK_ID | <WORD#1> | ... | <WORD#N> | COUNT_OTHER
lyrics_df = pd.DataFrame(columns = column_names, index = list_track_id)
lyrics_df = lyrics_df.fillna(0)
lyrics_df[column_names] = lyrics_df[column_names].astype('int32')
print(lyrics_df)

# Save initialized `lyrics_df` in pkl file
lyrics_df.to_pickle(pickle_path+'/df_lyrics.pkl')