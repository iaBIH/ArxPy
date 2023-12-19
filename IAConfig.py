import json

# required arx classes 
from org.deidentifier.arx import  AttributeType, ARXConfiguration, ARXPopulationModel

# criteria classes
from org.deidentifier.arx.criteria import KAnonymity, LDiversity,RecursiveCLDiversity,BasicBLikeness, TCloseness, AverageReidentificationRisk, PopulationUniqueness , HierarchicalDistanceTCloseness  
from org.deidentifier.arx.risk.RiskModelPopulationUniqueness import PopulationUniquenessModel

# metrics classes
from org.deidentifier.arx.metric import Metric


class IAConfig:
    """
    This class configures the anonymization process based on provided configueration file.
    """

    def getQualityModel(self, config):
        """
        Returns a quality model based on the provided configuration.
        Args:
            config: A dictionary containing the configuration parameters.
        Returns:
            An instance of a quality model.
        """        
        #TODO add more metrics, do more testing
        try:
            if config['Name']=="LossMetric Metric.AggregateFunction.GEOMETRIC_MEAN":   
               return Metric.createLossMetric(config['parameter'], Metric.AggregateFunction.GEOMETRIC_MEAN)
            elif config['Name']=="LossMetric Metric.AggregateFunction.ARITHMETIC_MEAN":
                return Metric.createLossMetric(config['parameter'], Metric.AggregateFunction.ARITHMETIC_MEAN)
            elif config['Name']=="LossMetric Metric.AggregateFunction.MAX":
                return Metric.createLossMetric(config['parameter'], Metric.AggregateFunction.MAXIMUM)
            elif config['Name']=="LossMetric Metric.AggregateFunction.MIN":
                return Metric.createLossMetric(config['parameter'], Metric.AggregateFunction.RANK)
            elif config['Name']=="LossMetric Metric.AggregateFunction.SUM":
                return Metric.createLossMetric(config['parameter'], Metric.AggregateFunction.SUM)         
            elif config['Name'] == "Entropy":
               return Metric.createEntropyMetric(config['parameter'])
            elif config['Name'] == "NonUniformEntropy":
               return Metric.createNonUniformEntropyMetric()
            elif config['Name'] == "Discernibility":
                return Metric.createDiscernabilityMetric()
            elif config['Name'] == "Precedence":
                return Metric.createPrecedenceMetric()            
            else:
                raise ValueError("Unsupported quality model configuration")
        except Exception as e:
            print("An error occurred while creating quality model:", e)
            return None

    def getPrivacyModel(self, p, dataDef=None, dataCfg=None):
        """
        Returns a privacy model based on the provided configuration.
        Args:
            p: A dictionary containing the configuration parameters.
            dataDef: An instance of DataDefinition.
            dataCfg: An instance of DataConfig.            
        Returns:
            An instance of a privacy model.
        """
        privacyModel = None
        if p['modelName'] == 'KAnonymity':
            privacyModel = KAnonymity(p['k'])
        elif p['modelName'] == 'LDiversity':
            privacyModel = LDiversity(p['l'])
        elif p['modelName'] == 'RecursiveCLDiversity':
            privacyModel = RecursiveCLDiversity(p['attribute'], p['c'],p['l'])
        elif p['modelName'] == 'BasicBLikeness':
            privacyModel = BasicBLikeness(p['attribute'],p['beta'])
        elif p['modelName'] == 'TCloseness':
            privacyModel = TCloseness(p['t'])
        elif p['modelName'] == 'HierarchicalDistanceTCloseness':                 
            t = p['t']
            attribute = p['attribute'] 
            hierarchy = dataCfg.getAttributeHierarchy(attribute)
            dataDef.setAttributeType(attribute, AttributeType.SENSITIVE_ATTRIBUTE)
            privacyModel = HierarchicalDistanceTCloseness(attribute, t, hierarchy)                                                       
        elif p['modelName'] == 'PopulationUniqueness':                 
            populationUniquenessModel =  PopulationUniquenessModel.valueOf(p['populationUniquenessModel'])   
            region = ARXPopulationModel.create(ARXPopulationModel.Region.valueOf(p['region']))     
            privacyModel = PopulationUniqueness(p['riskThreshold'], 
                                                populationUniquenessModel, 
                                                region)     
        elif p['modelName'] == 'AverageReidentificationRisk': 
            privacyModel = AverageReidentificationRisk(p['averageRisk'])                
        else:
            raise ValueError("Privacy model type is not supported: " + p['modelName'] )
        return privacyModel


    def getAnonymizationConfig(self, config_file_path, config_name, dataDef=None, myDataConfig=None):
        """
        Returns an ARXConfiguration object based on the provided configuration.
        Args:
            config_file_path: The path to the JSON configuration file.
            config_name: The name of the configuration to load.
            dataDef: An instance of DataDefinition.
            dataCfg: An instance of DataConfig.
        Returns:
            An instance of ARXConfiguration.            
        """
        # Load the JSON configuration file
        with open(config_file_path, 'r') as json_file:
            config_data = json.load(json_file)

        # Find the configuration with the specified name
        target_config = None
        for config in config_data['configArray']:
            if config['config_name'] == config_name:
                target_config = config
                break

        if target_config is None:
            raise ValueError("Configuration with name is not found in the JSON file: "+ config_name )

        # Create an ARXConfiguration object and set its properties based on the JSON data
        self.anonyConfig = ARXConfiguration.create()        
        self.anonyConfig.setAlgorithm(ARXConfiguration.AnonymizationAlgorithm.valueOf(target_config['Algorithm']))
        self.anonyConfig.setSuppressionLimit(target_config['SuppressionLimit'])

        # add all privacy models in the array
        privacyModelLst = target_config['privacyModelList']
        for p in privacyModelLst:
            # Add the privacy model(s)
            #print("Adding privacy model : " + str(p))
            privacyModel = self.getPrivacyModel(p, dataDef, myDataConfig)
            self.anonyConfig.addPrivacyModel(privacyModel)
        # print(self.anonyConfig.getPrivacyModels())
        self.anonyConfig.setQualityModel(self.getQualityModel(target_config["qualityModel"]))

        return self.anonyConfig, target_config

    def setAttributeWeights(self, config, dataConfig):
        """
        Sets the attribute weights in the ARXConfiguration object.
        Args:
            config: An instance of ARXConfiguration.
            dataConfig: An instance of DataConfig.
        Returns:
            An instance of ARXConfiguration with updated attribute weights.             
        """    
        # Note: it would be nice if Arx use the data definition to set the weights
        for i,attData in enumerate(dataConfig['attributes']):
            attName  = attData['name']
            weight   = attData['weight'] 
            config.setAttributeWeight(attName, weight)
        return config

    def __init__(self, datasetName):

        self.datasetName = datasetName
 