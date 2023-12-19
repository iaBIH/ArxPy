import os, sys,  csv, random

def mixDatasets(datasetPaths, outputPath, sampleSize = 200):
    """
    Mix multiple datasets
    Args:
        datasetPaths: A list of paths to the datasets.
        outputPath: The path to the output file.
        sampleSize: The size of the output dataset.        
    """    
    print("mixing datasets")
    #TODO: add implementation


def sampleDataset(datasetPath, outputPath, sampleSize = 200):
    """
    Sample a dataset
    Args:
        datasetPath: The path to the dataset.
        outputPath: The path to the output file.
        sampleSize: The size of the output dataset.        
    """
    inputData   = []
    with open(datasetPath, 'r') as f:
        reader = csv.reader(f)
        inputData = list(reader)

    if (0.0 <= sampleSize) and (sampleSize<= 1.0):
        sampleSize = int(sampleSize * len(inputData))

    print("Sample size ", sampleSize)    

    sampledData = [inputData[0]]
    sampledData.extend(random.sample(inputData, sampleSize))
    
    # write the sample data 
    with open(outputPath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sampledData)   
    print("sampled data is saved at ", outputPath) 
    # copy hierarchy files 
    datasetFolderPath =os.path.dirname(datasetPath)
    datasetName = os.path.basename(datasetFolderPath)
    hierarchyFiles = [os.path.join(datasetFolderPath+"/config",x) for x in os.listdir(datasetFolderPath+"/config") if "_hr_" in x]
    print("datasetFolderPath : ",datasetFolderPath)
    print("hierarchyFiles    : ",hierarchyFiles)
    for hFile in hierarchyFiles:
        newHr = os.path.basename(hFile).replace(datasetName,datasetName+"_"+str(sampleSize))
        newhFilePath = os.path.join(datasetFolderPath+"_"+str(sampleSize)+"/config",newHr )
        print("copying ",hFile,newhFilePath)
        os.system("cp " + hFile +"  " + newhFilePath)

def main(datasetName, sampleSize = 200, isMixd=0):
    """
    Create a small size dataset by sampling randomly from an input dataset
    Args:
        datasetName: The name of the dataset.
        sampleSize: The size of the output dataset.        
        isMixd: A flag indicating whether to mix multiple datasets.
    """
    # TODO error handling e.g.
    #    wrong paths or file formats 
    #    sample size is invalid or larger than the dataset size

    print("---------------------------------------------")   
    print("       Read input datasets ")   
    print("---------------------------------------------")   
    sampleSize = float(sampleSize) if float(sampleSize)<=1 else int(sampleSize)

    # check if multiple datasets are provided
    datasetPaths = os.listdir("./data/" + datasetName + "/")
    datasetPaths = [os.path.join("./data",datasetName,x) for x in datasetPaths if os.path.isdir(os.path.join("./data",datasetName,x)) 
                    and not x=="config" and not x=="results" and not "_"+str(sampleSize) in x[-7:]]
    datasetPaths = [os.path.join("./data",datasetName)] if len(datasetPaths) == 0 else datasetPaths
    print("datasetPaths ",datasetPaths)
    outputSampledPaths = []
    # TODO: make it works for onf folder as well
    for i, dPath in enumerate(datasetPaths):   
        sampleSizeX = sampleSize
        if (not type(sampleSize) == list):
            if isMixd:
               sampleSizeX = int(sampleSize/len(datasetPaths)) if sampleSize > 1.0 else sampleSize/len(datasetPaths)
            else:
               sampleSizeX = sampleSize   
        else:
            sampleSizeX = sampleSize[i]    

        #Get the dataset name
        datasetXName = [x for x in os.listdir(dPath) if (".csv" in x ) and (not "_hr_" in x)][0][:-4]        
        datasetPath  = dPath+ "/"+datasetXName+".csv"
        print("datasetXName : ",datasetXName)
        print("datasetPath  : ",datasetPath)        
        baseFolderPath = os.path.dirname(os.path.dirname(datasetPath))
        outputFolderPath  = baseFolderPath+"/" + datasetXName + "_"+str(sampleSize)
        outputSampledPath = outputFolderPath +"/" +datasetXName+"_"+str(sampleSize)+".csv"
        print("outputFolderPath : ",outputFolderPath)
        print("outputSampledPath: ",outputSampledPath)

        os.mkdir(outputFolderPath) if not os.path.exists(outputFolderPath) else None
        os.mkdir(outputFolderPath+"/config") if not os.path.exists(outputFolderPath+"/config") else None

        sampleDataset(datasetPath, outputSampledPath, sampleSize = sampleSizeX)
        outputSampledPaths.append(outputSampledPath)
    if isMixd:
        print("get sample from each dataset with total size ", sampleSize) 
        #mixDatasets(outputSampledPaths sampleSize = sampleSize)
    else:
        print("get sample from a dataset with size ", sampleSize) 

 
if __name__ == "__main__":    
    print("=============================================")
    print("    Data Sampling Tool")
    print("=============================================")
    datasetName = "adults"
    print(" The script sample a user-defined size (default 20%) from one or more datasets")    
    print(" This is uesful to test the anonymization pipiline on a small dataset or mix of mutiple datasets")        
    print(" If isMix == True: only one dataset with the user-defined size will be produced from all input datasets")    
    print(" Otherwise, multiple datasets will be produced where each has the user defined size")    
    print(" The script assumes:")
    print("    - one datset is placed in ./data/" + datasetName + "/"+datasetName+".csv")
    print("    - multiple datasets e.g.  ./data/" + datasetName + "/datasetName1/datasetName1.csv")
    print("                              ./data/" + datasetName + "/datasetName2/datasetName2.csv")
    print(" a new folder will be created with the sampled datset e.g. ./data/" + datasetName + "_small/"+ datasetName+"_small.csv")
    print("Usage: ")
    print("   arguments: datasetName <sampleSize> <isMix>")
    print("     if 0.0 <= sampleSize <= 1.0, means percentage, otherwise, number of records")
    print("Notes: ")
    print("   - Arguments like this <arg> are optional, if no value is provided, a default value will be used")
    print("   - The dataset must be saved in the data folder with the same name e.g. data/<dataset_name>/<dataset_name>.csv")
    
    #main(datasetName,config_name=None,data_config_name=None)
    if len(sys.argv) < 2:
        print(" No arguments were provided, adults dataset will be used")
        main("adults")    
        #main("rdDatasets")    
    elif len(sys.argv) < 3:        
        print(" No sampleSize is provided 20% will be used!")
        main(sys.argv[1])
    elif len(sys.argv) < 4:
        print("isMix==0 separated datasets will be generated")
        main(sys.argv[1],sys.argv[2])
    else:
        print(sys.argv[1], " dataset will be used!" )
        main(sys.argv[1],sys.argv[2],sys.argv[3]) 