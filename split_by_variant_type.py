#!/home/ubuntu/anaconda3/bin/python

import pandas as pd 
import os
import argparse
        


def processing_exonic_variant_function(path, suffix):
    
    data = pd.read_csv(path, delimiter="\t", header=None)
    data = data.applymap(str)

    if os.path.isdir("intermediates/splits/"):
        pass
    else:
        os.makedirs("intermediates/splits/")

    missense = data[data[1] == "nonsynonymous SNV"]
    missense.to_csv("intermediates/splits/%s.missense.exonic_variant_function" % suffix, sep="\t", header=False, index=False)

    indels = data[data[1].isin(["nonframeshift substitution","nonframeshift deletion","nonframeshift insertion"])]
    indels.to_csv("intermediates/splits/%s.indels.exonic_variant_function" % suffix, sep="\t", header=False, index=False)

    LOF = data[data[1].isin(["stopgain", "frameshift deletion", "frameshift insertion", "frameshift substitution"])]
    LOF.to_csv("intermediates/splits/%s.LOF.exonic_variant_function" % suffix, sep="\t", header=False, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an exonic_variant_function from annovar.')
    parser.add_argument('targetfile', metavar='-f', type=str, nargs='+',
                        help='the target file to process')

    args = parser.parse_args()

    filename = args.targetfile[0]
    filename_parts = filename.split("/")[-1].split(".")
    print (filename_parts)
    if filename_parts[-1] != "exonic_variant_function":
        print "Error: must be exonic_variant_function file from annovar"
    else:
        processing_exonic_variant_function(filename, filename_parts[0])
