#!/bin/sh
# script for execution of deployed applications
#
#Installs the needed packages and programs for MutPredMerge

while true; do
    read -p "The installation of the MutPred Suite takes 90 Gb? Do you wish to continue? " yn
    case $yn in
        [Yy]* ) 
            # download and unzip mutpred2
            wget --directory-prefix=tools/ http://mutpred.mutdb.org/mutpred2.0_linux_x86_64.tar.gz;
            tar -xvzf tools/mutpred2.0_linux_x86_64.tar.gz;
            rm tools/mutpred2.0_linux_x86_64.tar.gz;
            printf "[NCBI]\nDATA=$(pwd)/tools/mutpred2.0/blast-2.2.18/data/" > tools/mutpred2.0/.ncbirc;
            source tools/mutpred2.0/.ncbirc;
            echo "ignore this error, all is fine";

            #download and unzip mutpred LOF
            wget --directory-prefix=tools/ http://mutpredlof.cs.indiana.edu/MutPredLOF_compiled.tar.gz;
            tar -xvzf tools/MutPredLOF_compiled.tar.gz;
            rm tools/MutPredLOF_compiled.tar.gz;
            cp -r tools/mutpred2.0/v91/ tools/MutPredLOF/;

            #download and unzip mutpred indels
            wget --directory-prefix=tools/ http://mutpredindel.cs.indiana.edu/MutPredIndel_compiled.tar.gz;
            tar -xvzf tools/MutPredIndel_compiled.tar.gz;
            rm tools/MutPredIndel_compiled.tar.gz;
            cp -r tools/mutpred2.0/v91/ tools/MutPredIndel_compiled/;
            break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
