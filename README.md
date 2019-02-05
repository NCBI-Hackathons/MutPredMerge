# Mutpred_Consolidation
Consolidation of tools in the MutPred Package
Mutation Prediction Integration


*Motivation*
MutPred suite - machine learning tools to predict the pathogenicity of protein-coding variants and infer molecular mechanisms of disease
Currently, support inputs and outputs aimed at the protein biochemistry world
The genomics community works in the chromosomal space in VCFs

Access MutPred2 http://mutpred.mutdb.org/

NEED TO BRIDGE THE GAP!!
Build integrated workflow to support this and address issues with scalability - need to be able to run these tools on upto 100,000 variants
Think about ways to make this more generic


![alt text](https://github.com/NCBI-Hackathons/Mutpred_Consolidation/blob/master/mutpred_workflow.png "Workflow")

Goals
---------
* Implment a workflow manager to run and parallelize the pipeline
* Use/compare VCF annoation tools
* Integrate data from other pipelines

Annotation
----------
* ANNOVAR 
* Cravat

Workflow
--------
* Snakemake - use snakemake as the workflow system - at first it looked like this would not be possible. When Snakemake was installed with conda, and then run, an error resulted. The output has several python messages and a final message pointing to an issue with a datrie dependencie. Google Searches with snakemake datrie yielded: 
(1) https://bitbucket.org/snakemake/snakemake/issues/934/installation-failed-in-python-37 and 
(2) https://github.com/pytries/datrie/issues/52 indicating the error was related to snakemake's dependencie on datrie. The thread in (1) hinted to the solution in it's last message (2018-12-19) and (2) provided an additional explaination with the workaround by andersgs (2018-07-05) 

`wget https://github.com/pytries/datrie/archive/0.7.1.tar.gz 
tar xf 0.7.1.tar.gz 
cd datrie-0.7.1 
./update_c.sh 
python3.7 setup.py build 
python3.7 setup.py install`

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

