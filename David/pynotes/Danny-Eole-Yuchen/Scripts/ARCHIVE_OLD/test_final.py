import pandas as pd
import numpy as np
import pickle


lyrics_path = '/home/eolus/Documents/MA755_data/LyricsData'
pickle_path = '/home/eolus/Documents/MA755_data/myPickles'


# Retrieve `lyrics_df`
lyrics_df = pd.read_pickle(pickle_path+'/full_df_lyrics.pkl')


sum_columns = lyrics_df.columns[:(len(lyrics_df.columns)-2)]

# Deactivate Pandas warning on chained assignment
pd.options.mode.chained_assignment = None

# Create filtered version of the lyrics DataFrame for reporting purpose
lyrics_df_filtered = lyrics_df[(lyrics_df.COUNT_OTHER > 0)]
lyrics_df_filtered['COUNT_MOOD_RATED'] = ''
lyrics_df_filtered['%_MOOD_RATED'] = ''

for index, row in lyrics_df_filtered.iterrows():

	count_mood = sum([lyrics_df_filtered.get_value(index, col) for col in sum_columns])
	count_no_mood = lyrics_df_filtered.get_value(index, 'COUNT_OTHER')

	lyrics_df_filtered['COUNT_MOOD_RATED'][index] = count_mood
	lyrics_df_filtered['%_MOOD_RATED'][index] = '{percent}%'.format(percent = round((count_mood / (count_mood + count_no_mood) * 100),2))

lyrics_df_reporting = lyrics_df_filtered[['COUNT_OTHER', 'COUNT_MOOD_RATED', '%_MOOD_RATED']]
lyrics_df_reporting.columns = ['NOT_MOOD_RATED', 'MOOD_RATED', '%_MOOD_RATED']

print(lyrics_df_reporting)