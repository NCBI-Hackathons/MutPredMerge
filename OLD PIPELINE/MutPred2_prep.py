import annovar
import csv
import gzip
import os
from subprocess import call
import sys

MutPred2_scores = "/data/users/trberg/staging/MutPred_scores.csv"
base = "/data/users/trberg/"
target_file = "/data/users/trberg/staging/MutPred2_processing/MutPred2_annovar_ready/annovar_ready_ribosomal_variants.txt"
#target_file = "/data/nfs/annovar/datasets/MutPredMutations.hg19.exonic_variant_function"
#target_file = "/data/users/trberg/staging/MutPred2_processing/MutPred2_annovar_ready/top_1000_nonsynonymous_variants.txt.exonic_variant_function"
base_file_name = "Ribosomal_variants"
annovar = base + "annovar"
command = ("perl %s/annotate_variation.pl -build hg19 " + target_file + " %s/humandb") % (annovar, annovar)
#print command
call(command, shell=True)
exit()

scored_variants = {}

with open(MutPred2_scores, "Ur") as x:
	filereader = csv.reader(x)
	count = 0
	for row in filereader:
		if row[0] == "ID":
			pass
		elif row[2] == "-":
			pass
		else:
			score = float(row[2])
			variant = tuple(row[0].split("_")[:4])
			scored_variants[variant] = score
print len(scored_variants)

print "scores loaded"

rank={}
exonic_data = {}
unscored_variants = []
anno = annovar.annovar(target_file + ".exonic_variant_function")
with open(target_file, "Ur") as x:
	counted = 0
	filereader = csv.reader(x)
	for row in filereader:
		print '\r',
		print counted,
		sys.stdout.flush()
		tool = annovar.tools(anno, row)
		if tool.get_mut() != "nonsynonymous SNV" and tool.get_mut() != "nonframeshift substitution":
			pass
		else:
			print tool.get_var()
			exit()
			isRanked = False
			try:
				rank[tool.get_gene()]
				isRanked = True
			except:
				isRanked = False
			isScored = False
			try:
				scored_variants[tool.get_var()]
				isScored = True
			except:
				isScored = False
			
			variant = tool.get_var()
			if not isScored:# and isRanked:
				counted += 1
				unscored_variants.append(tool.get_var())
				exonic_data[tool.get_var()] = "".join(row)

print "scored filtered"

print "exonic data", len(exonic_data)
print "unscored variant", len(unscored_variants)

def chunks(l, n):
    #Yield successive n-sized chunks from l.
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
size = (len(unscored_variants)/4 + 1)
#size = 8000
print "chunked into %s sized files" % size
chunked = list(chunks(list(unscored_variants), size))
print len(chunked), "files created"

for number in range(len(chunked)):
	address = ("MutPred2_processing/MutPred2_annovar_ready/" + base_file_name + "_%s.txt") % (number)
	with open(address, "w") as x:
		for i in chunked[number]:
			variant = (i[0], str(i[1]), str(i[1]), i[2], i[3])
			x.write("\t".join(variant))
			x.write('\n')
	path = ("MutPred2_processing/MutPred2_annovar_ready/" + base_file_name + "_%s.txt.exonic_variant_function") % (number)
	with open(path, "w") as x:
		count = 1
		for i in chunked[number]:
			variant_line = exonic_data[i].split("\t")
			variant_line[0] = "line" + str(count)
			variant = "\t".join(variant_line)
			x.write(variant)
			x.write("\n")
			count += 1
print "files written"
for number in range(len(chunked)):
	annovar = base + "annovar"
	command = ("perl %s/coding_change.pl -includesnp "+ base +"staging/MutPred2_processing/MutPred2_annovar_ready/" + base_file_name + "_%s.txt.exonic_variant_function %s/humandb/hg19_refGene.txt %s/humandb/hg19_refGeneMrna.fa > " + base + "staging/MutPred2_processing/MutPred2_faa_files/" + base_file_name + "_%s.faa") % (annovar, number, annovar, annovar, number)
	print "creating .faa file %s" % number
	call(command, shell=True)

print "annovar annotated"	

chunked = [num for num in range(len(chunked))]
for number in range(len(chunked)):
	command = ("python MutPred2_processing/NBS_ProcessFAA4MutPred2.py " + base_file_name + "_%s") % (number)
	#print command
	call(command, shell=True)

print "NBS process run"

for number in range(len(chunked)):
	delete_path = ("MutPred2_processing/MutPred2_annovar_ready/" + base_file_name + "_%s.txt.exonic_variant_function") % (number)
	os.remove(delete_path)
	delete_path = ("MutPred2_processing/MutPred2_annovar_ready/" + base_file_name + "_%s.txt") % (number)
	os.remove(delete_path)
	delete_path = (base + "staging/MutPred2_processing/MutPred2_faa_files/" + base_file_name + "_%s.faa") % (number)
	os.remove(delete_path)


print "MutPred2 processor run"
file_number = len(chunked)
for number in range(file_number):
	command = ("/data/common/MutPred2/mutpred2_beta_v1/run_mutpred2.sh -i /data/users/trberg/staging/MutPred2_processing/MutPred2_ready/" + base_file_name + "_%s_MutPred2.faa -p 0 -c 1 -b 0 -k 5 -o /data/users/trberg/staging/MutPred2_processing/MutPred2_results/" + base_file_name + "_%s_mutpred2_scores.csv &") % (number,number)
	#call(command, shell=True)
	print command

print "cd /data/common/MutPred2/mutpred2_beta_v1"



