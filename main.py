import argparse
from VectorSpace import VectorSpace
from VS_blob import VectorSpace_B
import sys, getopt
import os
import time

# convert doc filepath to list
def docConverter(doc_list):
    documents = []
    doc_name = []
    for e in os.listdir(doc_list):
        if e[0] == '.':
            continue
        else:
            f = open(os.path.join(doc_list,e),'r')
            ret = f.read()
            documents.append(ret)
            doc_name.append(e[:-4])
            f.close()
    return documents, doc_name

def showResults(scores, doc_name, weightType, relevanceType):
    if weightType == 'tf':
        weightType = 'TF'
    elif weightType == 'tfidf':
        weightType = 'TF-IDF'
    relevanceType = 'Cosine Similarity' if relevanceType == 'cs' else 'Euclidean Distance'
    print(f'{weightType} Weighting + {relevanceType}')
    print('News', 'Score', sep='\t\t')
    print('---------', '---------', sep='\t')
    result = 0
    while result < 10:
        m = max(scores)
        i = scores.index(m)
        try:
            print(doc_name[i], m, sep='\t')
        except:
            print(i, m)
        scores[i] = 0
        result+=1

def main(argv):
    doc_list = ''
    query = ''
    relevanceType = ''
    weightType = ''
    feedback = False
    try:
        opts, args = getopt.getopt(argv,"d:w:r:q:f",["doc=","weight=", "relevance=", "query="])
    except getopt.GetoptError:
        print('main.py -d <doc_list_folder> -w <weight_type> -r <relevance_type> -q \'<querylist>\'')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <doc_list_folder> -w <weight_type> -r <relevance_type> -q \'<querylist>\'')
            sys.exit()
        elif opt in ("-d", "--doc"):
            doc_list = arg
        elif opt in ('-q', '--query'):
            query = arg
        elif opt in ('-w', '--weight'):
            weightType = arg
        elif opt in ('-r', '--relevance'):
            relevanceType = arg
        elif opt in ('-f', '--feedback'):
            feedback = True
    query = query.split(' ')
    documents, doc_name = docConverter(doc_list)
    v = VectorSpace(documents, query, weightType)
    scores = v.search(relevanceType)
    if feedback:
        first_doc = doc_name[scores.index(max(scores))]
        f = open(os.path.join(doc_list,f'{first_doc}.txt'),'r')
        ret = f.read()
        fq = v.feedback(ret)
        f.close()
        weightType = 'Feedback Queries + ' + weightType
        showResults(fq, doc_name, weightType, relevanceType)
    else:
        showResults(scores, doc_name, weightType, relevanceType)

if __name__ == '__main__':
    main(sys.argv[1:])