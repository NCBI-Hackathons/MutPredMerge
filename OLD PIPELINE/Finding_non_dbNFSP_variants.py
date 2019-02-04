import csv
exonic_variants = []
reference = []
address = "unscored_inherited.txt"
with open(address, "Ur") as x:
	filereader = csv.reader(x)
	line = 1
	for row in filereader:
		row = "".join(row)
		row = row.split("\t")
		row[0] = "line" + str(line)
		variant = row[3:]
		reference.append("\t".join(variant))
		exonic_variants.append("\t".join(row))
		line += 1

print len(reference)
"""
with open("unscored_inherited_variants.txt.exonic_variant_function", "w") as x:
	for variant in exonic_variants:
		x.write(variant)
		x.write("\n")

with open("unscored_inherited_variants.txt", "w") as x:
	for variant in reference:
		x.write(variant)
		x.write("\n")
"""