workdir: "/home/ubuntu/"

# want to get this from the command line, or a directory
VCFFILE = "data/small_sample.vcf"
BASE    = "small_sample"


#VCFFILE, = glob_wildcards("data/{vcf}.vcf")

# final output is the input
# for glob_wildcard, will likely need an expand here
rule all:
	input: BASE + ".end"

ruleorder: annovar_convert > annovar_annotate

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
		ops="--geneanno -dbtype refGene -buildver hg19"
	input:
		rules.annovar_convert.output, # output from step 1
		refdir="data_resources/annovar_reference/humandb/"
	output:
		BASE + ".end"
	shell:
		"{params.cmd} {params.ops} {input} --outfile {output}"


rule MutPred2:
	shell: "./run_mutpred2.sh -i /home/ubuntu/data/mutpred_sample_files/input_mutpred2_codingchange -p 1 -c 1 -b 0 -t 0.05 -f 2 -o /home/ubuntu/data/mutpred_sample_files/input_mutpred2_codingchange_output.txt"

rule MutPred-LOF
	shell: ./run_MutPredLOF.sh /home/ubuntu/tools/mutpred2.0/v91/ /home/ubuntu/data/mutpred_sample_files/input_mutpredlof_codingchange /home/ubuntu/data/mutpred_sample_files/input_mutpredlof_codingchange

# MutPred-indel
./run_MutPredIndel.sh /home/ubuntu/tools/mutpred2.0/v91 /home/ubuntu/data/mutpred_sample_files/input_mutpredindel_codingchange /home/ubuntu/data/mutpred_sample_files/input_mutpredindel_codingchange

