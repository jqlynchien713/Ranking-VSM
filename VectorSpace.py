from pprint import pprint
from Parser import Parser
import util
import math
import nltk

class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #query list
    queryList = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None

    #idf
    idf = []

    #queryVector for feedback
    queryVector = []

    def __init__(self, documents=[], queryList=[], weightType = ''):
        self.documentVectors=[]
        self.queryList = queryList
        self.weightType = weightType
        self.parser = Parser()
        if(len(documents)>0 and len(queryList)>0):
            self.build(documents, self.queryList)


    def build(self,documents, query):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents+query)
        if self.weightType == 'tfidf':
            self.idf = self.buildIdf(documents)
        self.documentVectors = [self.makeVector(document) for document in documents]


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


    def buildIdf(self, documents):
        idf_v = [0] * len(self.vectorKeywordIndex)
        for word in self.vectorKeywordIndex.keys():
            n_containing = sum(1 for doc in documents if word in doc.split(' '))
            idf_v[self.vectorKeywordIndex[word]] =(7034 / (1 + n_containing))
        return idf_v


    def makeVector(self, wordString):
        """ @pre: unique(vectorIndex) """
        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)

        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1 #Use simple Term Count Model
            
        # tf-idf
        for i, v in enumerate(vector):
            if v!=0:
                v_tf = v/len(wordList) #tf
                if self.weightType == 'tfidf':
                    v = v_tf*self.idf[i] #idf
            else:
                continue
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        return ratings


    def search(self, relevanceType):
        """ search for documents that match based on a list of terms """
        self.queryVector = self.buildQueryVector(self.queryList)

        if relevanceType == 'cs':
            ratings = [util.cosine(self.queryVector, documentVector) for documentVector in self.documentVectors]
        elif relevanceType == 'eu':
            ratings = [util.euclidean(self.queryVector, documentVector) for documentVector in self.documentVectors]
        return ratings

    def feedback(self,first_doc):
        ''' get first result from #1-3, then get noun and verb to make new query to get relevance feedback '''
        text = nltk.word_tokenize(first_doc)
        pos_tagged = nltk.pos_tag(text)

        feedbackQueryList = [e[0] for e in filter(lambda x:x[1][:2]=='NN' or x[1][:2]=='VB',pos_tagged)] #
        feedbackQueryVector = self.buildQueryVector(feedbackQueryList)
        if len(self.queryVector)==0:
            self.queryVector = self.buildQueryVector(self.queryList)

        queryVector = [e+0.5*a for e, a in zip(self.queryVector,feedbackQueryVector)]
        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        return ratings
