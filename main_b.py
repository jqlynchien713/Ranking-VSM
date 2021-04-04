import argparse
from VectorSpace import VectorSpace
from VS_blob import VectorSpace_B
import sys, getopt
import os

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

def main(argv):
    doc_list = ''
    query = ''
    try:
        opts, args = getopt.getopt(argv,"d:q:",["doc=", "query="])
    except getopt.GetoptError:
        print('main.py -d <doc_list_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <doc_list_folder>')
            sys.exit()
        elif opt in ("-d", "--doc"):
            doc_list = arg
        elif opt in ('-q', '--query'):
            query = arg
    print(doc_list)
    print(query)
    documents, doc_name = docConverter(doc_list)
    v = VectorSpace_B(documents, ['Trump','Biden', 'Taiwan','China'])
    scores = v.search()
    result = 0
    while result < 10:
        m = max(scores)
        i = scores.index(m)
        try:
            print(doc_name[i], m)
        except:
            print(i, m)
        scores[i] = 0
        result+=1

    # print('vectorKeywordIndex', v.vectorKeywordIndex)
    # print('documentVectors', v.documentVectors)
    # print('related(1)', v.related(1))
    # print('earch(["trump"])', v.search(["trump"]))

if __name__ == '__main__':
    main(sys.argv[1:])
