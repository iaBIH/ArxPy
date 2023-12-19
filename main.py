import os, sys, json, shutil

# add external librraries
sys.path.append("./lib/arx-3.9.1.jar")
sys.path.append("./lib/jfreechart-1.5.4.jar")


from java.io import File
from java.nio.file import Files, Paths
from java.nio.charset import StandardCharsets

from org.deidentifier.arx import ARXAnonymizer
from org.deidentifier.arx.metric import Metric
from org.deidentifier.arx.certificate import ARXCertificate 
from org.deidentifier.arx.io import CSVSyntax

from IAConfigData import IAConfigData   
from IAConfig import IAConfig   
from IAUtils  import IAUtils
from IAConfigRisk import IAConfigRisk

def doAnonymization(anonymizer, config_file_path, config_data_file_path,
                     datasetName, anonyCfgAll, dataCfgAll):               
    """
    Anonymize a dataset using a specific configuration
    Args:
        anonymizer: An instance of ARXAnonymizer.
        config_file_path: The path to the anonymization config file.
        config_data_file_path: The path to the data config file.
        datasetName: The name of the dataset.
        anonyCfgAll: A list of all anonymization configurations.
        dataCfgAll: A list of all data configurations.        
    """
    anony_config_name = anonyCfgAll["config_name"]
    data_config_name  = dataCfgAll["config_name"]

    # define defaults filenames and paths
    resultsFolderPath   = "./data/" + datasetName + "/" + "results/"+anony_config_name
    dataOutputPath      = resultsFolderPath + "/" + datasetName + "_output.csv"
    dataCertificatePath = resultsFolderPath + "/" + datasetName + "_crt.pdf"
    dataReportPath       = resultsFolderPath + "/" + datasetName + "_rpt.txt"
    dataInputStatReportPath  = resultsFolderPath + "/" + datasetName + "_stat_rpt_input.txt"
    dataOutputStatReportPath = resultsFolderPath + "/" + datasetName + "_stat_rpt_output.txt"
    dataInputRiskReportPath  = resultsFolderPath + "/" + datasetName + "_risk_rpt_input.txt"
    dataOutputRiskReportPath = resultsFolderPath + "/" + datasetName + "_risk_rpt_output.txt"

    # create output result folder inside the input folder
    iaUtils      = IAUtils()
    iaDataConfig = IAConfigData()    
    iaConfig     = IAConfig(datasetName)    
    csvSyntaxTmp = CSVSyntax()
    
    if os.path.exists(resultsFolderPath):
       shutil.rmtree(resultsFolderPath)
    os.makedirs(resultsFolderPath)

    print("---------------------------------------------")   
    print("            Read input data and data config")   
    print("---------------------------------------------")   
    data, dataConfig   = iaDataConfig.getData(datasetName, config_data_file_path, data_config_name)

    print("---------------------------------------------")   
    print("            Read Anonymiztion config")   
    print("---------------------------------------------")   
    config, configJsn = iaConfig.getAnonymizationConfig(config_file_path, 
                                                        anony_config_name,data.getDefinition(), iaDataConfig)
    # print("config.getPrivacyModels(): -----------" )
    # print( config.getPrivacyModels())

    # set attribute weights
    config = iaConfig.setAttributeWeights(config, dataConfig)

    print("---------------------------------------------")   
    print("           Start Anonymisation")   
    print("---------------------------------------------")   
    result = anonymizer.anonymize(data, config)

    # saving results
    print(" - saving anonymized data:", dataOutputPath)
    print(dataOutputPath)
    result.getOutput(False).save(dataOutputPath, ';')
    print("Done!")

    print("---------------------------------------------")   
    print("            Printing Result")   
    print("---------------------------------------------")   
    iaUtils.arxPrintResult(result, data, 0, dataReportPath)

    print("---------------------------------------------")   
    print("            Evaluation")   
    print("---------------------------------------------")   
    iaRisk       = IAConfigRisk(configJsn)
    iaRisk.getStatsSummary(data.getHandle(),0,dataInputStatReportPath)    
    iaRisk.getEstimatedRisk(data.getHandle(), 0, dataInputRiskReportPath)

    data.getHandle().release()
    
    iaRisk.getStatsSummary(result.getOutput(),0,dataOutputStatReportPath)
    iaRisk.getEstimatedRisk(result.getOutput(), 0, dataOutputRiskReportPath)

    print("---------------------------------------------")   
    print("            Charting")   
    print("---------------------------------------------")   
    iaUtils.arxCharting(result, data, datasetName, anony_config_name)

    print("---------------------------------------------")   
    print("            Creating Certificate")   
    print("---------------------------------------------")   

    certificate = ARXCertificate.create(data.getHandle(), data.getDefinition(), 
                                        config, result, result.getGlobalOptimum(),
                                        result.getOutput(), csvSyntaxTmp)
    
    certificateResourcesPath = "org/deidentifier/arx/certificate/resources/"
    os.environ["arx.resources.path"] = certificateResourcesPath
    certFile = File(dataCertificatePath) 
    certificate.save(certFile)
    print("Certificate saved in " + certFile.getAbsolutePath())

def process_all_data_configs(anonymizer, config_file_path, config_data_file_path, datasetName,
                        anonyCfgAll, dataCfgAll, anony_config_name, data_config_names):
           """
              Find all data configs for specific anonymization config and process them
                Args:
                    anonymizer: An instance of ARXAnonymizer.
                    config_file_path: The path to the anonymization config file.
                    config_data_file_path: The path to the data config file.
                    datasetName: The name of the dataset.
                    anonyCfgAll: A list of all anonymization configurations.
                    dataCfgAll: A list of all data configurations.
           """
           dataCfgnames = [dCfg for dCfg in data_config_names if anony_config_name.split("_")[0] == dCfg]
           anonyCfg = [cfg for cfg in anonyCfgAll if cfg['config_name'] == anony_config_name][0]
           for data_config_name in dataCfgnames:
               print("anony_config_name  : ",anony_config_name, "   data_config_name  : ",data_config_name)
               dataCfg = [cfg for cfg in dataCfgAll if cfg['config_name'] == data_config_name][0]
               doAnonymization(anonymizer, config_file_path, config_data_file_path, datasetName, anonyCfg, dataCfg)


def main(datasetName,anony_config_name=None,data_config_name=None):
    """
    Main function: Anonymize a dataset using a specific configuration
    If no specific config is provided, all configs in the provided json file will be used
    Args:
        datasetName: The name of the dataset.
        anony_config_name: The name of the anonymization configuration.
        data_config_name: The name of the data configuration.
    """
        # # Create an instance of the Arx anonymizer
    anonymizer = ARXAnonymizer()

    print("=============================================")
    print("    Data Anonymization using Arx " + anonymizer.VERSION)
    print("=============================================")
    print("The script assumes:")
    print("    - the data is placed in ./data/" + datasetName + "/"+datasetName+".csv")
    print("    - the attribute hierarchy is  placed in ./data/" + datasetName + "/config/" + datasetName+"_hr_<attribute_name>.csv")
    print("    - the anonymization config is placed in ./data/" + datasetName + "/config/" + datasetName + "_anonyCfg.csv")
    print("    - the data config is placed in          ./data/" + datasetName + "/config/" + datasetName + "_dataCfg.csv")
    print("    - the result anonymized dataset will be placed in ./data/" + datasetName +"/results/"+datasetName+"_output.csv")
    

    configFolderPath  = "./data/" + datasetName+ "/config/"
    anony_config_path = configFolderPath + datasetName + "_anonyCfg.json"
    data_config_path  = configFolderPath + datasetName + "_dataCfg_short.json"
    # override detailed path if short data config exists
    data_config_path  =  data_config_path if os.path.exists(data_config_path) else configFolderPath + datasetName + "_dataCfg.json"

    #TODO: optimize this and do cleaning 
    anony_config_names      = []
    with open(anony_config_path, 'r') as json_file:
            anonyCfgAll = json.load(json_file)
            anonyCfgAll = anonyCfgAll['configArray']
            for cfg in anonyCfgAll:
                anony_config_names.append(cfg['config_name'])  
    data_config_names = []
    with open(data_config_path, 'r') as json_file:
            dataCfgAll = json.load(json_file)
            dataCfgAll = dataCfgAll['dataConfigArray']
            for cfg in dataCfgAll:
                data_config_names.append(cfg['config_name'])  
    
    #TODO call getAllConfigs: suuport multiple parameters
    # print("anony_config_names    : ",anony_config_names)
    # print("data_config_names     : ",data_config_names)
    # print("user config_name      : ",anony_config_name)
    # print("user data_config_name : ",data_config_name)

    #check if user provides specific config
    if anony_config_name is None:
    #    print("anony_config_names  : ",anony_config_names)
       for anony_config_name in anony_config_names:
           # find all config data for this configuerations   
           process_all_data_configs(anonymizer,anony_config_path, data_config_path, datasetName, 
                                    anonyCfgAll, dataCfgAll, anony_config_name, data_config_names)
    else: 
       # The user provides a anony config name        
       # The user does not provide a data config name
       if data_config_name is None:
           # find all config data for this configuerations             
           process_all_data_configs(anonymizer,anony_config_path, data_config_path, datasetName, 
                                    anonyCfgAll, dataCfgAll, anony_config_name, data_config_names)
       else:  
              # The user provides a data config name
            #   print("config_name  : ",anony_config_name, "   data_config_name  : ",data_config_name)
              anonyCfg = [cfg for cfg in anonyCfgAll if cfg['config_name'] == anony_config_name][0]
              dataCfg = [cfg for cfg in dataCfgAll if cfg['config_name'] == data_config_name][0]
              doAnonymization(anonymizer, anony_config_path, data_config_path, datasetName, anonyCfg, dataCfg)

 

 
if __name__ == "__main__":    
    print("=================================================")
    print("            ArxPy Anonymization ")
    print("=================================================")
    print("Usage: ")
    print("    Anonymiation: anonymize a data set using one or more anonymization configurations")
    print("       arguments: datasetName <anony_config_name> <data_config_name>")
    print("Notes: ")
    print("   - Arguments like this <arg> are optional, if no value is provided, a default value will be used")
    print("   - The dataset must be saved in the data folder with the same name e.g. data/<dataset_name>/<dataset_name>.csv")
    print("      hierarchies must be saved next to the csv dataset file in this format <dataset_name>/<datasetName>_hr_<attributeName>.csv")
    print("      hierarchies should use ; separated data ")
    print("   - For each dataset, two configuerations muste be provided, one for the data and one for the anonymization process")
    print("       in JSON format and saved in config folder with the same name e.g. config/<dataset_name>_anonyCfg.json")
    print("       and  config/<dataset_name>_dataCfg.json or  config/<dataset_name>_dataCfg_short.json" )
    
    #main(datasetName,config_name=None,data_config_name=None)
    if len(sys.argv) < 2:
        print(" No arguments were provided, adults dataset with all configs will be used")
        main("adults")    
        #main("rdDatasets")    
    elif len(sys.argv) < 3:        
        print(" No config is provided ,all configs will be used")
        main(sys.argv[1])
    elif len(sys.argv) < 4:
        print("No data config is provided, all related configs will be used")
        main(sys.argv[1],sys.argv[2])
    elif len(sys.argv) < 5:
        print("Using user arguments: ", sys.argv )
        main(sys.argv[1],sys.argv[2], sys.argv[3])
    else:
        print(sys.argv[1], " dataset will be used!" )
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    
  