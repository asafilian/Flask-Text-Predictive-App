'''
PREDICTION ALGORITHM

The algorithm follows the 'stupid back-off method', and make 5 suggestions as the next word.
Suppose that we first start with quadgrams.
1. The function gets a string and tokenizes and preprocesses it.
2. It extracts the last 3 words of the string.
3. The function uses the quad-gram probability.
4. If the function above cannot find 5 quad-grams with the 3 given words, the algorithm backoffs to the 3-gram model.
5. If the algorithm cannot make enough suggestions by the 3-gram models, it backoffs to bi-grams.
6. If it cannot even find the corresponding bigrams, it randomly gets a word from unigrams with high probability.

NOTE: From now on, I decided to play with only filtered out profanities
'''

import re
import string
import random
import pandas as pd
from sqlalchemy import *
import pymysql

# connect to the engine
DATABASE_URI = 'mysql+pymysql:....'
engine = create_engine(DATABASE_URI, echo=False)

# get profanities
profanities = pd.read_sql_table('profanities_tb', engine)
bad_pattern = profanities.Word[0]
for item in profanities.Word[1:]:
    bad_pattern = bad_pattern + '|' + item


# get unigrams
unigrams = pd.read_sql_table('unigrams_tb', engine)

# get bigrams
bigrams = pd.read_sql_table('bigrams_tb', engine)

# get trigrams
trigrams = pd.read_sql_table('trigrams_tb', engine)

# get quadgrams
quadgrams = pd.read_sql_table('quadgrams_tb', engine)

# get pentagrams
pentagrams = pd.read_sql_table('pentagrams_tb', engine)

# get hexagrams
hexagrams = pd.read_sql_table('hexagrams_tb', engine)



def preprocess_str(str):
    ## to lower case
    str = str.lower()
    ## remove text containing numbers
    dig_pattern = re.compile(r'\w*\d\w*')
    str = re.sub(dig_pattern, '', str)
    ## remove punctuations
    str = re.sub('[%s]' % re.escape(string.punctuation), '', str)
    ## remove urls
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    str = re.sub(url_pattern, '', str)
    ## remove words containing non-english characters
    neng_pattern = re.compile(r'[A-z]*[^\x01-\x7F]+[A-z]*')
    str = re.sub(neng_pattern, '', str)
    ## remove non-sense words
    nsens_pattern = re.compile(r'\\w*(kk|nn|zz|'
                               r'aaa|bbb|ccc|ddd|eee|fff|ggg|hhh|jjj|lll|ppp|qqq|rrr|vvv|xxx|'
                               r'iiii|ssss|wwww|mmmmm|ooooo|ttttt|uuuuu|yyyyy)+\\w*\\s*')
    str = re.sub(nsens_pattern, '', str)
    ## filter out profanities
    str = re.sub(bad_pattern, '', str)

    words = str.split(' ')

    return words

# Choose randomly Unigrams
def get_random_unigram(n=5):
    return random.sample(list(unigrams.Word1), n)


# Backoff from Tri-grams
def get_next_backoff_2grams(input_words, n = 5):

    if input_words is None:
        return None

    probs_selected = bigrams[bigrams['Word1'] == input_words[0]]
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word2'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_1 = get_random_unigram(n-num_suggested)
        suggested_words.extend(suggested_words_1)

    return suggested_words

# Backoff from Tri-grams
def get_next_backoff_3grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 2:
        return None

    if len(input_words) > 2:
        input_words_words = input_words[-2:]

    probs_selected = trigrams[(trigrams['Word1'] == input_words[0]) &
                               (trigrams['Word2'] == input_words[1])]
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word3'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_2 = get_next_backoff_2grams(input_words[0], n-num_suggested)
        suggested_words.extend(suggested_words_2)

    return suggested_words

# Backoff from Quad-grams
def get_next_backoff_4grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 3:
        return None

    if len(input_words) > 3:
        input_words_words = input_words[-3:]

    probs_selected = quadgrams[(quadgrams['Word1'] == input_words[0]) &
                               (quadgrams['Word2'] == input_words[1]) &
                               (quadgrams['Word3'] == input_words[2])]
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word4'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_3 = get_next_backoff_3grams(input_words[-2:], n-num_suggested)
        suggested_words.extend(suggested_words_3)

    return suggested_words


# Backoff from Penta-grams
def get_next_backoff_5grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 4:
        return None

    if len(input_words) > 4:
        input_words_words = input_words[-4:]

    probs_selected = pentagrams[(pentagrams['Word1'] == input_words[0]) &
                           (pentagrams['Word2'] == input_words[1]) &
                           (pentagrams['Word3'] == input_words[2]) &
                           (pentagrams['Word4'] == input_words[3])]
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word5'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_4 = get_next_backoff_4grams(input_words[-3:], n-num_suggested)
        suggested_words.extend(suggested_words_4)

    return suggested_words


# Backoff from Hexa-grams
def get_next_backoff_6grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 5:
        return None

    if len(input_words) > 5:
        input_words_words = input_words[-5:]

    probs_selected = hexagrams[(hexagrams['Word1'] == input_words[0]) &
                           (hexagrams['Word2'] == input_words[1]) &
                           (hexagrams['Word3'] == input_words[2]) &
                           (hexagrams['Word4'] == input_words[3]) &
                           (hexagrams['Word5'] == input_words[4])]
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word6'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_5 = get_next_backoff_5grams(input_words[-4:], n-num_suggested)
        suggested_words.extend(suggested_words_5)

    return suggested_words


# Predict the Next Word
def get_next_backoff(str, n = 5):

    n_typ = 6
    if str == '':
        return ''

    words = preprocess_str(str)
    input_words = words[-n_typ+1:]

    if len(input_words) < n_typ:
        n_typ = len(input_words)+1


    suggested_words = None

    if n_typ == 6:
        suggested_words = get_next_backoff_6grams(input_words, n)
    elif n_typ == 5:
        suggested_words = get_next_backoff_5grams(input_words, n)
    elif n_typ == 4:
        suggested_words = get_next_backoff_4grams(input_words, n)
    elif n_typ == 3:
        suggested_words = get_next_backoff_3grams(input_words, n)
    else:
        suggested_words = get_next_backoff_2grams(input_words, n)


    return list(set(suggested_words))

