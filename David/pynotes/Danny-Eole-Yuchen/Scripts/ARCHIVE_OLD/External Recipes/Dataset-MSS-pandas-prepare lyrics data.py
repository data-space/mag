# coding: utf-8
# Million Songs Dataset - Aggregation of song and lyrics data (originak notebook: 'Dataset-MSS-preparation for text mining lyrics')

# REQUIREMENTS:
# + Download `mxm_dataset.db`

import pandas as pd
import sqlite3

# Location of pickle files (save/load)
save_load_path = '/home/eolus/Documents/MA755_data/myPickle'

# Location for lyrics data: 'mxm_dataset.db'
data_path = '/home/eolus/Documents/MA755_data/LyricsData/mxm_dataset.db'


# Open connection to lyrics data file
conn_lyrics	= sqlite3.connect(data_path)

# Feed dataframe from SQLite query
lyrics_df	= pd.DataFrame(pd.read_sql('SELECT * FROM lyrics', con= conn_lyrics))
lyrics_df = lyrics_df.rename(columns = {'track_id':'track'})

# Save to pickle
lyrics_df.to_pickle(save_load_path+'/lyrics_df.pkl')