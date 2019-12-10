import pickle
import pandas as pd
import numpy as np
import os


#--> Get the Corpus Info
def get_corpus_info():
    # open the txt files
    file_news = open("rawdata/news.txt", mode="r", encoding='utf8')  ## open 'news.txt'
    file_blogs = open("rawdata/blogs.txt", mode="r", encoding='utf8')  ## open 'blogs.txt'
    file_twitter = open("rawdata/twitter.txt", mode="r", encoding='utf8')  ## open 'twitter.txt'

    # get the file sizes
    size_news = round(os.stat("rawdata/news.txt").st_size / (10 ** 6), 2)  ## 'news.txt' size
    size_blogs = round(os.stat("rawdata/blogs.txt").st_size / (10 ** 6), 2)  ## 'blogs.txt' size
    size_twitter = round(os.stat("rawdata/twitter.txt").st_size / (10 ** 6), 2)  ## 'twitter.txt' size

    # read the whole file in lines
    lines_news = file_news.readlines()  ## read 'news.txt'
    lines_blogs = file_blogs.readlines()  ## read 'blogs.txt'
    lines_twitter = file_twitter.readlines()  ## read 'twitter.txt'

    # get the number of lines
    num_lines_news = len(lines_news)  ## 'news.txt' number of lines
    num_lines_blogs = len(lines_blogs)  ## 'blogs.txt' number of lines
    num_lines_twitter = len(lines_twitter)  ## 'twitter.txt' number of liness


    ## get number of words
    num_words_news = 0  ## 'news.txt' number of words
    num_words_blogs = 0  ## 'blogs.txt' number of words
    num_words_twitter = 0  ## 'twitter.txt' number of words



    # get min & max num of words in a line
        ## 'news.txt'
    min_num_words_news = len(lines_news[0].split())
    max_num_words_news = len(lines_news[0].split())
    for l in lines_news:
        words = l.split()
        num_words_news += len(words)
        if len(words) < min_num_words_news:
            min_num_words_news = len(words)
        if len(words) > max_num_words_news:
            max_num_words_news = len(words)

        ## 'blogs.txt'
    min_num_words_blogs = len(lines_blogs[0].split())  ## minimum number of words in a line
    max_num_words_blogs = len(lines_blogs[0].split())  ## minimum number of words in a line
    for l in lines_blogs:
        words = l.split()
        num_words_blogs += len(words)
        if len(words) < min_num_words_blogs:
            min_num_words_blogs = len(words)
        if len(words) > max_num_words_blogs:
            max_num_words_blogs = len(words)

        ## 'twitter.txt'
    min_num_words_twitter = len(lines_twitter[0].split())  ## minimum number of words in a line
    max_num_words_twitter = len(lines_twitter[0].split())  ## minimum number of words in a line
    for l in lines_twitter:
        words = l.split()
        num_words_twitter += len(words)
        if len(words) < min_num_words_twitter:
            min_num_words_twitter = len(words)
        if len(words) > max_num_words_twitter:
            max_num_words_twitter = len(words)


    # close the files
    file_news.close()
    file_blogs.close()
    file_twitter.close()


    # create an info DataFrame of the corpus
    corpus_info = pd.DataFrame({'Size': [size_news, size_blogs, size_twitter,
                                         size_news + size_blogs + size_twitter],
                                'Lines': [num_lines_news, num_lines_blogs, num_lines_twitter,
                                          num_lines_news + num_lines_blogs + num_lines_twitter],
                                'Words': [num_words_news, num_words_blogs, num_words_twitter,
                                          num_words_news + num_words_blogs + num_words_twitter],
                                'Min Words': [min_num_words_news, min_num_words_blogs, min_num_words_twitter,
                                              min(min_num_words_news, min(min_num_words_blogs, min_num_words_twitter))],
                                'Max Words': [max_num_words_news, max_num_words_blogs, max_num_words_twitter,
                                              max(max_num_words_news,
                                                  max(max_num_words_blogs, max_num_words_twitter))]},
                               index=['News', 'Blogs', 'Twitter', 'Corpus'])
    # pickle the objects for later use
    corpus_info.to_pickle('pickles/corpus_info.pkl')


    return corpus_info


#--> Split a Txt File into Mutliple Smaller Files
def split_bigfile(filename, lines_per_file = 2000):
    small_file = None
    i = 0
    with open('rawdata/'+filename+'.txt', encoding='utf8') as file:
        for line_num, line in enumerate(file):
            if line_num % lines_per_file == 0:
                if small_file:
                    small_file.close()
                i += 1
                small_filename = 'rawdata/'+filename+'_splitted/'+filename+'_{}.txt'.format(i)
                small_file = open(small_filename, "w", encoding='utf8')
            small_file.write(line)
        if small_file:
            small_file.close()



get_corpus_info()

split_bigfile('news')
split_bigfile('blogs', lines_per_file=2000)
split_bigfile('twitter')