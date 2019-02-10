#!/home/ubuntu/anaconda3/bin/python

import pandas as pd 
import os
import argparse
        


def processing_exonic_variant_function(path, output, suffix, threads):

    data = pd.read_csv(path, delimiter="\t", header=None)
    data = data.applymap(str)

    if os.path.isdir(output):
        pass
    else:
        os.makedirs(output)


    missense = data[data[1] == "nonsynonymous SNV"]
    #missense = missense.head(5)
    split_missense = pd.np.array_split(missense, threads)
    for i in range(threads):
        split_missense[i].to_csv(output + "/%s.missense_%s.exonic_variant_function" % (suffix, i), sep="\t", header=False, index=False)


    indels = data[data[1].isin(["nonframeshift substitution","nonframeshift deletion","nonframeshift insertion"])]
    #indels = indels.head(5)
    split_indels = pd.np.array_split(indels, threads)
    for i in range(threads):
        split_indels[i].to_csv(output + "/%s.indels_%s.exonic_variant_function" % (suffix, i), sep="\t", header=False, index=False)


    LOF = data[data[1].isin(["stopgain", "frameshift deletion", "frameshift insertion", "frameshift substitution"])]
    #LOF = LOF.head(5)
    split_LOF = pd.np.array_split(LOF, threads)
    for i in range(threads):
        split_LOF[i].to_csv(output + "/%s.LOF_%s.exonic_variant_function" % (suffix, i), sep="\t", header=False, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an exonic_variant_function from annovar.')
    parser.add_argument('-threads', type=int, nargs="?", default=1,
                        help="The number of threads to be used")
    parser.add_argument('--target', type=str, nargs=1,
                        help='the target file to process')
    parser.add_argument('--output', type=str, nargs=1,
                        help='the output folder to write the splits')

    args = parser.parse_args()

    filename = args.target[0]
    output = args.output[0]
    threads = args.threads
    
    filename_parts = filename.split("/")[-1].split(".")
    
    if filename_parts[-1] != "exonic_variant_function":
        print ("Error: must be exonic_variant_function file from annovar")
    else:
        processing_exonic_variant_function(filename, output, filename_parts[0], threads)
