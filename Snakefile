workdir: "/Users/admin/Documents/Research/Mutpred_Consolidation"

# want to get this from the command line, or a directory
VCFFILE = "data/small_sample.vcf"
BASE    = "small_sample"


#VCFFILE, = glob_wildcards("data/{vcf}.vcf")
VARTYPES = ["missense", "LOF", "indels"]
ANNOVAR = ["exonic_variant_function, log, variant_function"]


# final output is the input
# for glob_wildcard, will likely need an expand here
rule all:
	input:
		"intermediates/annovar/" + BASE + ".full.avinput",
		"intermediates/annovar/" + BASE + ".exonic_variant_function",
		expand("intermediates/splits/" + BASE + ".{vartype}_0.exonic_variant_function", vartype=VARTYPES),
		## expand("/Users/admin/Documents/Research/Mutpred_Consolidation/intermediates/splits/" + BASE + ".missense_0.exonic_variant_function", vartype=VARTYPES),
                expand("intermediates/faa/" + BASE + ".{vartype}_0.faa", vartype=VARTYPES)
		
		# "data/mutpred_sample_files/outputs/input_mutpredlof_codingchange",
		# "data/mutpred_sample_files/outputs/input_mutpred2_codingchange_output.txt",
		# "data/mutpred_sample_files/outputs/input_mutpredindel_codingchange"
		

ruleorder: annovar_convert > annovar_annotate > splitter > coding_change # > MutPred2 > MutPred_LOF > MutPred_indel 

# first run annovar - there are two steps
rule annovar_convert:
	params:
		cmd="tools/annovar/convert2annovar.pl",
		ops="-format vcf4 -allsample -withfreq -includeinfo"
	input:
		VCFFILE
	output:
		"intermediates/annovar/" + BASE + ".full.avinput"
	shell:
		"{params.cmd} {params.ops} {input} > {output}"

rule annovar_annotate:
	params:
		cmd="tools/annovar/annotate_variation.pl",
		ops="--geneanno -dbtype refGene -buildver hg19",
		annotate = "intermediates/annovar/" + BASE
	input:
		rules.annovar_convert.output, # output from step 1
		refdir="tools/annovar/humandb/"
	output:
		var_fxn="intermediates/annovar/" + BASE + ".exonic_variant_function"
	shell:
		"{params.cmd} {params.ops} {input} --outfile {params.annotate}"

rule splitter:
	params:
		cmd="python splitter_module.py",
                output_folder="intermediates/splits/"
	input:
                rules.annovar_annotate.output.var_fxn
	output:
		var_split="intermediates/splits/" + BASE + ".{vartype}_0.exonic_variant_function"
	shell:
		"{params.cmd} --target {input} --output {params.output_folder}"

rule coding_change:
        params:
                cmd="tools/annovar/coding_change.pl",
                ops="-includesnp",
                refGeneMrna="tools/annovar/humandb/hg19_refGeneMrna.fa",
                refGene="tools/annovar/humandb/hg19_refGene.txt"
        input:
                rules.splitter.output.var_split
        output:
                faa_file="intermediates/faa/" + BASE + ".{vartype}_0.faa"
        shell:
                "{params.cmd} {params.ops} {input} {params.refGene} {params.refGeneMrna} > {output}"

"""
rule MutPred2:
	input:
		"intermediates/faa/" + BASE + ".missense_0.faa"
	output:
		"scores/" + BASE + ".mutpred2.missense_0.csv"

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
"""
rule end:
	output: BASE + ".end"
