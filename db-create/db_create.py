from sqlalchemy import create_engine
import pandas as pd
import pymysql

# put your connection string here
DATABASE_URI = '...'
engine = create_engine(DATABASE_URI, echo=False)

# pd.read_sql_query("create database db", con=engine)


# Load Unigrams
prob_uni = pd.read_pickle('data/prob_uni_top50.pkl')
prob_uni.to_sql('unigrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'unigrams_tb' created....")
data = pd.read_sql_table('unigrams_tb', engine)
print('UNIGRAMS\n')
print(data.head())

# Load Bigrams
prob_bi = pd.read_pickle('data/prob_bi_top5.pkl')
prob_bi.to_sql('bigrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'bigrams_tb' created....")
print('BIGRAMS\n')
data = pd.read_sql_table('bigrams_tb', engine)
print(data.head())

# Load Trigrams
prob_tri = pd.read_pickle('data/prob_tri_top5.pkl')
prob_tri.to_sql('trigrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'trigrams_tb' created....")
print('TRIGRAMS\n')
data = pd.read_sql_table('trigrams_tb', engine)
print(data.head())


# Load Quadgrams
prob_quad = pd.read_pickle('data/prob_quad_top5.pkl')
prob_quad.to_sql('quadgrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'quadgrams_tb' created....")
print('QUADGRAMS\n')
data = pd.read_sql_table('quadgrams_tb', engine)
print(data.head())


# Load Pentagrams
prob_penta = pd.read_pickle('data/prob_penta_top5.pkl')
prob_penta.to_sql('pentagrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'pentagrams_tb' created....")
print('PENTAGRAMS\n')
data = pd.read_sql_table('pentagrams_tb', engine)
print(data.head())

# Load Hexagrams
prob_hexa = pd.read_pickle('data/prob_hexa_top5.pkl')
prob_hexa.to_sql('hexagrams_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'hexagrams_tb' created....")
print('HEXAGRAMS\n')
data = pd.read_sql_table('hexagrams_tb', engine)
print(data.head())


# Load Profanities
profanity_file = open('data/bad_words.txt', 'rt', encoding='utf8')
bad_words = profanity_file.readlines()
profanity_file.close()
bad_words = [w.replace('\n', '') for w in bad_words]
profanities = pd.DataFrame(bad_words, columns=['Word'])
profanities.to_sql('profanities_tb', engine, if_exists='replace', index=False)
print('-------------------------')
print("'profanities_tb' created....")
print('PROFANITIES\n')
data = pd.read_sql_table('profanities_tb', engine)
print(data.head())