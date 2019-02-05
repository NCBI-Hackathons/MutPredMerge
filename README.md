# Mutpred_Consolidation
Consolidation of tools in the MutPred Package
Mutation Prediction Integration

*Motivation*
The MutPred suite (http://mutpred.mutdb.org/) is a collection of machine learning tools that predict the pathogenicity of protein-coding variants to infer molecular mechanisms of disease. MutPred tools currently support inputs and outputs aimed at the protein biochemistry world. That is fasta formatted amino acid sequences are used as the primary input. The challenges with this input format are that isolated amino acid sequences cannot be easily assigned to genomic locations and the genomics community (including clinical genomics) works in the chromosomal space and uses VCF (Varant Call Format: https://en.wikipedia.org/wiki/Variant_Call_Format) as their primary file format. 

MutPred offers several advantages over other functional prediction methods (ref), list:   
Hence, if MutPred were able to "read" a VCF and perform its calculations on variants that map to conincal forms of conceptually translated amino acid sequences, then MutPred's acceptance and use would increase in the genomics community to ...

The above goal can be acheived through a scalable integrated workflow that combines genomic tools designed to annoate data sotred in VCF files with tools in the MutPred Suite. In terms of performance, this workflow should be to analyze VCF files containing an order of 100,000 variants in a few hours and be extensible with respect to VCF annoation. Becuase MutPred tools operation on idividual amino acid sequences, and in some cases subsquences, scalablity can beacheived through standard parallelization using multiple computer nodes within a cluster. Making such a system portable for wide use is enabled by employing a standardized worflow system and containerizing tools that have complex installation requirements.  

![alt text](https://github.com/NCBI-Hackathons/Mutpred_Consolidation/blob/master/mutpred_workflow.png "Workflow")

Goals
---------
* Implment a workflow manager to run and parallelize the pipeline
* Use/compare different VCF annoation tools
* Integrate data from other pipelines

Annotation
----------
* ANNOVAR 
* Cravat

Workflow
--------
* Snakemake: at first it looked like this would not be possible. When Snakemake was installed with conda, and then run, an error resulted. The output has several python messages and a final message pointing to an issue with a datrie dependencie. Google Searches with snakemake datrie yielded: 
(1) https://bitbucket.org/snakemake/snakemake/issues/934/installation-failed-in-python-37 and 
(2) https://github.com/pytries/datrie/issues/52 indicating the error was related to snakemake's dependencie on datrie. The thread in (1) hinted to the solution in it's last message (2018-12-19) and (2) provided an additional explaination with the workaround by andersgs (2018-07-05) 

```wget https://github.com/pytries/datrie/archive/0.7.1.tar.gz
tar xf 0.7.1.tar.gz
cd datrie-0.7.1
./update_c.sh 
python3.7 setup.py build
python3.7 setup.py install ```  

Once the above lines were executed, snakemake worked. 

Parallezation
-------------
Missense are the most abundant might consider splitting these up  
2 minutes per missense variant currently

Stretch Goals
-------------
* Dockerize
* Integration of MutPred tools

How to use
------------
Installation options:

Testing
--------------
1. Initial pipeline:  
  VCF file -> annovar -> translations (protein sequences) + mutations(SNPs, Indels, Splice Variants)  
  protein sequences -> MutPred Software Suite -> outputs  
  Descripe in Snakemake file  
  Run the pipelline  
  Verify output  
2. Parallelize operation  
  groups of protein sequences -> MutPred Software Suite -> outputs

Additional Functionality

