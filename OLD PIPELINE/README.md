# Old Pipeline Scripts
Descriptions of the scripts we used in an old, not very good pipeline to go from VCF to variant-score output.

## MutPred2_prep.py
Used to run the annovar annotation command from python. Problably not necessary

## annovar.py
Was used to take the data from the annovar annotated vcf files to map it a python class object. I don't remember where I was using this.

## NBS_ProcessFAA4MutPred2.py
Converts the annovar FAA protein sequences output into the MutPred2 input file format

## MutPred2_SCORING.py
Probably safe to ignore. Not sure there's anything to salvage here.

## MutPred_combine.py
I used this to combine multiple mutpred2 output files from multiple threads into one master output file.