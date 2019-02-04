# Old Pipeline Scripts
Descriptions of the scripts we used in an old, not very good pipeline to go from VCF to variant-score output.

## MutPred2_prep.py
Used to run the annovar annotation command from python. Currently,there is an exit right after the program runs annovar. But I believe this was the pipeline beginning to end.

The files that are referenced are as such:

MutPred2_scores = "/data/users/trberg/staging/MutPred_scores.csv"
This looks like the file MutPred_scores_example.csv. This is an example of MutPred2 outputs when it scores protein sequences.

target_file = "/data/users/trberg/staging/MutPred2_processing/MutPred2_annovar_ready/annovar_ready_ribosomal_variants.txt"

This looks like the file MutPredMutations.txt. Basically a slightly modified VCF file that is necessary for annovar to process.

## annovar.py
Was used to take the data from the annovar annotated vcf files to map it a python class object. I don't remember where I was using this.

## NBS_ProcessFAA4MutPred2.py
Converts the annovar FAA protein sequences output into the MutPred2 input file format

## MutPred2_SCORING.py
Probably safe to ignore. Not sure there's anything to salvage here.

## MutPred_combine.py
I used this to combine multiple mutpred2 output files from multiple threads into one master output file.