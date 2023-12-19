import json, os 

from java.nio.file import Files, Paths
from java.nio.charset import StandardCharsets

import org.deidentifier.arx as arx
from org.deidentifier.arx import AttributeType, Data, DataType

class IAConfigData:
    """
    This class configures the data based on provided configueration file.
    """

    def getData(self, datasetName, config_file_path, config_name):
        """
        Returns a data instance based on the provided configuration.
        Args:
            datasetName: A string containing the name of the dataset.
            config_file_path: A string containing the path to the configuration file.
            config_name: A string containing the name of the configuration.
        Returns:
            An instance of a data.
            configueration
        """
        #----------------------- Reading the data
        inputFolderPath =  "./data/" + datasetName 
        self.folderPath = Paths.get(inputFolderPath)
        if not Files.exists(self.folderPath) or not Files.isDirectory(self.folderPath):
            print("Invalid folder path provided.")
            return
        else:
            print("Found dataset folder!")

        # print(self.folderPath)

        # List all files in the folder
        files = self.folderPath.toFile().listFiles()

        # Identify data and hierarchies files
        dataFile = None
        print("Available files:")
        for file in files:
            print("   - " +  file.getName() )
            if (file.getName()==datasetName+".csv"):
                dataFile = file
                # print(file)

        if dataFile is None:
            print("Data file not found in the provided folder.")
            return
        data = Data.create(dataFile.getPath(), StandardCharsets.UTF_8, ';')

        handle = data.getHandle()

        #----------------------- Reading the attribute config and hierarchies 
        # Load the JSON configuration file
        config_data = ""
        with open(config_file_path, 'r') as json_file:
            # print("reading data config: ",config_file_path)
            config_data = json.load(json_file)
            #convert to the detailed format if needed
            json_string = json.dumps(config_data)
            if not '"attributes":' in json_string:
               config_data= self.convert_to_detailed_format(config_data)
 
        # Find the configuration with the specified name
        target_config = None
        # print("config_data['dataConfigArray']: ",config_data['dataConfigArray'])

        for dConfig in config_data['dataConfigArray']:
            # print("dConfig['config_name'], ","config_name",  dConfig['config_name'], config_name)
            if dConfig['config_name'] == config_name:
                target_config = dConfig
                break

        self.target_config = target_config
        if target_config is None:
            raise ValueError("Configuration with name is not found in the JSON file: "+ config_name )

        # Get attributes
        print("Attributes in the data file:")
        for i in range(handle.getNumColumns()):
                attribute = target_config['attributes'][i]['name']
                print("attribute : ",attribute)
                #attributeHrFnm = datasetName + "_hr_" + attribute + ".csv"
                attributeType  = self.getAttributeType(i, target_config)
                if  target_config['attributes'][i]['type'] == 'QUASI_IDENTIFYING_ATTRIBUTE':
                   hierarchy = self.getAttributeHierarchy(attribute)
                   data.getDefinition().setAttributeType(attribute, hierarchy)                   
                else:
                   data.getDefinition().setAttributeType(attribute, attributeType)
        
        return data, target_config
    
    # def getAttributeTransformationFunction(self,tFunction):
    #     if tFunction=="Mode":
    #        tFunction  = AttributeType.MicroAggregationFunction.createMode() 
    #     elif tFunction=="Set":
    #        tFunction  = AttributeType.MicroAggregationFunction.createSet()  
    #     else:   
    #        tFunction  = None
    #     return tFunction
    
    def getAttributeHierarchy(self, attribute):
        """
        Returns the hierarchy for the specified attribute.
        Args:
            attribute: A string containing the name of the attribute.
        Returns:
            An instance of a hierarchy.
        """
        folderPath = str(self.folderPath)+"/config"
        files = os.listdir(folderPath)
        #files = self.folderPath.toFile().listFiles()

        attributeInFnm = attribute if (not ":" in attribute)  else attribute[:2]
        attributeHrFnm =  [fnm  for fnm in files  if fnm.endswith("_hr_" + attributeInFnm + ".csv") ][0]
        hierarchy = AttributeType.Hierarchy.create(os.path.join(folderPath, attributeHrFnm), StandardCharsets.UTF_8, ';')
        return hierarchy

    def setAttributeTransformation(self,data, i, target_config, maxLevel):
        """
        Sets the transformation for the specified attribute.
        Args:
            data: An instance of ARXData.
            i: An integer containing the index of the attribute.
            target_config: A dictionary containing the configuration parameters.
            maxLevel: An integer containing the maximum level of generalization.
        Returns:
            An instance of ARXData.
        """    
        attribute = target_config['attributes'][i]['name']
        tTransformation = target_config['attributes'][i]['transformation'] 
        tFunction  = self.getAttributeTransformationFunction(target_config['attributes'][i]['transformationFunction'])
    
        if tTransformation == 'Generalization':
           min,max = target_config['attributes'][i]['transformationMinMax'].split(",")
           min= min.strip()
           max= max.strip()
           min = maxLevel if min == "All" else int(min)
           max = maxLevel if max == "All" else int(max)
           data.getDefinition().setMinimumGeneralization(attribute, min)
           data.getDefinition().setMaximumGeneralization(attribute, max)
        elif tTransformation == 'Microaggregation':            
            data.getDefinition().setMicroAggregationFunction(attribute, tFunction)
            if target_config['attributes'][i]['transformationIgnoreMissingData']=="True":
               data.definition.setMissingDataHandler(attribute, AttributeType.MissingDataHandler.IGNORE)

        elif tTransformation == 'ClusteringMicroaggregation':            
            data.getDefinition().setMicroAggregationFunction(attribute, tFunction, True)
            if target_config['attributes'][i]['transformationIgnoreMissingData']=="True":
               data.definition.setMissingDataHandler(attribute, AttributeType.MissingDataHandler.IGNORE)
        
        return data  

    def getAttributeType(self,i, target_config):
        """
        Returns the type for the specified attribute.
        Args:
            i: An integer containing the index of the attribute.
            target_config: A dictionary containing the configuration parameters.
        Returns:
            An instance of a type.            
        """
        if target_config['attributes'][i]['type'] == 'IDENTIFYING_ATTRIBUTE':
           return AttributeType.IDENTIFYING_ATTRIBUTE 
        elif target_config['attributes'][i]['type'] == 'QUASI_IDENTIFYING_ATTRIBUTE':
            return AttributeType.QUASI_IDENTIFYING_ATTRIBUTE
        elif target_config['attributes'][i]['type'] == 'SENSITIVE_ATTRIBUTE':
            return AttributeType.SENSITIVE_ATTRIBUTE
        elif target_config['attributes'][i]['type'] == 'INSENSITIVE_ATTRIBUTE':
            return AttributeType.INSENSITIVE_ATTRIBUTE        
        else:
            raise ValueError("Attribute type is not supported: " + target_config['attributeList'][i]['type'] )

    def getAttributeDataType(self, i, target_config):
        """
        Returns the data type for the specified attribute.
        Args:
            i: An integer containing the index of the attribute.
            target_config: A dictionary containing the configuration parameters.
        Returns:
            An instance of a data type.
        """
        if target_config['attributes'][i]['dataType'] == 'String':
           #dType = AttributeType.STRING
           dType = DataType.createOrderedString(target_config['attributes'][i]['dataFormat'])
        elif target_config['attributes'][i]['dataType'] == 'Integer':
           #dType = AttributeType.INTEGER
           dType = DataType.createInteger(target_config['attributes'][i]['dataFormat'])
        elif target_config['attributes'][i]['dataType'] == 'Decimal':
           #dType = AttributeType.DECIMAL
           dType = DataType.createDecimal(target_config['attributes'][i]['dataFormat'])
        elif target_config['attributes'][i]['dataType'] == 'Date':
           #dType = AttributeType.DATE
           dType = DataType.createDate(target_config['attributes'][i]['dataFormat'])
        elif target_config['attributes'][i]['dataType'] == 'Boolean':
           #dType = AttributeType.BOOLEAN
           dType = DataType.createBoolean(target_config['attributes'][i]['dataFormat'])
        else:
            dType=None
            raise ValueError("Attribute type is not supported: " + target_config['attributeList'][i]['dataType'] )
 
        return dType 
    
    def convert_to_detailed_format(self,short_json):
        """
        Converts a short JSON configuration to a detailed JSON configuration.
        Args:
            short_json: A dictionary containing the short JSON configuration.
        Returns:
            A dictionary containing the detailed JSON configuration.            
        """
        detailed_json = {"dataConfigArray": []}

        # Mapping for shortcuts
        type_mapping = {
            "id": "IDENTIFYING_ATTRIBUTE",
             "q": "QUASI_IDENTIFYING_ATTRIBUTE",
             "s": "SENSITIVE_ATTRIBUTE",
            "in": "INSENSITIVE_ATTRIBUTE"
        }
        data_type_mapping = {
             "s": "String",
           "int": "Integer",
           "dec": "Decimal",
            "dt": "Date",
             "b": "Boolean"
        }
        data_format_mapping = {
             "d": "Default"
        }
        transformation_mapping = {
            "g": "Generalization",
            "m": "Microaggregation",
            "c": "ClusteringMicroaggregation"
        }
        transformation_function_mapping = {
            "m": "Mode",
            "s": "Set"
        }
        
        # Iterate over the elements in the short format and construct the detailed format
        for j, cfg in enumerate(short_json["dataConfigArray"]):
            #print(j)
            detailed_config = {"config_name": short_json["dataConfigArray"][j]["config_name"], "attributes": []}
            for i in range(len(short_json["dataConfigArray"][j]["ids"])):
                detailed_attribute = {
                    "id": short_json["dataConfigArray"][j]["ids"][i],
                    "name": short_json["dataConfigArray"][j]["names"][i],
                    "type": type_mapping.get(short_json["dataConfigArray"][j]["types"][i], "UNKNOWN"),
                    "transformation": transformation_mapping.get(short_json["dataConfigArray"][j]["transformation"][i], "UNKNOWN"),
                    "transformationFunction": transformation_function_mapping.get(short_json["dataConfigArray"][j]["transformationFunction"][i], "NA"),
                    "transformationIgnoreMissingData": short_json["dataConfigArray"][j]["transformationIgnoreMissingData"][i],
                    "transformationMinMax": "All, All" if short_json["dataConfigArray"][j]["transformationMinMax"][i] == [-1, -1] else str(short_json["dataConfigArray"][j]["transformationMinMax"][i]),
                    "dataType": data_type_mapping.get(short_json["dataConfigArray"][j]["dataTypes"][i], "UNKNOWN"),
                    "dataFormat": data_format_mapping.get(short_json["dataConfigArray"][j]["dataFormats"][i], "UNKNOWN"),
                    "weight": short_json["dataConfigArray"][j]["weights"][i],
                    "targetVariable": bool(short_json["dataConfigArray"][j]["targetVariables"][i])
                }
                detailed_config["attributes"].append(detailed_attribute)

            detailed_json["dataConfigArray"].append(detailed_config)
        return detailed_json

    def __init__(self):
        self.folderPath = ""
        self.target_config = None
  