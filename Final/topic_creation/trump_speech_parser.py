# -*- coding: utf-8 -*-

import requests
from nltk import tokenize
from bs4 import BeautifulSoup

# Each one of these is an speech
pids = [ 110306, 116597, 117813, 117775, 117790, 117815, 117791, 117935, 118047, 123199, 119744, 122534, 123515, 119503, 119165, 119175, 123197, 119176, 123198, 119806, 119805, 119196, 119198, 119199, 119197, 119177, 119195, 119194, 119204, 119178, 119205, 119193, 119206, 119190, 119209, 119208, 119207, 119192, 119189, 119191, 119203, 119200, 119201, 119202, 119179, 119166, 119167, 119168, 119169, 119170, 119171, 123517, 119173, 119180, 119172, 119174, 119183, 123516, 119184, 119185, 119186, 119875, 119187, 119188, 123518, 123519, 119181, 119182, 122537, 122535, 123513, 123514, 122536 ]

strs_to_delete = [u'—', u':', u'[]', u' – ', '...']

all_text = ''

# Loop over all speeches
for pid in pids:
    page = requests.get('http://www.presidency.ucsb.edu/ws/index.php?pid=%s' % pid)
    soup = BeautifulSoup(page.content, 'html.parser')

    # This is the speech itself, with some garbage as well
    displaytext = soup.find(class_="displaytext")

    # extract italics because they are annotations
    i_tags = displaytext.find_all('i')
    for i in i_tags:
        i.extract()

    # there are a few things that these can contain
    for t in displaytext:
        if hasattr(t, 'text'):
            all_text += t.text
        elif t.__class__.__name__ == 'NavigableString': 
            all_text += t
        else:
            print("oops!")
        
        # Just to make sure the words are separate
        all_text += ' '


# Remove garbage
for str_to_delete in strs_to_delete:
    all_text = all_text.replace(str_to_delete, ' ')

# Split into sentences
toks = tokenize.sent_tokenize(all_text)

with open('speeches.txt', 'w') as f:
    for tok in toks:
        line = tok + '\n'
        line = line.encode('utf8')
        f.write(line)
    
