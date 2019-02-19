
configfile: "config.json"
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
ALL_THREADS = [num for num in range(config["num_threads"])]
NUM_THREADS = max(ALL_THREADS) + 1

# final output is the input
# for glob_wildcard, will likely need an expand here

rule all:
	input:
		expand(MAIN_DIR + "intermediates/faa/" + BASE + ".{vartype}_{num_threads}.faa", vartype=VARTYPES, num_threads=ALL_THREADS),
		expand(MAIN_DIR + "intermediates/scores/" + BASE + ".{vartype}_{num_threads}_output.txt", vartype=VARTYPES, num_threads=ALL_THREADS),
		MAIN_DIR + "data/" + BASE + ".annotated.vcf",
		MAIN_DIR + "data/" + BASE + ".scored.vcf",
		MAIN_DIR + "data/" + BASE + ".unscored.vcf"


ruleorder: annovar_convert > annovar_annotate > splitter > coding_change > MutPred2 > MutPred_LOF > MutPred_indel > Merge

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
		expand(MAIN_DIR + "intermediates/splits/" + BASE + ".{vartype}_{num_threads}.exonic_variant_function", vartype=VARTYPES, num_threads=ALL_THREADS)
	threads:
		NUM_THREADS
	shell:
		"{params.cmd} -threads " + str(NUM_THREADS) + " --target {input} --output {params.output_folder}"

rule coding_change:
	params:
			cmd="perl tools/annovar/coding_change.pl",
			ops="-includesnp",
			refGeneMrna="tools/annovar/humandb/hg19_refGeneMrna.fa",
			refGene="tools/annovar/humandb/hg19_refGene.txt"
	input:
			MAIN_DIR + "intermediates/splits/" + BASE + ".{vartype}_{num_threads}.exonic_variant_function"
	output:
			MAIN_DIR + "intermediates/faa/" + BASE + ".{vartype}_{num_threads}.faa"
	threads:
		1
	shell:
			"{params.cmd} {input} {params.refGene} {params.refGeneMrna} {params.ops} > {output}"


rule MutPred2:
	input:
		MAIN_DIR + "intermediates/faa/" + BASE + ".missense_{num_threads}.faa"
	output:
		MP2=MAIN_DIR + "intermediates/scores/" + BASE + ".missense_{num_threads}_output.txt"
	threads:
		2
	shell: 
		"cd tools/mutpred2.0 && ./run_mutpred2.sh -i {input} -p 1 -c 1 -b 0 -t 0.05 -f 2 -o {output}"


rule MutPred_LOF:
	params:
		outfile_prefix=MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_{num_threads}"
	input:	
		MAIN_DIR + "intermediates/faa/" + BASE + ".LOF_{num_threads}.faa"
	output:
		MPL=MAIN_DIR + "intermediates/scores/" + BASE + ".LOF_{num_threads}_output.txt"
	threads:
		6
	shell:
		"cd tools/MutPredLOF && ./run_MutPredLOF.sh v91/ {input} {params.outfile_prefix}"

rule MutPred_indel:
	params:
		outfile_prefix=MAIN_DIR + "intermediates/scores/" + BASE + ".indels_{num_threads}"
	input:
		MAIN_DIR + "intermediates/faa/" + BASE + ".indels_{num_threads}.faa"
	output:
		MPI=MAIN_DIR + "intermediates/scores/" + BASE + ".indels_{num_threads}_output.txt"
	threads:
		6
	shell:
		"cd tools/MutPredIndel_compiled && ./run_MutPredIndel.sh v91/ {input} {params.outfile_prefix}"

rule Merge:
	input:
		expand(MAIN_DIR + "intermediates/scores/" + BASE + ".{vartype}_{num_threads}_output.txt", vartype=VARTYPES, num_threads=ALL_THREADS)
	output: 
		MAIN_DIR + "data/" + BASE + ".annotated.vcf",
		MAIN_DIR + "data/" + BASE + ".scored.vcf",
		MAIN_DIR + "data/" + BASE + ".unscored.vcf"
	threads:
		NUM_THREADS
	shell:
		"python mutpred_merge.py --vcf " + VCFFILE

