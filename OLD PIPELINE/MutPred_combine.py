import csv
import os

path = "MutPred2_scores"
all_lines = []
unique_set = {}
for i in os.listdir(path):
	with open(path + "/" + i, "Ur") as x:
		filereader = csv.reader(x)
		Indexed = False
		ID = 0
		Substitution = 1
		Score = 2
		Hypothesis = 3
		ConfHypothesis = 4
		VeryConfidentHypothesis = 5
		TopKmechanisms = 6
		Remarks = 7
		for row in filereader:
			if not Indexed:
				ID = row.index("ID")
				Substitution = row.index("Substitution")
				Score = row.index("MutPred2 score")
				Hypothesis = row.index("Actionable hypotheses")
				ConfHypothesis = row.index("Confident hypotheses")
				VeryConfidentHypothesis = row.index("Very confident hypotheses")
				TopKmechanisms = row.index("Top k mechanisms")
				Remarks = row.index("Remarks")
				Indexed = True
			else:
				info = row[ID].split("_")
				info = info[1:]
				if info[0].startswith("chr"):
					info[0] = info[0][3:]
				else:
					pass
				var = tuple(info[:4])
				info = "_".join(info)
				unique_set[var] = (info, row[Substitution], row[Score], row[Hypothesis], row[ConfHypothesis], row[VeryConfidentHypothesis], row[TopKmechanisms], row[Remarks])
				all_lines.append((info, row[Substitution], row[Score], row[Hypothesis], row[ConfHypothesis], row[VeryConfidentHypothesis], row[TopKmechanisms], row[Remarks]))

print len(unique_set.keys())

all_lines = sorted(unique_set.values())

with open("MutPred_scores.csv", "w") as x:
	x.write("ID,Substitution,MutPred2 score,Actionable hypotheses,Confident hypotheses,Very confident hypotheses,Top k mechanisms,Remarks\n")
	for i in all_lines:
		i = ",".join(i)
		x.write(i)
		x.write("\n")

