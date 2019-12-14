'''
Number: 5
Since our app will return the top-5 most likely word for a given sequence of words,
 it does not make sense to keep lower-rated n-grams.
That's, in a ngrams table, for a given n-1-gram 'w1....wn-1', we keep top-5 ngrams 'w1...wn-1 w'
Moreover, we do not need to keep all unigrams. We just keep top-50 rated unigrams.
These will help us to have a much faster and mempry-efficient web-based app.
'''

import pandas as pd

def keep_top_ngrams(typ, top=5, profanity=False, pickled=True):

    # check if typ is valid
    valid_typ = ['uni', 'bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca']
    if typ not in valid_typ:
        raise ValueError("dtm: 'typ' must be one of %r." % valid_typ)

    n = valid_typ.index(typ) + 1

    # read the corresponiding datafarme
    path = ''
    if profanity:
        path = 'pickles/Probs/profanity-not/prob_' + typ + '_np.pkl'
    else:
        path = 'pickles/Probs/general/prob_' + typ + '.pkl'
    prob_df = pd.read_pickle(path)

    # drop column 'Count'
    prob_df.drop('Count', axis=1, inplace=True)

    if typ == 'uni': # keep top 50 unigrams
        prob_df.sort_values(by='Prob', ascending=False, inplace=True)
        prob_df.reset_index(inplace=True, drop=True)
        prob_top = prob_df[:50]
    else: # keep top-5 ngrams for each (n-1)grams
        col_indx = ['Word' + format(i+1) for i in range(n-1)]
        prob_top = prob_df.groupby(col_indx).head(5).reset_index(drop=True)

    # pickle
    if pickled:
        path = ''
        if profanity:
            if typ == 'uni':
                path = 'pickles/Final Probs/profanity-not/prob_' + typ + '_top50_np.pkl'
            else:
                path = 'pickles/Final Probs/profanity-not/prob_' + typ + '_top' + format(top) + '_np.pkl'
        else:
            if typ == 'uni':
                path = 'pickles/Final Probs/general/prob_' + typ + '_top50.pkl'
            else:
                path = 'pickles/Final Probs/general/prob_' + typ + '_top' + format(top) + '.pkl'

        prob_top.to_pickle(path)

    return prob_top


# Unigrams
prob_top_uni = keep_top_ngrams(typ='uni')
prob_top_uni_np = keep_top_ngrams(typ='uni', profanity=True)


# Bigrams
prob_top_bi = keep_top_ngrams(typ='bi')
prob_top_bi_np = keep_top_ngrams(typ='bi', profanity=True)

# Trigrams
prob_top_tri = keep_top_ngrams(typ='tri')
prob_top_tri_np = keep_top_ngrams(typ='tri', profanity=True)

# Quadgrams
prob_top_quad = keep_top_ngrams(typ='quad')
prob_top_quad_np = keep_top_ngrams(typ='quad', profanity=True)


# Pentagrams
prob_top_penta = keep_top_ngrams(typ='penta')
prob_top_penta_np = keep_top_ngrams(typ='penta', profanity=True)

# Hexagrams
prob_top_hexa = keep_top_ngrams(typ='hexa')
prob_top_hexa_np = keep_top_ngrams(typ='hexa', profanity=True)

# Heptagrams
prob_top_hepta = keep_top_ngrams(typ='hepta')
prob_top_hepta_np = keep_top_ngrams(typ='hepta', profanity=True)

# Octagrams
prob_top_octa = keep_top_ngrams(typ='octa')
prob_top_octa_np = keep_top_ngrams(typ='octa', profanity=True)

# Nonagrams
prob_top_nona = keep_top_ngrams(typ='nona')
prob_top_nona_np = keep_top_ngrams(typ='nona', profanity=True)

# Decagrams
prob_top_deca = keep_top_ngrams(typ='deca')
prob_top_deca_np = keep_top_ngrams(typ='deca', profanity=True)