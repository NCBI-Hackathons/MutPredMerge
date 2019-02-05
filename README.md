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
* Snakemake - use snakemake as the workflow system

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

