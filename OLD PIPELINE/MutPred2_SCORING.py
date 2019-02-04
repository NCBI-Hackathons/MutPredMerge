import csv
import annovar

genes = {}
gene_list = "Rankedgenemaniaset.txt"
with open(gene_list, "Ur") as x:
	filereader = csv.reader(x)
	for row in filereader:
		row = "".join(row)
		row = row.split("\t")
		gene = row[1]
		rank = int(row[0])
		genes[gene] = rank


chroms = [str(num) for num in range(1, 23)]
chroms.append("Y")
chroms.append("X")
#chroms = ["20"]

def MP2_address(chrom):
	address = "MutPred2/"
	filename = "dbnsfp_chr%s_mutpred.txt" % (chrom)
	return address + filename


##{chromosome: {chrom:position:ref:alt : annotated_annovar_row}}
def variant_sort(file_address):
	variant_dict = {}
	for num in chroms:
		variant_dict[num] = {}
	with open(file_address, "Ur") as x:
		anno = annovar.annovar(file_address)
		filereader = csv.reader(x)
		for row in filereader:
			tool = annovar.tools(anno, row)
			mutation = tool.get_mut()
			gene = tool.get_gene()
			if mutation != "nonsynonymous SNV":
				pass
			else:
				try:
					if genes[gene] <= 2205:
						variant = tool.get_var()
						if len(variant[2]) > 1:
							pass
						else:
							chrom = variant[0]
							position = int(variant[1])
							variant = ":".join(variant)
							variant_dict[chrom][variant] = "".join(row)
					else:
						pass
				except:
					pass

	return variant_dict

##{chrom:position:ref:alt : [exonic variant data, mutpred2 data]}
def variant_score(variant_list):
	Scoring_Variants = {}
	for chrom in variant_list.keys():
		print chrom
		with open(MP2_address(chrom), "Ur") as scoring:
			MP_filereader = csv.reader(scoring)
			for MP_row in MP_filereader:
				MP_row = "".join(MP_row)
				MP_row_list = MP_row.split("\t")
				scored_variant = MP_row_list[0]
				stuff = scored_variant.split(":")
				position = int(stuff[1])
				try:
					variant_list[chrom][scored_variant]
					Scoring_Variants[scored_variant] = ("".join(variant_list[chrom][scored_variant]).split("\t") + MP_row.split("\t"))
				except:
					pass
		print len(Scoring_Variants.keys())
	return Scoring_Variants




patient_baseName = "Patient_Inherited_variants.txt"
sibling_baseName = "Sibling_Inherited_variants.txt"
address = "MutPred2_processing/MutPred2_annovar_ready/"

patient_file_address = address + patient_baseName + ".exonic_variant_function"
sibling_file_address = address + sibling_baseName + ".exonic_variant_function"

#patient_file_address = "/data/users/trberg/Staging/MutPred2_processing/MutPred2_annovar_ready/CADD_ready_variants.txt.exonic_variant_function"

all_variants = []
patient_variants = variant_sort(patient_file_address)
count = 0
for i in patient_variants.keys():
	count += len(patient_variants[i].keys())

sibling_variants = variant_sort(sibling_file_address)
count = 0
for i in sibling_variants.keys():
	count += len(sibling_variants[i].keys())


patient_variants_list = []
for k,v in patient_variants.items():
	for k_variant in v.keys():
		patient_variants_list.append(k_variant)
		
sibling_variants_list = []
for k,v in sibling_variants.items():
	for k_variant in v.keys():
		sibling_variants_list.append(k_variant)

print "patient variants", len(set(patient_variants_list) - set(sibling_variants_list))
print "sibling variants", len(set(sibling_variants_list) - set(patient_variants_list))

patient_variants = set(patient_variants_list) - set(sibling_variants_list)
sibling_variants = set(sibling_variants_list) - set(patient_variants_list)

with open("scored_inherited_patients_2205.txt", "w") as writing:
	for variant in patient_variants:

		writing.write(variant)
		writing.write("\n")

with open("scored_inherited_siblings_2205.txt", 'w') as writing:
	for variant in sibling_variants:

		writing.write(variant)
		writing.write("\n")


exit()


all_variants = list((patient_variants_list - sibling_variants_list).union(sibling_variants_list - patient_variants_list))
print "all unique variants", len(all_variants)

scored_variants = []
scored_patients = variant_score(patient_variants)
scored_siblings = variant_score(sibling_variants)
scored_variants = scored_patients.keys() + scored_siblings.keys()
scored_variants = set(scored_variants)
print "scored variants", len(scored_variants)


not_scored = (set(all_variants) - set(scored_variants))
print "not scored", len(not_scored)
	

with open("unscored_inherited_2205.txt", "w") as writing:
	for i in not_scored:
		chrom = i.split(":")[0]
		try:
			variant = patient_variants[chrom][i]
		except:
			variant = sibling_variants[chrom][i]
		writing.write(variant)
		writing.write("\n")
"""
with open("scored_inherited_patients.txt", "w") as writing:
	for variant in scored_patients.keys():
		writing.write("\t".join(scored_patients[variant]))
		writing.write("\n")

with open("scored_inherited_siblings.txt", 'w') as writing:
	for variant in scored_siblings.keys():
		writing.write("\t".join(scored_siblings[variant]))
		writing.write("\n")
"""

