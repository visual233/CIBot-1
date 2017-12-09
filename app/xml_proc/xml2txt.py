# import modules & set up logging
from gensim.models import word2vec
import xml.etree.ElementTree as ET
import logging
f = open('/media/lusong/新加卷/full_subject.txt','w')

for event,elem in ET.iterparse("/media/lusong/新加卷/FullOct2007.xml", events=(['end'])):
    # if elem.tag in ['subject', 'content', 'answer_item']:
    if elem.tag in ['subject']:
        f.write(elem.text.replace('<br />','')+'\n')
        elem.clear()

f.flush()
f.close()
