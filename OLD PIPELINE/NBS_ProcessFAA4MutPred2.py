'''
Created on Oct 22, 2015

@author: B. Cai

Process output FASTA protein sequence file of ANNOVAR to the format that required by the MutPred2

'''
import sys
import csv
posDict={}# dictionary of variant position of each line

seqDict={} # sequence dictionary, key title with mutations
mutationList=[] # list of mutations, title rows of the output fasta file, keys of the sequence dictionary
curSeq=''
curMutSeq=''
saveSeq=False
saveMutSeq=False
curKey=''
base = "/data/users/trberg/staging/MutPred2_processing/"
wp=base + 'MutPred2_faa_files/'
wp2 = base + 'MutPred2_annovar_ready/'
wp3 = base + "MutPred2_ready/"
filename=sys.argv[1]

# get chromesome position information
with open(wp2+filename+'.txt', 'rU') as csvfile:
    lineReader = csv.reader(csvfile,delimiter='\t')
    linenum=0
    #annoVarTitle=next(lineReader)
    #otherInfoInd=annoVarTitle.index('Otherinfo')
    for row in lineReader:
        linenum=linenum+1
        #posDict['line'+str(linenum)]=str(row[otherInfoInd+3]+'_'+row[otherInfoInd+4]+'_'+row[otherInfoInd+6]+'_['+row[otherInfoInd+7]+']')
        posDict['line'+str(linenum)]=str(row[0]+'_'+row[1]+'_'+row[3]+'_'+row[4])

        #print 'line'+str(linenum)
        #print posDict['line'+str(linenum)]
# process the fasta file
with open(wp+filename+'.faa', 'rU') as csvfile:
    codeReader = csv.reader(csvfile)
    for row in codeReader:
        if not row: continue
        #print row
        curRow=row[0]
        if curRow.startswith('>'):
            # process title row
            titleElements=curRow.split(' ')
            if titleElements[2]=='WILDTYPE':                                
                
                if saveMutSeq:
                    if len(curSeq)==len(curMutSeq):
                        if curKey.find('*')==-1: 
                            mutationList.append(curKey)                   
                            seqDict[curKey]=curSeq[:-1]
                            #print curKey
                        
                    
                    curSeq=''
                    saveSeq=False
                    curMutSeq=''
                    saveMutSeq=False    
                saveSeq=True    
            else:
                
                #print titleElements
                if titleElements[3]!='synonymous' and titleElements[3]!='immediate-stopgain':
                    curKey=titleElements[0]+'_'+posDict[titleElements[0][1:]]+'_'+titleElements[1]+'_'+titleElements[2]+' '+titleElements[9]+titleElements[6]+titleElements[11][:-1]                    
                    saveMutSeq=True
                    saveSeq=False
                    #seqDict[curKey]=curSeq[:-1]
                    #print titleElements[9]+titleElements[6]+titleElements[11][:-1]
                else:
                    curSeq=''
                    saveSeq=False
                    curMutSeq=''
                    saveMutSeq=False
                                   
        elif saveSeq:
            # process wild-type sequence row
            if curSeq=='':
                curSeq=curSeq+curRow
            else:
                curSeq=curSeq+'\n'+curRow
            #print curSeq
        elif saveMutSeq:
            # process mutated sequence row
            if curMutSeq=='':
                curMutSeq=curMutSeq+curRow
            else:
                curMutSeq=curMutSeq+'\n'+curRow    
            
#print seqDict
#print seqDict['>line6_NM_001010881_c.G3572A R1191H']
#print seqDict['>line3712_NM_000531_c.G639A M213I']

with open(wp3+filename+'_MutPred2.faa', 'wb') as faafile:
    #pdWriter = csv.writer(csvfile, delimiter=',')
    #pdWriter.writerow(['Patient']+['Category']+['Type']+diseaseNameList)    
    #pdWriter.writerow(['MedGen ID']+codeIDList)
    for mutationTitle in mutationList:
        faafile.write(mutationTitle+'\n')
        faafile.write(seqDict[mutationTitle])
        if seqDict[mutationTitle][-1:]!='\n':
            faafile.write('\n')
