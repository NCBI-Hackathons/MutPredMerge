import pandas as pd 
import os
        


def processing_exonic_variant_function(path):
    
    data = pd.read_csv(path, delimiter="\t", header=None)
    data = data.applymap(str)
    
    #data.apply(lambda x: triage_variant_types(x), axis=1)
    
    mutations = set(list(data.iloc[:, 1]))
    for i in mutations:
        print (i)

    if os.path.isdir("intermediates/splits/"):
        pass
    else:
        os.makedirs("intermediates/splits/")

    missense = data[data[1] == "nonsynonymous SNV"]
    missense.to_csv("intermediates/splits/missense.exonic_variant_function", sep="\t", header=False, index=False)

    indels = data[data[1].isin(["nonframeshift substitution","nonframeshift deletion","nonframeshift insertion"])]
    indels.to_csv("intermediates/splits/indels.exonic_variant_function", sep="\t", header=False, index=False)

    LOF = data[data[1].isin(["stopgain", "frameshift deletion", "frameshift insertion", "frameshift substitution"])]
    LOF.to_csv("intermediates/splits/LOF.exonic_variant_function", sep="\t", header=False, index=False)


path = "All_DeNovo_Variants.txt.exonic_variant_function"
processing_exonic_variant_function(path)
