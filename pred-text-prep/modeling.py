'''
Number: 4
This file models sequences of words using the statistical properties of n-grams.
I follow the Markov assumption (or independence assumption).
As for probabilities, I use and implement the Kneser-Ney Smoothing method.
'''
import pandas as pd


# --> Unigrams Probabilities (something wrong with this)
def kneserNey_prob_uni(profanity=False, pickled=True):
    '''
    profanity: bool - if True, it works in the dtm with profanities filterd out
    pickled: bool - if True the result is pickled
    keep: int - keep the top-keep unigrams when pickled; give it -1 if you want to keep all
    '''

    # read the DTM for bigrams
    path = ''
    if profanity:
        path = 'pickles/DTMs/dtm-bi/integrated/dtm_bi_badnot.pkl'
    else:
        path = 'pickles/DTMs/dtm-bi/integrated/dtm_bi.pkl'
    dtm_bi = pd.read_pickle(path)

    # read the DTM for unigrams
    path = ''
    if profanity:
        path = 'pickles/DTMs/dtm-uni/integrated/dtm_uni_badnot.pkl'
    else:
        path = 'pickles/DTMs/dtm-uni/integrated/dtm_uni.pkl'
    dtm_uni = pd.read_pickle(path)


    # compute probabilities
    prob_uni = ((dtm_bi.groupby('Word2')[['Count']].count() / len(dtm_bi))).rename(columns={'Count':'Prob'})
    #prob_uni.sort_values(by='Prob', ascending=False, inplace=True)

    # merge with unigrams DTM
    count_prob_uni = pd.merge(dtm_uni, prob_uni, how='left', left_on='Word1', right_on='Word2')
    count_prob_uni.sort_values('Prob', ascending=False, inplace=True)

    count_prob_uni.dropna(inplace=True)

    if pickled:
        path = ''
        if profanity:
            path = 'pickles/Probs/profanity-not/prob_uni_np.pkl'
        else:
            path = 'pickles/Probs/general/prob_uni.pkl'

        count_prob_uni.to_pickle(path)

    return count_prob_uni


# --> Unigrams Probabilities
def kneserNey_ngrams(typ, discount_weight=0.75, profanity=False, pickled=True):
    '''
    typ: type of n-grams which you want to get the probability for
    discount_weight: discount weight/value
    profanity: bool - if True, it works in the dtm with profanities filterd out
    pickled: bool - if True the result is pickled
    '''

    valid_typ = ['uni', 'bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca']
    if typ not in valid_typ[1:]:
        raise ValueError("dtm: 'typ' must be one of %r." % valid_typ[1:])

    n = valid_typ.index(typ) + 1

    # read the DTM for bigrams and unigrams probabilities
    path_ngrams = ''
    path_prob = ''
    if profanity:
        path_ngrams = 'pickles/DTMs/dtm-' + typ + '/integrated/dtm_' + typ + '_badnot.pkl'
        path_prob = 'pickles/Probs/profanity-not/prob_' + valid_typ[valid_typ.index(typ)-1] + '_np.pkl'
    else:
        path_ngrams = 'pickles/DTMs/dtm-' + typ + '/integrated/dtm_' + typ + '.pkl'
        path_prob = 'pickles/Probs/general/prob_' + valid_typ[valid_typ.index(typ)-1] + '.pkl'

    dtm = pd.read_pickle(path_ngrams)
    probs = pd.read_pickle(path_prob)
    probs.drop(columns=['Count'], inplace=True)

    cols = ['Word' + format(i + 2) for i in range(n - 1)]
    cols.append('Prob_w2_wn')
    probs.columns = cols



    count_prob = dtm.copy()

    # get the n-1_grams probability of 'Word2 ... Wordn' & add to count_prob
    merge_on = ['Word'+format(i+2) for i in range(n-1)]
    count_prob = pd.merge(count_prob, probs, how='left', left_on=merge_on, right_on=merge_on)

    # compute count sum of 'Word1....Wordn-1' in ngrams & add to count_prob
    aggregate_on = ['Word'+format(i+1) for i in range(n-1)]
    count_w1_wn__1 = dtm.groupby(aggregate_on)[['Count']].sum().rename(columns={'Count': 'Count_w1_wn__1'})
    count_prob = pd.merge(count_prob, count_w1_wn__1, how='left', left_on=aggregate_on, right_on=aggregate_on)

    # compute number of ngrams with 'Word1...Wordn-1' as the first n-1 words & add to count_prob
    num_w1_wn__1 = dtm.groupby(aggregate_on)[['Count']].count().rename(columns={'Count': 'Num_w1_wn__1'})
    count_prob = pd.merge(count_prob, num_w1_wn__1, how='left', left_on=aggregate_on, right_on=aggregate_on)
    #
    # # compute the bigram probabilities & add count_prob_bi
    count_prob['Prob'] = ((count_prob['Count'] - discount_weight).combine(0, max)) / count_prob['Count_w1_wn__1']
    count_prob['Prob'] = (count_prob['Prob'] + (
                (discount_weight / count_prob['Count_w1_wn__1']) * count_prob['Num_w1_wn__1'] * count_prob['Prob_w2_wn']))


    # keep important columns and sort
    cols_selected =['Word' + format(i + 1) for i in range(n)]
    cols_selected.extend(['Count', 'Prob'])
    count_prob = count_prob[cols_selected]
    count_prob.sort_values('Prob', ascending=False, inplace=True)
    count_prob.reset_index(inplace=True, drop=True)

    count_prob.dropna(inplace=True)


    if pickled:
        path = ''
        if profanity:
            path = 'pickles/Probs/profanity-not/prob_' + typ + '_np.pkl'
        else:
            path = 'pickles/Probs/general/prob_' + typ + '.pkl'

        count_prob.to_pickle(path)

    return count_prob





#--> Probabilities of Unigrams
probs_uni = kneserNey_prob_uni()
probs_uni_notbad = kneserNey_prob_uni(profanity=True)

# --> Probabilities of Bigrams
probs_bi = kneserNey_ngrams(typ='bi')
probs_bi = kneserNey_ngrams(typ='bi', profanity=True)

# --> Probabilities of Trigrams
probs_tri = kneserNey_ngrams(typ='tri')
probs_tri = kneserNey_ngrams(typ='tri', profanity=True)


# --> Probabilities of Quadgrams
probs_quad = kneserNey_ngrams(typ='quad')
probs_quad = kneserNey_ngrams(typ='quad', profanity=True)


# --> Probabilities of Pentagrams
probs_penta = kneserNey_ngrams(typ='penta')
probs_penta = kneserNey_ngrams(typ='penta', profanity=True)


# --> Probabilities of Hexagrams
probs_hexa = kneserNey_ngrams(typ='hexa')
probs_hexa = kneserNey_ngrams(typ='hexa', profanity=True)

# --> Probabilities of Heptagrams
probs_hepta = kneserNey_ngrams(typ='hepta')
probs_hepta = kneserNey_ngrams(typ='hepta', profanity=True)

# --> Probabilities of Octagrams
probs_octa = kneserNey_ngrams(typ='octa')
probs_octa = kneserNey_ngrams(typ='octa', profanity=True)

# --> Probabilities of Nonagrams
probs_nona = kneserNey_ngrams(typ='nona')
probs_nona = kneserNey_ngrams(typ='nona', profanity=True)


# --> Probabilities of Decagrams
# probs_deca = kneserNey_ngrams(typ='deca')
# probs_deca = kneserNey_ngrams(typ='deca', profanity=True)













