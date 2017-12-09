from gensim import models,corpora,similarities
import logging,linecache
#load model & data
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = models.TfidfModel.load('../tfidf_question_stop.model')
corpus = corpora.MmCorpus('../corpus_stop.mm')
dictionary = corpora.Dictionary.load('../dict_tfidf_stop')
tfidf_corpus = model[corpus]

# similarity = similarities.Similarity('Similarity-tfidf-stop-index',tfidf_corpus,num_features=len(dictionary))
# similarity = similarities.MatrixSimilarity(tfidf_corpus)
# similarity.save('Similarity-tfidf-stop-index')
similarity = similarities.MatrixSimilarity.load('Similarity-tfidf-stop-index')
while(True):
    print("请输入需要查找相似度的语句")
    ques_raw=input()
    ques_corpus = dictionary.doc2bow(ques_raw.split())
    similarity.num_best = 5

    ques_corpus_tfidf = model[ques_corpus]

    print("查找结果如下：")
    n_best_ans = similarity[ques_corpus_tfidf]
    for items in n_best_ans:
        print('问题编号：',items[0],'相似度：',items[1])
        print(linecache.getline('/media/lusong/新加卷1/full_subject.txt',items[0]+1))
