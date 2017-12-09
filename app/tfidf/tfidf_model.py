from gensim import corpora,models
import logging,nltk
import os

class Myquestions(object):
    def  __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        for line in open(self.dirname,'r'):
            sentence_stop = [i for i in line.lower().split() if i not in stoplist]
            yield sentence_stop

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stoplist = set(nltk.corpus.stopwords.words('english'))
sentences = Myquestions('/media/lusong/新加卷1/full_subject.txt')
dict = corpora.Dictionary(sentences)
dict.save('dict_tfidf_stop')
corpus = [dict.doc2bow(text) for text in sentences]
corpora.MmCorpus.serialize('corpus_stop.mm',corpus)

tfidf = models.TfidfModel(corpus,dict,normalize=False)
tfidf.save('tfidf_question_stop.model')




