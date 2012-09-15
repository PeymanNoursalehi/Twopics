"""
Ambidextrous
Sep, 2012

Use Oxford Thesaurus to get synonyms for all words (w) possible
Use UNTIndexer to get top n (4) synonyms for each w
Add the synonyms to the overall tweet

Dependencies: Oxford XML, NLTK
"""
import sys
import shelve
from collections import defaultdict
from nltk import word_tokenize, pos_tag
from xml.dom import minidom

def error():
    print 'Usage: supply thesaurus_xml n all_tweets_file'
    print 'Quitting now'
    sys.exit()

def get_sanitized_pos(penn_pos):
    sanitized = ''
    if 'NN' in penn_pos:
        sanitized = 'n'
    if 'RB' in penn_pos:
        sanitized = 'r'
    if 'JJ' in penn_pos:
        sanitized = 'a'
    if 'VB' in penn_pos:
        sanitized = 'v'
    return sanitized

def weed_out_lexelts(tweets_file):
    lexelts = []
    with open(tweets_file, 'r') as twh:
        for line in twh:    
            line = line.strip().split(' :: ')
            lexelts_temp = pos_tag(word_tokenize(line))
            lexelts_temp[1] = get_sanitized_pos(lexelts_temp[1])
            lexelts.extend(lexelts_temp)
    return lexelts

def explore_thesaurus_for_lexelt(word, pos, all_lexsub_elements):
    # childNodes[1] and [3] are word and pos
    # Derive one lexelt that matches the lexelt(word, pos)
    # The lexelt returned should and will be a single node
    lexelt = filter( (lambda L: L.childNodes[1].firstChild.data == word and L.childNodes[3].firstChild.data == pos), all_lexsub_elements)[0]
    syns = []
    senses = lexelt.getElementsByTagName('sense')
    for sense in senses:    
        synonyms = sense.getElementsByTagName('synonyms')
        for syn in synonyms:
            if ' ' not in syn:
                syns.append(syn.firstChild.data)
    return syns

def prepare_syndb(thesaurus, lexelts):
    xml_thesaurus = minidom.parse(thesaurus)
    pers_obj = shelve.open('oxf.syns.db')
    temp_obj = defaultdict(dict)
    all_lexsub_elements = xml_thesaurus.getElementsByTagName('lexelt')
    for word, pos in lexelts:
        syns = explore_thesaurus_for_lexelt(word, pos, all_lexsub_elements)
        temp_obj[word][pos] = syns

    pers_obj['1'] = temp_obj
    pers_obj.close()

def prepare_SaLSA_input_file(tweets_file):
    # IDs are assigned sequentially to the tweets
    # So they should match what we have later in the
    # aggregated tweets
    file_id = 0
    with open(tweets_file, 'r') as twh:
        for line in twh:
            fho = open('SaLSAInputFiles/{0}'.format(file_id), 'w')

            line = line.strip().split(' :: ')[1]
            line_array = line.split(' ')
            for i in xrange(0, len(line_array)):
                temp_line = ' '.join(line_array[:i]) + ' <head>' + line_array[i] + '</head> ' + ' '.join(line_array[i+1:])
                fho.write(temp_line + '\n')

def main():
    if len(sys.args) != 4:
        error()
    thesaurus = sys.argv[1]
    n = sys.argv[2]
    tweets_file = sys.argv[3]

    # List of tuples
    lexelts = weed_out_lexelts(tweets_file)
    # Persistent object from Oxford
    prepare_syndb(thesaurus, lexelts)
    # Each word is a head word - multiple files
    prepare_SaLSA_input_file(tweets_file)

if __name__ == '__main__':
    main()
