import re
import string
import os

profanity_file = open('rawdata/bad_words.txt', 'rt', encoding='utf8')
bad_words = profanity_file.readlines()
profanity_file.close()
bad_words = [w.replace('\n', '') for w in bad_words]
bad_pattern = bad_words[0]
for item in bad_words[1:]:
    bad_pattern = bad_pattern + '|' + item


def clean_text(text, profanity=False):
    ## to lower case
    text = [t.lower() for t in text]
    ## remove text containing numbers
    dig_pattern = re.compile(r'\w*\d\w*')
    text = [re.sub(dig_pattern, '', t) for t in text]
    ## remove punctuations
    text = [re.sub('[%s]' % re.escape(string.punctuation), '', t) for t in text]
    ## remove urls
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = [re.sub(url_pattern, '', t) for t in text]
    ## remove words containing non-english characters
    neng_pattern = re.compile(r'[A-z]*[^\x01-\x7F]+[A-z]*')
    text = [re.sub(neng_pattern, '', t) for t in text]
    ## remove non-sense words
    nsens_pattern = re.compile(r'\\w*(kk|nn|zz|'
                               r'aaa|bbb|ccc|ddd|eee|fff|ggg|hhh|jjj|lll|ppp|qqq|rrr|vvv|xxx|'
                               r'iiii|ssss|wwww|mmmmm|ooooo|ttttt|uuuuu|yyyyy)+\\w*\\s*')
    text = [re.sub(nsens_pattern, '', t) for t in text]

    ## profanities
    if profanity:
        text = [re.sub(bad_pattern, '', t) for t in text]

    return text

def clean_text_source(source, profanity=False):
    dir_path = 'rawdata/' + source + '_splitted'
    files_path = [dir_path + '/' + item for item in os.listdir(dir_path) if
                  os.path.isfile(os.path.join(dir_path, item))]

    for i, f in enumerate(files_path):
        file = open(f, 'rt', encoding='utf8')
        text = file.readlines()
        file.close()
        clean_txt = clean_text(text, profanity)
        ## write a new file
        dest_path = ''
        if profanity:
            dest_path = 'cleandata/' + source + '_splitted/profanity_not/' + source + '_' + format(i+1) + '.txt'
        else:
            dest_path = 'cleandata/' + source + '_splitted/' + source + '_' + format(i+1) + '.txt'
        with open(dest_path, 'wt', encoding='utf8') as f:
            for item in clean_txt:
                f.write("%s" % item)


# Uncomment to get cleaned data
#clean_text_source('news')
#clean_text_source('blogs')
#clean_text_source('twitter')

#clean_text_source('news', profanity=True)
#clean_text_source('blogs', profanity=True)
#clean_text_source('twitter', profanity=True)
