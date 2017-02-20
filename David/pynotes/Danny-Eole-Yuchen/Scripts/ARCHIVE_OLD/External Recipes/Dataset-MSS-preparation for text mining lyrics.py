# coding: utf-8
# Million Songs Dataset - Aggregation of song and lyrics data

# Source/Original notebook: 'Dataset-MSS-preparation for text mining lyrics'

# REQUIREMENTS:
# + Run `Dataset-MSS-pandas-create dataframe.py`
# + Run `Dataset-MSS-pandas-prepare lyrics data.py` 

import pandas as pd
import sqlite3

save_load_path = '/home/eolus/Documents/MA755_data/myPickle'


# ### Create a data frame with rows for each track and columns for each word. 
# Cells contain the count of that word in the lyrics for that track.

# Load the `mss_df` and `lyrics_df` dataframes.
mss_df = pd.read_pickle(save_load_path+'/mss_df.pkl')
lyrics_df = pd.read_pickle(save_load_path+'/lyrics_df.pkl')

# Next, load the stopwords from the `nltk` package.
import nltk 
stopword_set = set(nltk.corpus.stopwords.words('english'))
is_not_stopword = [word not in stopword_set for word in lyrics_df.word.ravel()]


# Create dataframe `lyrics_sub_df` by removing the stopwords.
lyrics_sub_df = lyrics_df[is_not_stopword]

# We have now 4884 unique words for all the lyrics, which doesn't seem like much. 
len(pd.unique(lyrics_sub_df.word.ravel())), pd.unique(lyrics_sub_df.word.ravel())

# Now merge the lyrics without stopwords dataframe `lyrics_sub_df` with the `mss_df` dataframe. 
mss_lyrics_df = lyrics_sub_df.merge(mss_df, how='inner', on='track')

# But we really just want the variables `track`, `word` and `count`.
mss_lyrics_twc_df = mss_lyrics_df[['track','word','count']]

# If we want more variables later then they should be merged into the dataframe.
# Now we _gather_ the rows into columns. __R__ users will recall the `tidyr` package.
import numpy as np
mss_lyrics_pvt_df = mss_lyrics_df.pivot(index='track', 
                                        columns='word', 
                                        values='count')

# Replace NaN values with 0
NaN_locations = np.isnan(mss_lyrics_pvt_df)
mss_lyrics_pvt_df[NaN_locations] = 0

conn_lyrics.close()

# Save to pickle
mss_lyrics_pvt_df.to_pickle(save_load_path+'/mss_lyrics_pvt_df.pkl')