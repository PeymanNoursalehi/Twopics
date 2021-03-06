"""
Ambidextrous
Sep 2012

Wrapper around SaLSA to get top n 
synonyms for all words in the tweets
using the Oxford thesaurus

Input: SaLSA input files: 1400
Output from SaLSA: bla bla bla, then 
All synonyms scores = [(score, 'word'), ...] - reverse ranked

n = 4
"""
import re
import sys
import commands
from collections import defaultdict

def complain():
    print 'Usage: supply path_to_input_files all_tweets_file'
    print 'Quitting now'
    sys.exit()

def word_presence(word):
    return re.search('[A-Za-z]', word)

def run_salsa(path_to_input_files): 
    files = os.listdir(path_to_input_files)
    extensions = defaultdict(dict)
    for f in files:
        extensions[f] = []
        print 'Processing ', f
        out = commands.getstatusoutput('python salsa.py {0}/{1} > temp.out.SaLSA.txt'.format(path_to_input_files, f))
        all_lines = []
        with open('temp.out.SaLSA.txt', 'r') as fho:
            for line in fho:
                line = line.strip()
                all_lines.append(line)

        output_lines = filter( (lambda L: 'All synonyms scores' in L), all_lines)
        for out_line in output_lines:
            words_of_interest = out_line.split(' = ')[1].split(', ')
            words_of_interest = filter(word_presence, words_of_interest)
            words_of_interest = words_of_interest[:4]
            for w in words_of_interest:
                w = w.strip("'()")

        extensions[f].append(words_of_interest) # all words found

    return extensions

def merge_and_extend(all_tweets_file, extensions):
    

def main():
    if len(sys.argv != 3):
        complain()
    path_to_input_files = sys.argv[1]
    all_tweets_file = sys.argv[2]

    # Get a hashmap of the extensions keyed on the tweet / file ID
    extensions = run_salsa(path_to_input_files)
    merge_and_extend(all_tweets_file, extensions)

if __name__ == '__main__':
    main()


