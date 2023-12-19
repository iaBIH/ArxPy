#  ArxPy: a simple Python interface to Arx anonymization tool

<!-- ![](https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/arx_logo_512.png?raw=true) -->
<img src="https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/arx_logo_512.png?raw=true" alt="Alt text" width="100"/>

This is a simple python interface that uses jython to interact with Arx

Motivation: Arx is difficult to use and lack detailed documentation. Arx based on jave, even thought there are many examples it is 
still difficult to use by data scientists. Providing a python code and a simple way for configuration may benefit wide range of audiences.       

The python script:
   - read JSON configueration files 
     - anonymisation config: algorithm, privacy model, quality model, ..., etc
     - data config: attributes, hierarchies,..., etc  
   - run the Arx anonymization process and produces result files 
   - Notes: 
     - data file must be saved in data folder with the same name e.g.:
       
            ./data/<dataset-name>/<dataset-name>.csv
    
     - config files must be saved in config folder with the same dataset name e.g.:
       
            ./config/<dataset-name>_anonyCfg.json
            ./config/<dataset-name>_dataCfg.json or ./config/<dataset-name>_dataCfg_short.json
     - if _dataCfg_short is provided, the file detailed _dataCfg file is ignored 

     - Sample structure for a dataset input and output:

               ├───<dataset name>: dataset folder
               │   └───<dataset name>.csv: the dataset file 
               │   └───config: datasets configueration files (.json) and hierarchis (.csv) 
               │       ├───<dataset name>_anonyCfg.json: anonymization process configuerations
               │       ├───<dataset name>_dataCfg.json: data configuerations
               │       ├───<dataset name>_hr_<attribute1>.csv: attribute1 hierarchies
               │       ├───<dataset name>_hr_<attribute2>.csv: attribute2 hierarchies
               │       ├─── ...
               │       ├───<dataset name>_hr_<attributeN>.csv: attributeN hierarchies                                              
               │   └───results: results file from diffiernet configuerations
               │       ├───<Data Config Name>_<Anonymization Config Name 1>: results from this configuerations
               │       │   └───charts: all charts of the results of this configuerations  
               │       ├───<Data Config Name>_<Anonymization Config Name 2>: results from this configuerations
               │       │   └───charts: all charts of the results of this configuerations  
               │       ├─── ...
               │       └───<Data Config Name>_<Anonymization Config Name N>: results from this configuerations
               │           └───charts:all charts of the results of this configuerations  

### Requirments:

Python, Jython, Java
Python libs: pip3 install numpy matplotlib pandas plotly seaborn kaleido tensorflow-privacy diffprivlib


Tested on: 

   Linux ubuntu 22.04:

      java       21.0.1 2023-10-17 LTS
      Jython     2.7.2-DEV      
      Python     3.10.12
      matplotlib 3.5.1
      numpy      1.24.2
      pandas     1.5.3
      plotly     5.18.0
      seaborn    0.13.0
      kaleido

   Windows 10:

      java       18.0.2 2022-07-19
      Jython     2.7.3            
      Python     3.6.4
      kaleido    0.1.0.post1
      matplotlib 3.5.2
      numpy      1.23.1
      pandas     1.4.3
      plotly     5.18.0
      seaborn    0.13.0
               
### Compile and Run         
       
        // Windpws
        // for all configs 
        C:\<path-to>\jython2.7.3\bin\jython.exe main.py adults
        // for specific config
        C:\<path-to>\jython2.7.3\bin\jython.exe main.py adults  D1_K5 D1
        //Linux
        jython main.py

### Creating hierarchies:

    - Used Arx GUI, this video is helpful: https://www.youtube.com/watch?v=N8I-sxmMfqQ
    - One also can use chatGPT when possible
    - Another way, is edit csv file directly as text or a table
    - TODO: use hierachy builder in the code. 
    - Hierarchy files must be saved next to the datafile with this format: 

            ./data/<dataset-name>/<dataset-name>_hr_<attributeName>.csv
      if the attributename hasspecial character then only the first two letters is used e.g. for CBC:g/dL
            ./data/<dataset-name>/<dataset-name>_hr_<CB>.csv      


Usage: 
    
    1. Data sampling: get a sample of the data from one or more datasets 
        arguments: s datasetName <0> 
    2. Anonymiation: anonymize a data set using one or more anonymization configurations 
       arguments: a datasetName <anony_config_name> <data_config_name> 
    3. Data sampling and anonymiation: sample from data then anonymize the sampled datase 
          using one or more anonymization configurations 
          arguments: sa datasetName <0> <anony_config_name> <data_config_name> 
    Notes:  
       - Arguments like this <optinal> are optional, if no value is provided, a default value will be used 
       - The dataset must be saved in the data folder with the same name e.g. data/<dataset_name>/<dataset_name>.csv 
          hierarchies must be saved next to the csv dataset file in this format <dataset_name>/<datasetName>_hr_<attributeName>.csv 
          hierarchies should use ; separated data  
       - For each dataset, two configuerations muste be provided, one for the data and one for the anonymization process 
           in JSON format and saved in config folder with the same name e.g. config/<dataset_name>_anonyCfg.json 
           and  config/<dataset_name>_dataCfg.json or  config/<dataset_name>_dataCfg_short.json" )
       - In case multiple datasets are provided e.g. data/<dataset_name>/<dataset_name1>/<dataset_name1>.csv 
                                              data/<dataset_name>/<dataset_name2>/<dataset_name2>.csv 
          for sampling: if mix==0, a new sampled data will be generated for each dataset data/<dataset_name>/<dataset_name1s>/<dataset_name1s>.csv 
                  if mix==1, a mix of all data files will be generated for each dataset data/<dataset_name>/<dataset_name_s>/<dataset_name_s>.csv 

### Data configueration short format: 

   * type_mapping:
      - "id": "IDENTIFYING_ATTRIBUTE",
      - "q": "QUASI_IDENTIFYING_ATTRIBUTE",
      - "s": "SENSITIVE_ATTRIBUTE",
      - "in": "INSENSITIVE_ATTRIBUTE"
   * data_type_mapping:
      - "s": "String",
      - "int": "Integer",
      - "dec": "Decimal",
      - "dt": "Date",
      - "b": "Boolean"
    * data_format_mapping:
      - "d": "Default"
    * transformation_mapping:
      - "g": "Generalization",
      - "m": "Microaggregation",
      - "c": "ClusteringMicroaggregation"
    * transformation_function_mapping:
      - "m": "Mode",
      - "s": "Set"

### Repository structure


TODO: move config to the dataset, so we have everything related to a dataset in one place


               ├───data: datasets and their hierarchies 
               │   ├───adults: dataset folder
               │   │   └───config: datasets configueration files (.json) and hierarchis (.csv) 
               │   │   └───results: results file from diffiernet configuerations
               │   │       ├───D1_Avg9: results from this configuerations
               │   │       │   └───charts: all charts of the results of this configuerations  
               │   │       ├───D1_Identity
               │   │       │   └───charts
               │   │       ├───D1_K3
               │   │       │   └───charts
               │   │       ├───D1_K5
               │   │       │   └───charts
               │   │       ├───D1_PITMAN
               │   │       │   └───charts
               │   │       └───D2_LEOSS
               │   │           └───charts
               ├───lib: required libs e.g. Arx api 
               ├───org: required Arx classes that are not available in arx lib
               ├───resources: figures and resources for github
               └───web: (not completed yet): web UI to generate the configueration files. Based on html and javascript.  

### Sample results 

These are results from adult dataset using LEOSS config

![](https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/MaxRisks.png?raw=true)
![](https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/RiskTable.png?raw=true)
![](https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/distribution_age.png?raw=true)
![](https://github.com/iaBIH/arxPipline/blob/main/iaPipline/resources/contingencyMap_age_education.png?raw=true)


