from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import os




def dtm(text, typ, max_features=5000):
    valid_typ = ['uni', 'bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca']
    if typ not in valid_typ:
        raise ValueError("dtm: 'typ' must be one of %r." % valid_typ)

    n = valid_typ.index(typ) + 1
    cv = CountVectorizer(ngram_range=(n,n), max_features=max_features, dtype=np.uint16)
    data_cv = cv.fit_transform(text)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())

    data_dtm = pd.DataFrame(data_dtm.sum(axis=0), dtype=np.uint16, columns=['Count'])
    data_dtm = data_dtm.sort_values(by='Count', ascending=False)

    return data_dtm

def dtms_integrate(dtms_list):  ## MemoryError problem here
    # dt_integ = None
    # for dt in dtms_list:
    dt_integ = pd.concat(dtms_list, axis=0)
    dt_integ.reset_index(inplace=True)
    dt_integ = pd.DataFrame(dt_integ.groupby('index')['Count'].sum(), columns=['Count'], dtype=np.uint16)

    dt_integ.sort_values(by='Count', ascending=False, inplace=True)
    return dt_integ

def dtms_source(source, typ, profanity=False, max_features=5000, pickled=True):
    valid_typ = {'uni', 'bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca'}
    if typ not in valid_typ:
        raise ValueError("dtm: 'typ' must be one of %r." % valid_typ)

    dir_path = ''
    if profanity:
        dir_path = 'cleandata/' + source + '_splitted/profanity_not'
    else:
        dir_path = 'cleandata/' + source + '_splitted'

    files_path = [dir_path + '/' + item for item in os.listdir(dir_path) if
                  os.path.isfile(os.path.join(dir_path, item))]

    dtms_list = []

    for f in files_path:
        file = open(f, 'rt', encoding='utf8')
        text = file.readlines()
        file.close()
        try:
            dtm_dt = dtm(text, typ, max_features=max_features)
        except MemoryError:
            print('Memory Error in ' + format(file))
        dtm_dt.astype(np.uint16)
        dtms_list.append(dtm_dt)

    dtm_integrated = dtms_integrate(dtms_list)

    # pickle
    if pickled:
        path = ''
        if profanity:
            path = 'pickles/DTMs/dtm-' + typ + '/profanity-not/' + source + '_dtm_'+ typ +'_badnot.pkl'
        else:
            path = 'pickles/DTMs/dtm-' + typ + '/general/' + source + '_dtm_' + typ +'.pkl'

        dtm_integrated.to_pickle(path)

    return dtm_integrated


# <-- Unigrams -->
#dtms_source(source='news', typ='uni')
#dtms_source(source='news', typ='uni', profanity=True)

#dtms_source(source='blogs', typ='uni')
#dtms_source(source='blogs', typ='uni', profanity=True)
#
#dtms_source(source='twitter', typ='uni')
#dtms_source(source='twitter', typ='uni', profanity=True)


# <-- Bigrams -->
#dtms_source(source='news', typ='bi')
#dtms_source(source='news', typ='bi', profanity=True)

#dtms_source(source='blogs', typ='bi')
#dtms_source(source='blogs', typ='bi', profanity=True)
#
#dtms_source(source='twitter', typ='bi')
#dtms_source(source='twitter', typ='bi', profanity=True)



# <-- Trigrams -->
# dtms_source(source='news', typ='tri')
# dtms_source(source='news', typ='tri', profanity=True)

# dtms_source(source='blogs', typ='tri')
# dtms_source(source='blogs', typ='tri', profanity=True)
#
# dtms_source(source='twitter', typ='tri')
# dtms_source(source='twitter', typ='tri', profanity=True)


# <-- Quadgrams -->
#dtms_source(source='news', typ='quad')
#dtms_source(source='news', typ='quad', profanity=True)

#dtms_source(source='blogs', typ='quad')
#dtms_source(source='blogs', typ='quad', profanity=True)
#
#dtms_source(source='twitter', typ='quad')
#dtms_source(source='twitter', typ='quad', profanity=True)

# <-- Pentagrams -->
#dtms_source(source='news', typ='penta')
#dtms_source(source='news', typ='penta', profanity=True)

#dtms_source(source='blogs', typ='penta')
#dtms_source(source='blogs', typ='penta', profanity=True)
#
#dtms_source(source='twitter', typ='penta')
#dtms_source(source='twitter', typ='penta', profanity=True)


# <-- Hexagrams -->
#dtms_source(source='news', typ='hexa')
#dtms_source(source='news', typ='hexa', profanity=True)

#dtms_source(source='blogs', typ='hexa')
#dtms_source(source='blogs', typ='hexa', profanity=True)
#
#dtms_source(source='twitter', typ='hexa')
#dtms_source(source='twitter', typ='hexa', profanity=True)


# <-- Heptagrams -->
#dtms_source(source='news', typ='hepta')
#dtms_source(source='news', typ='hepta', profanity=True)

#dtms_source(source='blogs', typ='hepta')
#dtms_source(source='blogs', typ='hepta', profanity=True)
#
#dtms_source(source='twitter', typ='hepta')
#dtms_source(source='twitter', typ='hepta', profanity=True)


# <-- Octagrams -->
#dtms_source(source='news', typ='octa')
#dtms_source(source='news', typ='octa', profanity=True)

#dtms_source(source='blogs', typ='octa')
#dtms_source(source='blogs', typ='octa', profanity=True)
#
# dtms_source(source='twitter', typ='octa')
# dtms_source(source='twitter', typ='octa', profanity=True)


# <-- Nonagrams -->
# dtms_source(source='news', typ='nona')
# dtms_source(source='news', typ='nona', profanity=True)

# dtms_source(source='blogs', typ='nona')
# dtms_source(source='blogs', typ='nona', profanity=True)
#
# dtms_source(source='twitter', typ='nona')
# dtms_source(source='twitter', typ='nona', profanity=True)


# <-- Decagrams -->
# dtms_source(source='news', typ='deca')
# dtms_source(source='news', typ='deca', profanity=True)

# dtms_source(source='blogs', typ='deca')
# dtms_source(source='blogs', typ='deca', profanity=True)
#
# dtms_source(source='twitter', typ='deca')
# dtms_source(source='twitter', typ='deca', profanity=True)


#--> DTMs Integration based on grams type
def dtms_integrate_typ(typ, profanity=False, pickled=True, min_freq = 2, split_terms=True):
    valid_typ = ['uni', 'bi', 'tri', 'quad', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca']
    if typ not in valid_typ:
        raise ValueError("dtm: 'typ' must be one of %r." % valid_typ)

    dir_path = ''
    if profanity:
        dir_path = 'pickles/DTMs/dtm-' + typ + '/profanity-not'
    else:
        dir_path = 'pickles/DTMs/dtm-' + typ + '/general'

    files_path = [dir_path + '/' + item for item in os.listdir(dir_path) if
                  os.path.isfile(os.path.join(dir_path, item))]

    dtms_list = []

    for f in files_path:
        dtm = pd.read_pickle(f)
        dtm = dtm[dtm['Count'] >= min_freq]
        dtms_list.append(dtm)

    dtm_integrated = dtms_integrate(dtms_list)

    if split_terms:
        dtm_integrated.reset_index(inplace=True)
        n = valid_typ.index(typ) + 1
        col_names = ['Word'+format(i+1) for i in range(n)]
        dtm_integrated[col_names] = dtm_integrated['index'].str.split(' ', expand=True)
        col_names.extend(['Count'])
        dtm_integrated = dtm_integrated[col_names]

    # pickle
    if pickled:
        path = ''
        if profanity:
            path = 'pickles/DTMs/dtm-' + typ + '/integrated/dtm_' + typ + '_badnot.pkl'
        else:
            path = 'pickles/DTMs/dtm-' + typ + '/integrated/dtm_' + typ + '.pkl'

        dtm_integrated.to_pickle(path)

    return dtm_integrated

# integrate DTMs (run again with min_freq = 3)
# dtms_integrate_typ('uni')
# dtms_integrate_typ('uni', profanity=True)

# dtms_integrate_typ('bi')
# dtms_integrate_typ('bi', profanity=True)
#
# dtms_integrate_typ('tri')
# dtms_integrate_typ('tri', profanity=True)
#
# dtms_integrate_typ('quad')
# dtms_integrate_typ('quad', profanity=True)
#
# dtms_integrate_typ('penta')
# dtms_integrate_typ('penta', profanity=True)
#
# dtms_integrate_typ('hexa')
# dtms_integrate_typ('hexa', profanity=True)
#
# dtms_integrate_typ('octa') ## Memory error (why int64?!)
# dtms_integrate_typ('octa', profanity=True)
#
# dtms_integrate_typ('hepta')
# dtms_integrate_typ('hepta', profanity=True)
#
# dtms_integrate_typ('nona')
# dtms_integrate_typ('nona', profanity=True)
#
# dtms_integrate_typ('deca')
# dtms_integrate_typ('deca', profanity=True)
