import pandas as pd
import os
import argparse
import json

def mutpred2_parse(row, temp):
    mechs  = []
    probs  = []
    p_vals = []

    mech_info = row.filter(regex=("Molecular mechanisms.*"))[0].split("; ")
    for m_pr_p in mech_info:
        if m_pr_p == ".":
            m = "."
            p = "."
            pr = "."
        else:
            m = m_pr_p.split(" (")[0].strip().replace(" ", "_")

            pr_p    = m_pr_p.split(" (")[1].strip(")")
            pr = pr_p.split(" | ")[0].split(" = ")[1]
            p  = pr_p.split(" | ")[1].split(" = ")[1]

        mechs.append(m)
        probs.append(pr)
        p_vals.append(p)
    
    temp[row["ID"].split("|")[0]] = ";".join([
        "MPMANN=" + row["ID"],
        "MPMTOOL=" + "MP2",
        "MPMSCORE=" + str(row["MutPred2 score"]),
        "MPMMECH=" + ",".join(mechs),
        "MPMPROB=" + ",".join(probs),
        "MPMPVAL=" + ",".join(p_vals)
    ])
    #print (json.dumps(temp, indent=2))
    

def mutpred_indel_parse(row, temp):
    mechs  = []
    probs  = []
    p_vals = []

    mech_info = row.filter(regex=("Molecular mechanisms.*"))[0].split("; ")
    for m_p in mech_info:
        if m_p == ".":
            m = "."
            p = "."
        else:
            m_p = m_p.strip(";")
            m = m_p.split("(")[0].strip().replace(" ", "_")
            p = m_p.split("(")[1].strip(")").split("=")[1].strip()

        mechs.append(m)
        probs.append(".")
        p_vals.append(p)
    
    temp[row["ID"].split("|")[0]] = ";".join([
        "MPMANN=" + row["ID"],
        "MPMTOOL=" + "MPI",
        "MPMSCORE=" + str(row["MutPred indel score"]),
        "MPMMECH=" + ",".join(mechs),
        "MPMPROB=" + ",".join(probs),
        "MPMPVAL=" + ",".join(p_vals)
    ])

def mutpred_lof_parse(row, temp):
    mechs  = []
    probs  = []
    p_vals = []

    mech_info = row.filter(regex=("Molecular mechanisms.*"))[0].split("; ")
    for m_p in mech_info:
        if m_p == ".":
            m = "."
            p = "."
        else:
            m_p = m_p.strip(";")
            m = m_p.split("(")[0]
            p = m_p.split("(")[1].strip(")").split("=")[1]

        mechs.append(m)
        probs.append(".")
        p_vals.append(p)
    
    temp[row["ID"].split("|")[0]] = ";".join([
        "MPMANN=" + row["ID"],
        "MPMTOOL=" + "MPL",
        "MPMSCORE=" + str(row["MutPred LOF score"]),
        "MPMMECH=" + ",".join(mechs),
        "MPMPROB=" + ",".join(probs),
        "MPMPVAL=" + ",".join(p_vals)
    ])

def merge():

    merged_variants = {}

    score_dir = os.listdir("intermediates/scores/")
    for filename in score_dir:
        mutType = filename.split(".")[1].split("_")[0]
        
        if mutType == 'missense':
            data = pd.read_csv("intermediates/scores/" + filename)
            data.fillna(".", inplace=True)
            data.apply(lambda row: mutpred2_parse(row, merged_variants), axis=1)

        elif mutType == 'LOF':
            cols = ["ID", "MutPred LOF score", "Molecular mechanisms"]
            data = pd.read_csv("intermediates/scores/" + filename, names=cols, header=None, sep="|")
            data.fillna(".", inplace=True)
            data["ID"] = data["ID"].apply(lambda x: x.split("(")[0].rstrip().replace(" ", "|"))
            data.apply(lambda row: mutpred_lof_parse(row, merged_variants), axis=1)

        elif mutType == 'indels' and filename.split(".")[-1] != 'mat':
            cols = ["ID", "MutPred indel score", "Molecular mechanisms"]
            data = pd.read_csv("intermediates/scores/" + filename, names=cols, header=None, sep="|")
            data.fillna(".", inplace=True)
            data["ID"] = data["ID"].apply(lambda x: x.split("(")[0].rstrip().replace(" ", "|"))
            data.apply(lambda row: mutpred_indel_parse(row, merged_variants), axis=1)

        else:
            pass
    return merged_variants


def map_to_chrom(merged_results, base):
    mapped_variants = {}
    exonic_variants = pd.read_csv("intermediates/annovar/" + base + ".exonic_variant_function", sep="\t", header=None)
    exonic_variants = exonic_variants[[0, 11, 12, 14, 15]].set_index(0)
    exonic_variants.columns = ["CHROM", "POS", "REF", "ALT"]
    #exonic_variants = exonic_variants.to_dict('index')

    for line in merged_results.keys():
        row = exonic_variants.loc[line]
        
        mapped_variants[str(row["CHROM"]) + "," + str(row["POS"]) + "," + str(row["REF"]) + "," + str(row["ALT"])] = merged_results[line]
    return mapped_variants


def map_to_vcf(mapped_variants, base, vcf):
    orig_vcf = vcf
    annotated_vcf = "data/" + base + ".annotated.vcf"
    unscored_vcf = "data/" + base + ".unscored.vcf"
    scored_vcf = "data/" + base + ".scored.vcf"

    INFO = """##source=MutPredMerge
##INFO=<ID=MPMANN,Number=1,Type=String,Description="Annotation from ANNOVAR in the transcript and protein space">
##INFO=<ID=MPMTOOL,Number=1,Type=String,Description="Name of software run from MutPred suite: MP2 for MutPred2 (missense), MPL for MutPred-LOF (loss-of-function) and MPI for MutPred-Indel (non-frameshifting indels)">
##INFO=<ID=MPMSCORE,Number=1,Type=Float,Description="General (pathogenicity) prediction score">
##INFO=<ID=MPMMECH,Number=.,Type=String,Description="Predicted molecular mechanisms that meet software threshold">
##INFO=<ID=MPMPROB,Number=.,Type=Float,Description="Posterior probability for each molecular mechanism">
##INFO=<ID=MPMPVAL,Number=.,Type=Float,Description="P-value for each molecular mechanism">
"""

    with open(orig_vcf, 'rU') as orig:
        with open(annotated_vcf, "w") as out:
            with open(scored_vcf, "w") as scored:
                with open(unscored_vcf, "w") as unscored:
                    for line in orig:
                        if line.startswith("##"):
                            out.write(line)
                            scored.write(line)
                            unscored.write(line)
                        elif line.startswith("#C"):
                            out.write(INFO)
                            out.write(line)
                            scored.write(INFO)
                            scored.write(line)
                            unscored.write(line)
                        else:
                            split_line = line.split("\t")
                            var_key = ",".join([split_line[0], split_line[1], split_line[3], split_line[4] ])
                            try:
                                MPM_INFO = mapped_variants[var_key]
                                line = line.split("\t")
                                line[7] = line[7] + ";" + MPM_INFO
                                line = "\t".join(line)
                                out.write(line)
                                scored.write(line)
                                
                            except KeyError:
                                out.write(line)
                                unscored.write(line)
    #print (json.dumps(mapped_variants, indent=2))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Combine all the scored variants into vcf files.')
    parser.add_argument('--vcf', type=str, nargs=1,
                        help='the original vcf filename')

    args = parser.parse_args()

    vcf = args.vcf[0]
    print (vcf)

    base = vcf.split("/")[-1].split(".")[-2]
    print (base)

    merged_variants = merge()
    mapped_variants = map_to_chrom(merged_variants, base)
    map_to_vcf(mapped_variants, base, vcf)
