# title: 	sentiment analysis
# author:	Eole Cervenka
# date:		03/08/2016


'''
SOURCES

***************************************
Opinion Lexicon: Positive & Negative
***************************************

`positive-words.txt` contains a list of POSITIVE opinion words (or sentiment words).
`negative-words.txt` contains a list of POSITIVE opinion words (or sentiment words).

This file and the papers can all be downloaded from 
http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

Citation:

   Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
       Proceedings of the ACM SIGKDD International Conference on Knowledge 
       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
       Washington, USA, 
   Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
       and Comparing Opinions on the Web." Proceedings of the 14th 
       International World Wide Web conference (WWW-2005), May 10-14, 
       2005, Chiba, Japan.


***************************************
Mapping Stemmed word -> Unstemmed word
***************************************

`mxm_reverse_mapping.txt` contains the mapping for Stemmed word -> Unstemmed word

This file can be downloaded from 
http://labrosa.ee.columbia.edu/millionsong/sites/default/files/mxm_reverse_mapping.txt

Citation:

musiXmatch dataset, the official lyrics collection for the Million Song Dataset

@INPROCEEDINGS{Bertin-Mahieux2011,
  author = {Thierry Bertin-Mahieux and Daniel P.W. Ellis and Brian Whitman and Paul Lamere},
  title = {The Million Song Dataset},
  booktitle = {{Proceedings of the 12th International Conference on Music Information
	Retrieval ({ISMIR} 2011)}},
  year = {2011},
  owner = {thierry},
  timestamp = {2010.03.07}
}
'''


import re
import pandas as pd


# Prepare `mood lexicon`: STEMMED_WORD | MOOD
# *******************************************

# Download sources `mxm_reverse_mapping.txt` and `positive-words.txt`, `negative-words.txt` under <path>
path = '/home/eolus/Documents/MA755_data/LyricsData/'

# Put text content stemmed/unstemmed entries in list
f_1 = open(path+'mxm_reverse_mapping.txt', 'r')
lines_1 = [line.rstrip('\n').split('<SEP>') for line in f_1.readlines()]

# Put list in pandas df
df_1 = pd.DataFrame(lines_1, columns=['Stemmed', 'Unstemmed'])

# Remove non letter terms
df_stem_mapping = df_1[df_1.Stemmed.str.match("^[a-zA-Z]+$") == True]

# Put text content positive & negative unstemmed entries in list
f_2 = open(path+'positive-words.txt', 'r', encoding='ISO-8859-1')
lines_2 = [line.rstrip('\n') for line in f_2.readlines()]

f_3 = open(path+'negative-words.txt', 'r', encoding='ISO-8859-1')
lines_3 = [line.rstrip('\n') for line in f_3.readlines()]

# Put list positive in pandas df
df_2 = pd.DataFrame(lines_2, columns=['Unstemmed'])
df_2['Mood'] = pd.Series([1] * len(df_2.index) )

# Put list negative in pandas df
df_3 = pd.DataFrame(lines_3, columns=['Unstemmed'])
df_3['Mood'] = pd.Series([-1] * len(df_3.index) )

# Stack the positive and negative df on top of each other
df_mood = pd.concat([df_2, df_3], axis=0)

# Define outter join data.frame to JOIN stem_mapping and df_mood
df_outter_join = pd.merge(df_stem_mapping, df_mood, on='Unstemmed', how='outer')

# Filter out Nan values in `Stemmed` (meaning is not in Lyrics bag of word) and from `Mood`(meaning not in sentiment lexicon docs)
df_stem = df_outter_join[df_outter_join.Stemmed.notnull() & df_outter_join.Mood.notnull()]
print(df_stem)
print('Stemmed words tagged with a mood value: %d' %(len(df_stem.index)))


# Save `df_stem` to pickle file:
save_load_path = '/home/eolus/Documents/MA755_data/myPickles'
df_stem.to_pickle(save_load_path+'/df_stem.pkl')
