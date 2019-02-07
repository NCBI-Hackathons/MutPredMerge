workdir: "/home/ubuntu/"

# want to get this from the command line, or a directory
VCFFILE = "data/small_sample.vcf"
BASE    = "small_sample"


#VCFFILE, = glob_wildcards("data/{vcf}.vcf")
VARTYPES = ["missense, LOF, indels"]

# final output is the input
# for glob_wildcard, will likely need an expand here
rule all:
	input:
		"todd-test/" + BASE + ".full.avinput",
		"todd-test/" + BASE + ".exonic_variant_function",
		"todd-test/" + BASE + ".log",
		"todd-test/" + BASE + ".variant_function",
		"/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".indels_0.exonic_variant_function",
                "/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".missense_0.exonic_variant_function",
                "/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".LOF_0.exonic_variant_function",
		"data/mutpred_sample_files/outputs/input_mutpredlof_codingchange",
		"data/mutpred_sample_files/outputs/input_mutpred2_codingchange_output.txt",
		"data/mutpred_sample_files/outputs/input_mutpredindel_codingchange"

ruleorder: annovar_convert > annovar_annotate > splitter> MutPred2 > MutPred_LOF > MutPred_indel 

# first run annovar - there are two steps
rule annovar_convert:
	params:
		cmd="tools/annovar/convert2annovar.pl",
		ops="-format vcf4 -allsample -withfreq -includeinfo"
	input:
		VCFFILE
		#expand ("data/{vcf}.vcf", vcf=VCFFILE)
	output:
		"todd-test/" + BASE + ".full.avinput"
	shell:
		"{params.cmd} {params.ops} {input} > {output}"

rule annovar_annotate:
	params:
		cmd="tools/annovar/annotate_variation.pl",
		ops="--geneanno -dbtype refGene -buildver hg19",
		annotate = "todd-test/" + BASE
	input:
		rules.annovar_convert.output, # output from step 1
		refdir="data_resources/annovar_reference/humandb/"
	output:
		"todd-test/" + BASE + ".log",
		"todd-test/" + BASE + ".variant_function",
		var_fxn="todd-test/" + BASE + ".exonic_variant_function"
	shell:
		"{params.cmd} {params.ops} {input} --outfile {params.annotate}"

rule splitter:
	params:
		cmd="python Mutpred_Consolidation/splitter_module.py",
                output="/home/ubuntu/Mutpred_Consolidation/intermediates/splits"
	input:
        	rules.annovar_annotate.output.var_fxn
	output:
		"/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".indels_0.exonic_variant_function",
		"/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".missense_0.exonic_variant_function",
		"/home/ubuntu/Mutpred_Consolidation/intermediates/splits/" + BASE + ".LOF_0.exonic_variant_function"
	shell:
		"{params.cmd} --target {input} --output /home/ubuntu/Mutpred_Consolidation/intermediates/splits"

rule MutPred2:
	input:
		"data/mutpred_sample_files/inputs/input_mutpred2_codingchange"
	output:
		"data/mutpred_sample_files/outputs/input_mutpred2_codingchange_output.txt"

	shell: "tools/mutpred2.0/run_mutpred2.sh -i {input} -p 1 -c 1 -b 0 -t 0.05 -f 2 -o {output}"

rule MutPred_LOF:
	input:	
		"data/mutpred_sample_files/inputs/input_mutpredlof_codingchange"
	output:
		"data/mutpred_sample_files/outputs/input_mutpredlof_codingchange"

	shell:
		"tools/MutPredLOF/run_MutPredLOF.sh /tools/mutpred2.0/v91/ {input} {output}"

rule MutPred_indel:
	input:
		"data/mutpred_sample_files/inputs/input_mutpredindel_codingchange"
	output:
		"data/mutpred_sample_files/outputs/input_mutpredindel_codingchange"	
	shell:
		"tools/MutPredIndel_compiled/run_MutPredIndel.sh /tools/mutpred2.0/v91/ {input} {output}"

rule end:
	output: BASE + ".end"
