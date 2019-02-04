# Mutpred_Consolidation
Consolidation of tools in the MutPred Package

Mutation Prediction Integration

Motivation
MutPred suite - machine learning tools to predict the pathogenicity of protein-coding variants and infer molecular mechanisms of disease
Currently, support inputs and outputs aimed at the protein biochemistry world
The genomics community works in the chromosomal space in VCFs
NEED TO BRIDGE THE GAP!!
Build integrated workflow to support this and address issues with scalability - need to be able to run these tools on upto 100,000 variants
Think about ways to make this more generic

Workflow (editable) 

Annotation
ANNOVAR

Workflow:
Snake-make
CWL



Parallezation:
Missense are the most abundant might consider splitting these up
2 minutes per missense variant currently
