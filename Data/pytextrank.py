"""THIS CODE IS FROM PYTEXTRANK CREATOR PACO's GITHUB. IT WAS ORIGINALLY SPLIT INTO
4 PARTS BUT COMBINING ALL 4 HERE AND ADAPTING FOR THIS PROJECT"""

#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank
import math



def step_1(json_file, output1 = 'output1.json'):
## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format
##
## INPUTS: <stage0>
## OUTPUT: JSON format `ParsedGraf(id, sha1, graf)`
    sys.stdout=open(output1,"w")

    path = json_file

    for graf in textrank.parse_doc(textrank.json_iter(path), force_encode=False):
        print(textrank.pretty_print(graf._asdict()))
    sys.stdout.close()



def step_2(prev_output1= 'output1.json', output2 ='output2.json'):
    """ Stage 2:
          * collect and normalize the key phrases from a parsed document
    
         INPUTS: <stage1>
         OUTPUT: JSON format `RankedLexeme(text, rank, ids, pos)`"""
 
    
    if __name__ == "__main__":
        # print "START OF STEP 2"
        path = prev_output1
        graph, ranks = textrank.text_rank(path)

        textrank.render_ranks(graph, ranks)

         # output as JSON
        sys.stdout=open(output2,"w")
        for rl in textrank.normalize_key_phrases(path, ranks):
            print(textrank.pretty_print(rl._asdict()))
        sys.stdout.close()
        # print "END OF STEP 2"

def step_3(prev_output1 = 'output1.json', prev_output2 = 'output2.json', output3 = 'output3.json'):
## Stage 3:
##  * calculate a significance weight for each sentence, using MinHash to
##  * approximate Jaccard distance from key phrases determined by TextRank
##
## INPUTS: <stage1> <stage2>
## OUTPUT: JSON format `SummarySent(dist, idx, text)`
    sys.stdout=open(output3, "w")
    path = prev_output2
    kernel = textrank.rank_kernel(path, force_encode=False)

    path = prev_output1

    for s in textrank.top_sentences(kernel, path, force_encode=False):
        print(textrank.pretty_print(s._asdict()))

    sys.stdout.close()



def step_4(prev_output2 = 'output2.json', prev_output3 ='output3.json', output4 = 'output4.json'):
    """
        Stage 4:
        summarize a document based on most significant sentences and key phrases
    
    INPUTS: <stage2> <stage3>
    OUTPUT: Markdown format """

    def de_byte (lexeme):
      """a cheap hack, b/c unicode is hard"""
      return lexeme[1:].strip("'")


    def de_byte_phrase (phrase):
      """a cheap hack, b/c unicode is hard"""
      return " ".join([de_byte(l) for l in phrase.split(" ")])
    

    sys.stdout=open(output4, "w")

    path = prev_output2
    phrases = ", ".join([p for p in textrank.limit_keyphrases(path, phrase_limit=12)])

    path = prev_output3
    sent_iter = sorted(textrank.limit_sentences(path, word_limit=150), key=lambda x: x[1])
    s = []

    for sent_text, idx in sent_iter:
        s.append((textrank.make_sentence([w for w in sent_text])))

    graf_text = "".join(s)
    #print phrases, type(phrases)
    print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
    sys.stdout.close()

if __name__ == "__main__":
#Example with sample json here
    # step_1('dat/mih.json', 'out1.json')
    step_1('reviews.json', 'out1.json')
    
    step_2('out1.json', 'out2.json')
    step_3('out1.json', 'out2.json', 'out3.json')
    step_4('out2.json', 'out3.json', 'out4.json')








