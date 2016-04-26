=== udconv.py ===

The script does the following:
- maps the tags in XPOSTAG column (see the conllu format) 
  to the universal tags and writes results to the UPOSTAG 
  column;
- replaces unconventional relation names in the DEPREL 
  column to their universal counterparts;
- replace spaces in wordforms and lemmata with a specified 
  delimeter, default is "__" (double underscore)
- reports some format inconsistencies (if any);
- logs freq. lists of:
  -- space containg wordforms 
     (log section: === FORMSPLIT ===);
  -- universal postags 
     (log section: === UPOSTAG ===);
  -- lang. specific postags 
     (log section: === XPOSTAG ===);
  -- dependency relations
     (log section: === DEPREL ===).


usage: udconv.py [-h] [-i INFILE] [-o OUTFILE] [-J MWTJOINER] [-l LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        input file in conllu format
  -o OUTFILE, --outfile OUTFILE
                        input file in conllu format
  -J MWTJOINER, --mwtjoiner MWTJOINER
                        multi-word token joiner symbol (deaful is "__" [double
                        underscore])
  -l LOG, --log LOG     log file, if not set redirects to STDOUT

example: python udconv.py -i puupankki.conllu.txt -o kk-ud-train.conllu -l udconv.log
