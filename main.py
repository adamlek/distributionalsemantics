# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:29:13 2016

@author: Adam Ek

Class1: Read data with Random Indexing
    input: .txt file
    output: success_rate, sentences, {vocabulary: [word_vector][random_vector][word_count_doc_n], documents: ...}

Class2: Read data and apply weights
    input: {vocabulary: [word_vector][random_vector][word_count_doc_n], documents: ...}
    output {vocabulary: [word_vector][WEIGHTED_random_vector][word_count_doc_n], documents: ...}

Class3: Read contexts
    input: list of sentences
    output: {vocabulary: [word_vector][random_vector][word_count_doc_n], documents: ...}

Class4: Evaluate data
    command: 'sim word1 word2'
    input: two words
    output: similarity between them

    command: 'top word'
    input: one word
    output: top similar words

Class5: Data operations
    input: command
    output: message

"""

from randomindexer import RandomIndexing
from randomindexer import Weighter
from randomindexer import ReadContexts
from randomindexer import Similarity
from randomindexer import DataOptions

import sys
import numpy as np

def main():
    ri = RandomIndexing()
    wgt = Weighter('tf-idf')
    dt = DataOptions()

    print('Welcome to Distributial Semantics with Random Indexing\n')
    new_data = False
    settings = ['CBOW', 1]
    #< init data
    while True:
        if new_data:
            print('Enter new data by typing "new <path>" , "set setting value" to change context settings and finish by typing "apply"\n')
        else:
            print('Enter new data source by typing "new <path>" and load saved data by typing "load <name>"\n')

        setup = input('> ')
        setup = setup.split()

        if len(setup) == 0:
            print('Please try again')

        #< !!!
        elif setup[0] == 'load':
            if not new_data:
                try:
                    dist_data = dt.load(setup[1])
                    break
                except Exception as e:
                    print('Try again\n', e)

        #< input a new data source
        elif setup[0] == 'new':
            new_data = True
#            sentences, dist_data = ri.process_data(['/home/usr1/git/dist_data/test_doc_0.txt', '/home/usr1/git/dist_data/test_doc_1.txt', '/home/usr1/git/dist_data/austen-emma.txt'])
            sentences, dist_data = ri.process_data(['/home/usr1/git/dist_data/test_doc_3.txt', '/home/usr1/git/dist_data/test_doc_4.txt'])


        #< apply precessed data
        elif setup[0] == 'apply':
            if new_data:
                docs = []
                for doc in dist_data['documents']:
                    docs.append(dist_data['documents'][doc]['words'])

                for word in dist_data['vocabulary']:
                    dist_data['vocabulary'][word]['random_vector'] = wgt.weight(dist_data['vocabulary'][word]['random_vector'], dist_data['vocabulary'][word]['word_count'], docs)

                rc = ReadContexts(dist_data['vocabulary'], settings[0], settings[1])
                dist_data['vocabulary'], dist_data['data_info'] = rc.read_data(sentences)
                dt = DataOptions(dist_data['vocabulary'], dist_data['documents'], dist_data['data_info'])
                break
            else:
                print('Invalid command')

#        #< change settings before data is applied with command "apply"
        elif setup[0] == 'set':
            if setup[1] == 'context':
                settings[0] = setup[2]
            elif setup[1] == 'window':
                settings[1] = setup[2]
            else:
                print('Invalid input')

        #< exit
        elif setup[0] == 'exit':
            sys.exit()

        else:
            print('Invalid input')

    #< User interface after data has been loaded
    print('Type "sim <word1> <word2>" for similarity between two words, "top <word>" for top 3 similar words, "help" to display availible commands and "exit" to quit\n')
    sim = Similarity(dist_data['vocabulary'])

    while True:
        choice = input('> ')
        input_args = choice.split()

        #< empty input
        if not input_args:
            print('Please try again\n')

        #< RI similarity between words
        elif input_args[0] == 'sim':
            try:
                sim_res = sim.cosine(input_args[1].lower(), input_args[2].lower())
                if sim_res == str(sim_res):
                    print(sim_res)
                else:
                        print('Cosine similarity between "{0}" and "{1}" is\n {2}\n'.format(input_args[1], input_args[2], sim_res))
            except Exception as e:
                print('Invalid input for "sim"\n', e)

        elif input_args[0] == 'top':
            try:
                top_res = sim.top(input_args[1].lower())
                if top_res == str(top_res):
                    print(top_res)
                else:
                    print('Top similar words for "{0}" is:'.format(input_args[1]))
                    for i, (dist, word) in enumerate(top_res):
                        print(i+1, dist[0][0], word)
                    print('')
            except Exception as e:
                print(e)
                print('Invalid input for "top"\n')

        #< quit
        elif input_args[0] == 'exit':
           break

        #< save data
        elif input_args[0] == 'save':
            try:
                print(dt.save(input_args[1], dist_data['vocabulary'], dist_data['documents'], dist_data['data_info']))
            except Exception as e:
                print('Error\n{0}'.format(e))

        #< update data
#        elif input_args[0] == 'update':
#            try:
#                new_data = ri.process_data(input_args[1:])
#                random_i = wgt.weighter(new_data[2])
#                rc = ReadContexts(random_i, data['data_info']['context'], data['data_info']['window'])
#                data = rc.read_data(process_data[1])
#            except Exception as e:
#                print('Update failed\n{0}'.format(e))
#
        #< info about dataset or word
        elif input_args[0] == 'info':
            try:
                dt.info(input_args[1].lower())

            except:
                dt.info()

        #< help information
        elif input_args[0] == 'help':
            print('- Semantic operations')
            print('\t"sim <word> <word>" similarity between two words')
            print('\t"top <word>" top 3 similar words')
            print('\t"lsasim <word> <word>" LSA/HAL-like similarity between two words')
            print('- Data operations')
            print('\t"save <name>" save current data')
            print('\t"update <path>" update the data with a new textfile')
            print('\t"info" information about the data')
            print('\t"info <word>" information about a word')
            print('\t"set <context/window> <value>" to set context type(CBOW or skip-gram) or window size')
            print('- ETC')
            print('\t"exit" to quit\n')

        else:
           print('Unrecognized command')

if __name__ == '__main__':
    main()



