from pprint import pprint
from Parser import Parser
import util
import textblob as tb

class VectorSpace_B:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #Collection of document term vectors
    documents = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None

    #blob list
    bloblist=[]

    #query list
    queryList = []
    
    def __init__(self, documents=[], queryList=[]):
        self.parser = Parser()
        self.documentVectors=[]
        self.documents = documents
        self.bloblist = [tb.TextBlob(' '.join(self.parser.removeStopWords(self.parser.tokenise(d)))) for d in self.documents]
        print('blob done')
        self.queryList = queryList
        if(len(documents)>0 and len(queryList)>0):
            self.build(self.documents, self.queryList)

    def build(self,documents, query):
        """ Create the vector space for the passed document strings """
        print('build')
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents+query)
        print('vectorKeywordIndex done')
        self.documentVectors = [self.makeVector(blob) for blob in self.bloblist]
        print('documentVectors done')

        #print(self.vectorKeywordIndex)
        #print(self.documentVectors)


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, blob):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)

        # tf
        # blob.words = tb.WordList(self.parser.removeStopWords(self.parser.tokenise(list(blob.words))))
        print(blob.words)
        for word in blob.words:
            vector[self.vectorKeywordIndex[word]] = blob.words.count(word) / len(blob.words)

        # wordList = self.parser.tokenise(wordString)
        # wordList = self.parser.removeStopWords(wordList)
        # for word in wordList:
        #     vector[self.vectorKeywordIndex[word]] += 1 #Use simple Term Count Model
        # return [v/len(wordList) for v in vector]
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        # print('q', query)
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self):
        """ search for documents that match based on a list of terms """
        # for s in searchList:
        #     if s not in self.vectorKeywordIndex.keys():
        #         self.build(self.documents, searchList)
        #         break

        queryVector = self.buildQueryVector(self.queryList)

        # ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        ratings = [util.euclidean(queryVector, documentVector) for documentVector in self.documentVectors]
        # ratings.sort(reverse=True)
        return ratings


    

################################################################

if __name__ == '__main__':
    #test data
    documents = ["The cat in the hat disabled",
                 "A cat is a fine pet ponies.",
                 "Dogs and cats make good pets.",
                 "I haven't got a hat."]

    vectorSpace = VectorSpace(documents)

    print('vectorSpace.search(["cat"])', vectorSpace.search(["cat", 'dog', 'check']))

    print('vectorSpace.vectorKeywordIndex', vectorSpace.vectorKeywordIndex)

    print('vectorSpace.documentVectors', vectorSpace.documentVectors)

    print('vectorSpace.related(1)', vectorSpace.related(1))

###################################################
