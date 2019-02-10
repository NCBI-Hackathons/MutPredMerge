

# want to get this from the command line, or a directory


# paths and directories

# This needs to be the absolute path to the current directory
MAIN_DIR = "/data/common/MutPredMerge/"

# This can be either the relative or absolute path to your target vcf file
VCFFILE = "data/small_sample.vcf"

# Make sure this is the same as the filename of your VCF file, just minus the ".vcf".
BASE    = "small_sample"


# wildcars
VARTYPES = ["missense", "LOF", "indels"]


# final output is the input
# for glob_wildcard, will likely need an expand here
rule all:
	input:
		MAIN_DIR + "intermediates/annovar/" + BASE + ".full.avinput",
		MAIN_DIR + "intermediates/annovar/" + BASE + ".exonic_variant_function",
		expand(MAIN_DIR + "intermediates/splits/" + BASE + ".{vartype}_0.exonic_variant_function", vartype=VARTYPES),
        expand(MAIN_DIR + "intermediates/faa/" + BASE + ".{vartype}_0.faa", vartype=VARTYPES),
		MAIN_DIR + "intermediates/scores/" + BASE + ".missense_0.csv",
		MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_0_output.txt",
		MAIN_DIR + "intermediates/scores/" + BASE + ".indels_0_output.txt",
		MAIN_DIR + "data/" + BASE + ".vcf.tmp"


ruleorder: annovar_convert > annovar_annotate > splitter > coding_change > MutPred2 > MutPred_LOF > MutPred_indel > merge

# first run annovar - there are two steps
rule annovar_convert:
	params:
		cmd="tools/annovar/convert2annovar.pl",
		ops="-format vcf4 -allsample -withfreq -includeinfo"
	input:
		VCFFILE
	output:
		MAIN_DIR + "intermediates/annovar/" + BASE + ".full.avinput"
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
		var_fxn=MAIN_DIR + "intermediates/annovar/" + BASE + ".exonic_variant_function"
	shell:
		"{params.cmd} {params.ops} {input} --outfile {params.annotate}"

rule splitter:
	params:
		cmd="python splitter_module.py",
                output_folder="intermediates/splits/"
	input:
                rules.annovar_annotate.output.var_fxn
	output:
		splits=MAIN_DIR + "intermediates/splits/" + BASE + ".{vartype}_0.exonic_variant_function"
	shell:
		"{params.cmd} --target {input} --output {params.output_folder}"

rule coding_change:
        params:
                cmd="tools/annovar/coding_change.pl",
                ops="-includesnp",
                refGeneMrna="tools/annovar/humandb/hg19_refGeneMrna.fa",
                refGene="tools/annovar/humandb/hg19_refGene.txt"
        input:
                rules.splitter.output.splits
        output:
                faa_file=MAIN_DIR + "intermediates/faa/" + BASE + ".{vartype}_0.faa"
        shell:
                "{params.cmd} {params.ops} {input} {params.refGene} {params.refGeneMrna} > {output}"


rule MutPred2:
	input:
		MAIN_DIR + "intermediates/faa/" + BASE + ".missense_0.faa"
	output:
		MAIN_DIR + "intermediates/scores/" + BASE + ".missense_0.csv"
	shell: 
		"tools/mutpred2.0/run_mutpred2.sh -i {input} -p 1 -c 1 -b 0 -t 0.05 -f 2 -o {output}"


rule MutPred_LOF:
	params:
		outfile_prefix=MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_0"
	input:	
		MAIN_DIR + "intermediates/faa/" + BASE + ".LOF_0.faa"
	output:
		MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_0_output.txt"
	shell:
		"cd tools/MutPredLOF && ./run_MutPredLOF.sh v91/ {input} {params.outfile_prefix}"

rule MutPred_indel:
	params:
		outfile_prefix=MAIN_DIR + "intermediates/scores/" + BASE + ".indels_0"
	input:
		MAIN_DIR + "intermediates/faa/" + BASE + ".indels_0.faa"
	output:
		MAIN_DIR + "intermediates/scores/" + BASE + ".indels_0_output.txt"
	shell:
		"cd tools/MutPredIndel_compiled && ./run_MutPredIndel.sh v91/ {input} {params.outfile_prefix}"


rule merge:
	input:
		MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_0_output.txt",
		MAIN_DIR + "intermediates/scores/" + BASE + ".indels_0_output.txt",
		MAIN_DIR + "intermediates/scores/" + BASE + ".missense_0.csv"
	output: 
		MAIN_DIR + "data/" + BASE + ".vcf.tmp"
	shell:
		"python mutpred_merge.py --base " + BASE

