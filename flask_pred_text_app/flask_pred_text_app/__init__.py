from flask import Flask
import pandas as pd


app = Flask(__name__)

# read the data tables (not profanities)
prob_uni = pd.read_pickle('flask_pred_text_app/data/prob_uni_top50.pkl')
words_uni = list(prob_uni['Word1'])
prob_bi = pd.read_pickle('flask_pred_text_app/data/prob_bi_top5.pkl')
prob_tri = pd.read_pickle('flask_pred_text_app/data/prob_tri_top5.pkl')
prob_quad = pd.read_pickle('flask_pred_text_app/data/prob_quad_top5.pkl')
prob_penta = pd.read_pickle('flask_pred_text_app/data/prob_penta_top5.pkl')
prob_hexa = pd.read_pickle('flask_pred_text_app/data/prob_hexa_top5.pkl')
prob_hepta = pd.read_pickle('flask_pred_text_app/data/prob_hepta_top5.pkl')
prob_octa = pd.read_pickle('flask_pred_text_app/data/prob_octa_top5.pkl')
prob_nona = pd.read_pickle('flask_pred_text_app/data/prob_nona_top5.pkl')
prob_deca = pd.read_pickle('flask_pred_text_app/data/prob_deca_top5.pkl')

# get a list of profanities
profanity_file = open('flask_pred_text_app/data/bad_words.txt', 'rt', encoding='utf8')
bad_words = profanity_file.readlines()
profanity_file.close()
bad_words = [w.replace('\n', '') for w in bad_words]
bad_pattern = bad_words[0]
for item in bad_words[1:]:
    bad_pattern = bad_pattern + '|' + item

from flask_pred_text_app import routes