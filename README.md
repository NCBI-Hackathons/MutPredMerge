# MutPredMerge
Pipeline that integrates and parallelizes MutPred suite.

* [Download](http://mutpred.mutdb.org/index.html#dload) MutPred2 
* [Submit](http://mutpred.mutdb.org/index.html) a single protein mutation 

Motivation
---------
The MutPred suite (http://mutpred.mutdb.org/) is a collection of machine learning tools that predict the pathogenicity of protein-coding variants to infer molecular mechanisms of disease. MutPred takes in a fasta formatted amino acid sequences as the primary input. The challenges with this input format are that isolated amino acid sequences cannot be easily assigned to genomic locations and the genomics community (including clinical genomics) works in the chromosomal space and uses VCF (Varant Call Format: https://en.wikipedia.org/wiki/Variant_Call_Format) as their primary file format. 

The MutPred suite offers several advantages over other functional prediction methods:
* Tools in the MutPred suite have been shown to be among the top-performing methods in independent assessments and community-wide experiments
* Apart from general pathogenicity scores, the MutPred tools return a ranked list of putative molecular mechanisms, thus generating hypotheses for further experimental follow-up.

Hence, if MutPred were to ingest a VCF containing DNA sequence variants and perform its calculations on those variants that map to conincal forms of conceptually translated amino acid sequences, then MutPred's acceptance and use would increase in the genomics community to ultimately aid in clinical DNA sequence analaysis. In particular MutPred's prediction capabiliies could improve the annoation of variants of uncertain significance.

The above goal can be acheived through a scalable integrated workflow that combines genomic tools designed to annoate data sotred in VCF files with tools in the MutPred Suite. In terms of performance, this workflow should be to analyze VCF files containing an order of 100,000 variants in a few hours and be extensible with respect to VCF annoation. Becuase MutPred tools operation on idividual amino acid sequences, and in some cases subsquences, scalablity can beacheived through standard parallelization using multiple computer nodes within a cluster. Making such a system portable for wide use is enabled by employing a standardized worflow system and containerizing tools that have complex installation requirements.  

**Workflow** ![Here](https://github.com/NCBI-Hackathons/Mutpred_Consolidation/blob/master/mutpred_workflow.png "Conceptual Workflow")
* [Link](https://docs.google.com/drawings/d/1K82kxgp6OYccRhUak_vzbA3sk6ERMYB-eNRHvFq8JGo/edit?usp=sharing) to Workflow

Future Directions
-----------------
* Implement support for other annotation tools - SNPeff, VARANT, OpenCRAVAT 
* Think about containerization and accessibility to users
* Scale up to cloud and HPC environments

Installation and Dependencies
--------
* Snakemake: Current conda installation of Snakemake has datrie dependency failure:
See bug:
(1) https://bitbucket.org/snakemake/snakemake/issues/934/installation-failed-in-python-37 and 
(2) https://github.com/pytries/datrie/issues/52 

Update datrie dependency first. 
``` 
wget https://github.com/pytries/datrie/archive/0.7.1.tar.gz
tar xf 0.7.1.tar.gz
cd datrie-0.7.1
./update_c.sh 
python3.7 setup.py build
python3.7 setup.py install  
```

Normal conda installation of Snakemake should work

Usage
------------
Installation options: install snakemake, and dependent software (TBD)
Obtain the Snakefile

To run a pipleline type
>snakemake

[Slides](https://docs.google.com/presentation/d/1Fp9yuV2slaYAni1wY5unc3VICNFA83dt0pRXeipHnmo/edit?usp=sharing)


Cite
----
In Process: [Manuscript](https://docs.google.com/document/d/1vBUD3H7PPvaJc4gL45TGOKKsatZuMZtkQfMggRceGec/edit?usp=sharing)

Pejaver V, Urresti J, Lugo-Martinez J, Pagel KA, Lin GN, Nam H, Mort M, Cooper DN, Sebat J, Iakoucheva LM, Mooney SD, Radivojac P. MutPred2: inferring the molecular and phenotypic impact of amino acid variants. bioRxiv 134981; doi: https://doi.org/10.1101/134981.
