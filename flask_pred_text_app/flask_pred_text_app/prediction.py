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
import pandas as pd
import random
from nltk import word_tokenize
from flask_pred_text_app import words_uni
from flask_pred_text_app import words_uni, prob_bi, prob_tri, prob_quad, prob_penta, prob_hexa, prob_hepta, prob_octa, prob_nona, prob_deca
from flask_pred_text_app import bad_pattern







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

    words = word_tokenize(str)

    return words

# Choose randomly Unigrams
def get_random_unigram(n=5):
    return random.sample(words_uni, n)


# Backoff from Tri-grams
def get_next_backoff_2grams(input_words, n = 5):

    if input_words is None:
        return None

    probs = prob_bi

    probs_selected = probs[probs['Word1'] == input_words[0]]
    #probs_selected.sort_values('Prob', inplace=True)
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

    probs = prob_tri

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                               (probs['Word2'] == input_words[1])]
    #probs_selected.sort_values('Prob', inplace=True)
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

    probs = prob_quad

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                               (probs['Word2'] == input_words[1]) &
                               (probs['Word3'] == input_words[2])]
    #probs_selected.sort_values('Prob', inplace=True)
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

    probs = prob_penta

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3])]
    #probs_selected.sort_values('Prob', inplace=True)
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

    probs = prob_hexa

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3]) &
                           (probs['Word5'] == input_words[4])]
    #probs_selected.sort_values('Prob', inplace=True)
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word6'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_5 = get_next_backoff_5grams(input_words[-4:], n-num_suggested)
        suggested_words.extend(suggested_words_5)

    return suggested_words

# Backoff from Hepta-grams
def get_next_backoff_7grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 6:
        return None

    if len(input_words) > 6:
        input_words_words = input_words[-6:]

    probs = prob_hepta

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3]) &
                           (probs['Word5'] == input_words[4]) &
                           (probs['Word6'] == input_words[5])]
    #probs_selected.sort_values('Prob', inplace=True)
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word7'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_6 = get_next_backoff_6grams(input_words[-5:], n-num_suggested)
        suggested_words.extend(suggested_words_6)

    return suggested_words

# Backoff from Octa-grams
def get_next_backoff_8grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 7:
        return None

    if len(input_words) > 7:
        input_words_words = input_words[-7:]

    probs = prob_octa

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3]) &
                           (probs['Word5'] == input_words[4]) &
                           (probs['Word6'] == input_words[5]) &
                           (probs['Word7'] == input_words[6])]
    #probs_selected.sort_values('Prob', inplace=True)
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word8'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_7 = get_next_backoff_7grams(input_words[:6], n-num_suggested)
        suggested_words.extend(suggested_words_7)

    return suggested_words

# Backoff from Nona-grams
def get_next_backoff_9grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 8:
        return None

    if len(input_words) > 8:
        input_words_words = input_words[-8:]

    probs = prob_nona

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3]) &
                           (probs['Word5'] == input_words[4]) &
                           (probs['Word6'] == input_words[5]) &
                           (probs['Word7'] == input_words[6]) &
                           (probs['Word8'] == input_words[7])]
    #probs_selected.sort_values('Prob', inplace=True)
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word9'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_8 = get_next_backoff_8grams(input_words[:7], n-num_suggested)
        suggested_words.extend(suggested_words_8)

    return suggested_words

# Backoff from Nona-grams
def get_next_backoff_10grams(input_words, n = 5):

    if input_words is None:
        return None
    if len(input_words) < 9:
        return None

    if len(input_words) > 9:
        input_words_words = input_words[-9:]

    probs = prob_deca

    probs_selected = probs[(probs['Word1'] == input_words[0]) &
                           (probs['Word2'] == input_words[1]) &
                           (probs['Word3'] == input_words[2]) &
                           (probs['Word4'] == input_words[3]) &
                           (probs['Word5'] == input_words[4]) &
                           (probs['Word6'] == input_words[5]) &
                           (probs['Word7'] == input_words[6]) &
                           (probs['Word8'] == input_words[7]) &
                           (probs['Word9'] == input_words[8])]
    #probs_selected.sort_values('Prob', inplace=True)
    probs_selected = probs_selected.head(n)

    suggested_words = list(probs_selected['Word10'])
    num_suggested = len(suggested_words)

    if num_suggested < n:
        suggested_words_9 = get_next_backoff_9grams(input_words[:8], n-num_suggested)
        suggested_words.extend(suggested_words_9)

    return suggested_words


# Predict the Next Word
def get_next_backoff(str, start_typ='deca', n = 5):
    valid_typ = ['bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca']
    if start_typ not in valid_typ:
        raise ValueError("'start_typ' must be one of %r." % valid_typ)

    n_typ = valid_typ.index(start_typ) + 2

    if str is '':
        return ''

    if str == '':
        return list(set(get_random_unigram(n)))

    words = preprocess_str(str)
    input_words = words[-n_typ+1:]

    if len(input_words) < n_typ-1:
        n_typ = len(input_words)+1


    suggested_words = None

    if n_typ == 2:
        suggested_words = get_next_backoff_2grams(input_words, n)
    elif n_typ == 3:
        suggested_words = get_next_backoff_3grams(input_words, n)
    elif n_typ == 4:
        suggested_words = get_next_backoff_4grams(input_words, n)
    elif n_typ == 5:
        suggested_words = get_next_backoff_5grams(input_words, n)
    elif n_typ == 6:
        suggested_words = get_next_backoff_6grams(input_words, n)
    elif n_typ == 7:
        suggested_words = get_next_backoff_7grams(input_words, n)
    elif n_typ == 8:
        suggested_words = get_next_backoff_8grams(input_words, n)
    elif n_typ == 9:
        suggested_words = get_next_backoff_9grams(input_words, n)
    else:
        suggested_words = get_next_backoff_10grams(input_words, n)

    return list(set(suggested_words))


