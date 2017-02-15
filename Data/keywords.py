"""THIS CODE IS FROM PYTEXTRANK CREATOR PACO's GITHUB. IT WAS ORIGINALLY SPLIT INTO
4 PARTS BUT COMBINING ALL 4 HERE AND ADAPTING FOR THIS PROJECT"""

#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

def step_1(json_file, output1):
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



def step_2(prev_output1, output2):
    """ Stage 2:
          * collect and normalize the key phrases from a parsed document
    
         INPUTS: <stage1>
         OUTPUT: JSON format `RankedLexeme(text, rank, ids, pos)`"""
    sys.stdout=open(output2,"w")
    if __name__ == "__main__":
        path = prev_output1
        graph, ranks = textrank.text_rank(path)

        textrank.render_ranks(graph, ranks)

         # output as JSON

        for rl in textrank.normalize_key_phrases(path, ranks):
            print(textrank.pretty_print(rl._asdict()))
        sys.stdout.close()

def step_3(prev_output1, prev_output2, output3):
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



step_1('dat/mih.json', 'out1.json')
step_2('out1.json', 'out2.json')
step_3('out1.json', 'out2.json', 'out3.json')



