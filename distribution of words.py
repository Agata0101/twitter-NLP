# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 10:59:58 2019

@author: Agata
"""

"""
distribution of words
cloud of words
"""


### DISTRIBUTION
# here I create a graph illustrating the distribution of words in tweets
# X-axis is the rank of the frequency from highest rank from left to the right. 
# Y-axis is the frequency observed in the corpus

# the results proove that the distributions of the frequency of words follow Zipf’s law
# the frequency of any word is inversely proportional to its rank in the frequency table

import matplotlib.pyplot as plt
y = [count for tag, count in tf.most_common(1000)]
x = range(1, len(y)+1)
fig = plt.figure(1, figsize=(13,11))
plt.ylabel('Number of occurences', fontsize=16, fontweight=500)
plt.xlabel('Position in the ranking of most commonly used words', fontsize=16, fontweight=500, labelpad=10)
plt.plot(x, y)
plt.title("The frequency distribution of words", fontsize=17, fontweight=600, y=1.02)
plt.tick_params(labelsize=15)
#plt.set_xlim(0, 1000)
#plt.xticks(np.arange(0,100,20))

#save the figue
#plt.savefig('term_distribution.png')

#### WORDCLOUD
# Here I represnat all most commonly used words in the form of a word cloud
from scipy.misc import imread
from wordcloud import WordCloud
from wordcloud import STOPWORDS

# Here I import the mask to represent the word cloud in shape of a Twitter logo
twitter_mask = imread('twitter_mask.png')

## from the counter
wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color='white',
                      width=1800,
                      height=1400,
                      #max_words=1000,
                      mask=twitter_mask
            ).fit_words(tf)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./my_twitter_wordcloud_2.png', dpi=300)
plt.show()