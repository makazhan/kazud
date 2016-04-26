# -*- coding: UTF-8 -*-

import sys
import os
import argparse
import codecs
import re
import shutil


import nltk


#handle command line arguments
def cliParse():
    #define agrs
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--infile',\
                        help='input file in conllu format')
    parser.add_argument('-o','--outfile',\
                        help='input file in conllu format')
    parser.add_argument('-J','--mwtjoiner',action='store',\
                        default=u'__',
                        help='multi-word token joiner symbol (deaful is "__" [double underscore])')
    parser.add_argument('-l','--log',action='store',\
                        help='log file, if not set redirects to STDOUT')
    #parse args
    args = parser.parse_args()
    #handle the log
    if not args.log:
	args.log = sys.stdout
    else:
	try:
	    args.log = codecs.open(args.log,'w','utf-8')
	except:
	    args.log = sys.stdout
    return args


punc = {
    u'"':u'бірынғай тырнақша',\
    u'\'':u'апостроф',\
    u',':u'үтір',\
    u'.':u'нүкте',\
    u'\\':u'бэкслэш',\
    u'/':u'слэш',\
    u'\-':u'дефис',\
    u':':u'қоснүкте',\
    u';':u'үтір-нүкте',\
    u'?':u'сұрақ белгісі',\
    u'!':u'леп белгісі',\
    u'«':u'ашатын тырнақша',\
    u'»':u'жабатын тырнақша',\
    u'\—':u'тире',\
    u'“':u'ашатын тырнақша',\
    u'”':u'жабатын тырнақша',\
    u'\(':u'ашатын доғал жақша',\
    u'\)':u'жабатын доғал жақша',\
    u'\[':u'ашатын тік жақша',\
    u'\]':u'жабатын тік жақша',\
    u'\{':u'ашатын ирек жақша',\
    u'\}':u'ашатын ирек жақша',\
}


posmap = {
    'n':'NOUN',\
    'v':'VERB',\
    'sent':'PUNCT',\
    'adj':'ADJ',\
    'np':'PROPN',\
    'cm':'PUNCT',\
    'num':'NUM',\
    'prn':'PRON',\
    'cnjcoo':'CONJ',\
    'cop':'VERB',\
    'vaux':'AUX',\
    'det':'DET',\
    'post':'ADP',\
    'adv':'ADV',\
    'guio':'PUNCT',\
    'abbr':'NOUN',\
    'postadv':'PART',\
    'lpar':'PUNCT',\
    'rpar':'PUNCT',\
    'qst':'PART',\
    'cnjadv':'SCONJ',\
    'rquot':'PUNCT',\
    'lquot':'PUNCT',\
    'ij':'INTJ',\
    'sym':'SYM',\
    'mod_ass':'PART',\
    'mod':'PART',\
    'emph':'PART',\
    'cnjsub':'SCONJ',\
    '_':'_',\
}


relmap = {
    'punct':'punct',\
    'nmod':'nmod',\
    'subj':'nsubj',\
    'root':'root',\
    'nmod:poss':'nmod:poss',\
    'amod':'amod',\
    'conj':'conj',\
    'obj':'dobj',\
    '_':'_',\
    'advmod':'advmod',\
    'advcl':'advcl',\
    'cop':'cop',\
    'cc':'cc',\
    'aux':'aux',\
    'det':'det',\
    'acl':'acl',\
    'case':'case',\
    'cmpnd':'compound',\
    'nummod':'nummod',\
    'appos':'appos',\
    'ccomp':'ccomp',\
    'name':'name',\
    'disc':'discourse',\
    'parataxis':'parataxis',\
    'remnant':'remnant',\
    'csubj':'csubj',\
    'voc':'vocative',\
    'xcomp':'xcomp',\
    'mark':'mark',\
    'arg':'iobj',\
}


conllu = ['ID',\
          'FORM',\
          'LEMMA',\
          'UPOSTAG',\
          'XPOSTAG',\
          'FEATS',\
          'HEAD',\
          'DEPREL',\
          'DEPS',\
          'MISC',\
          ]
    

def convert_line(txt,ln,log,mwtjoiner='__',dlm='\t'):
    
    #don't touch sent. delims and comments
    if not txt.strip() or txt.startswith(u'#'): return None,None
    
    fields = txt.split(dlm)
    field_num = len(fields)
    
    ##log possible issues
    #wrong nnumber of fields
    if not field_num==10:
	log.write('\n[line #%d: wrong number of fields]\n%d instead of 10]\n'%(ln,field_num))
    #empty fields
    for i,e in enumerate(fields):
	if not e.strip():
	    log.write('\n[line #%d: field #%d is empty]\n'%(ln,i+1))
    #non-numeric HEAD field
    if not (fields[6].isdigit() or fields[0].count('-')):
	log.write('\n[line #%d: non-numeric HEAD]\n'%ln)
	log.write('%s\t%s\n'%(fields[0],fields[6]))
    #no pos
    if fields[4]==u'_' and not fields[0].count('-'):
	log.write('\n[line #%d: no pos]\n'%ln)
    
    ##convert
    #map pos tags
    fields[3] = posmap[fields[4]]
    #map relations
    fields[7] = relmap[fields[7]]
    #dismiss features
    fv = [e for e in fields[5].split('|') if (e and not e=='_')]
    fields[5] = '_'
    #join MWTs: word forms
    fields[1] = mwtjoiner.join(rex_anyspc.split(fields[1]))
    #join MWTs: lemmas
    fields[2] = mwtjoiner.join(rex_anyspc.split(fields[2]))
    
    return fields,fv


def main():

    args = cliParse()
    
    #stats collectors
    stats = {conllu[1]+'SPLIT':{},
             conllu[3]:{},
             conllu[4]:{},
             conllu[5]:{},
             conllu[7]:{},
             }
    
    fd = codecs.open(args.outfile,'w','utf-8')
    lines = codecs.open(args.infile,'r','utf-8').readlines()
    for i,l in enumerate(lines):
	[fields,fv] = convert_line(l.strip(),i+1,args.log,args.mwtjoiner)
	if not fields:
	    fd.write(l)
	    continue
	else:
	    fd.write('%s\n'%'\t'.join(fields))
	if fields[1].count(args.mwtjoiner):
	    k = conllu[1]+'SPLIT'
	    stats[k][fields[1]] = stats[k].get(fields[1],0) + 1
	k = conllu[5]
	for v in fv:
	    stats[k][v] = stats[k].get(v,0) + 1
	k = conllu[3]
	for k in [3,4,7]:
	    stats[conllu[k]][fields[k]] = stats[conllu[k]].get(fields[k],0) + 1	
    
    #log stats
    for f in conllu:
	if not f in stats:
	    f = f + 'SPLIT'
	    if not f in stats: continue
	args.log.write('\n=== %s ===\n'%f)
	for k,v in sorted(stats[f].iteritems(),key=lambda(x,y):(y,x),reverse=1):
	    args.log.write('%s\t%d\n'%(k,v))


if __name__=='__main__':
	main()
