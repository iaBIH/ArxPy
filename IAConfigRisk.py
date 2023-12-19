import org.deidentifier.arx as arx
from org.deidentifier.arx import  ARXPopulationModel
from org.deidentifier.arx.risk import RiskEstimateBuilder
from org.deidentifier.arx.risk import RiskModelAttributes
from org.deidentifier.arx.risk.RiskModelPopulationUniqueness import PopulationUniquenessModel;

class IAConfigRisk:
    """
    This class configures risk models for the ARX data anonymization process.
    """
    
    def getRiskModel(self, config=None):        
        """
        Returns a risk model based on the provided configuration.
        Args:
            config: A dictionary containing the configuration parameters.
        Returns:
            An instance of a risk model.
        """
        try:
            # Example for configuring a specific risk model
            if config['Name']   == "ReidentificationRisk":
                return RiskEstimateBuilder.getSampleBasedReidentificationRisk()
            elif config['Name'] == "PopulationUniqueness":
                return RiskEstimateBuilder.getPopulationBasedUniquenessRisk()
            elif config['Name'] == "QuasiIdentifierRisk":
                return RiskModelAttributes.QuasiIdentifierRisk()
            elif config['Name'] == "SampleUniqueness":
                return RiskEstimateBuilder.getSampleBasedUniquenessRisk()
            else:
                raise ValueError("Unsupported risk model configuration")
        except Exception as e:
            print("An error occurred while creating risk model: ",e)
            return None
        
    def getEstimatedRisk(self, dataHandle, showReport=0, outputPath=None):       
        """
        Prints estimated risk of a data handle
        Args:
            dataHandle: An instance of ARXDataHandle.
            showReport: A flag indicating whether to show the report.
            outputPath: The path to the output file.
        """ 
        txtData=[]
        #TODO: use risk model from the config file
        populationmodel = ARXPopulationModel.create(ARXPopulationModel.Region.USA)
        
        stats = dataHandle.getStatistics()
        
        builder = dataHandle.getRiskEstimator(populationmodel);
        
        #classes = builder.getEquivalenceClassModel();
        sampleReidentifiationRisk = builder.getSampleBasedReidentificationRisk();
        sampleUniqueness = builder.getSampleBasedUniquenessRisk();
        
        populationUniqueness = builder.getPopulationBasedUniquenessRisk();
            
        histogram = builder.getEquivalenceClassModel().getHistogram();
        txtData.append("  Equivalence classes:");
        txtData.append("     - Average size: " + str(builder.getEquivalenceClassModel().getAvgClassSize()));
        txtData.append("     - Num classes : " + str(builder.getEquivalenceClassModel().getNumClasses()));
        txtData.append("     - Histogram   :");
        for i in range(0, len(histogram), 2):
           #print(f"       [Size: {histogram[i]}, count: {histogram[i + 1]}]")
           #print("        [Size: {}, count: {}]".format(histogram[i], histogram[i + 1]))
           txtData.append("        [Size: {}, count: {}]".format(histogram[i], histogram[i + 1]))

        txtData.append(" * Risk estimates:");
        txtData.append("   - Sample-based measures");
        txtData.append("       + Average risk     : " + str(sampleReidentifiationRisk.getAverageRisk()));
        txtData.append("       + Lowest risk      : " + str(sampleReidentifiationRisk.getLowestRisk()));
        txtData.append("       + Tuples affected  : " + str(sampleReidentifiationRisk.getFractionOfRecordsAffectedByLowestRisk()))
        txtData.append("       + Highest risk     : " + str(sampleReidentifiationRisk.getHighestRisk()));
        txtData.append("       + Tuples affected  : " + str(sampleReidentifiationRisk.getFractionOfRecordsAffectedByHighestRisk()))

        txtData.append("     + Max Risk Prosecutor: " + str(sampleReidentifiationRisk.getEstimatedProsecutorRisk()))
        txtData.append("     + Max Risk Journalist: " + str(sampleReidentifiationRisk.getEstimatedJournalistRisk()))
        txtData.append("     + Max Risk Marketer  : " + str(sampleReidentifiationRisk.getEstimatedMarketerRisk()))
 
        txtData.append("       + MaxClassSize     : " + str(stats.getEquivalenceClassStatistics().getMaximalEquivalenceClassSize()))
        txtData.append("       + AverageClassSize : " + str(stats.getEquivalenceClassStatistics().getAverageEquivalenceClassSize()))
        txtData.append("       + MinClassSize     : " + str(stats.getEquivalenceClassStatistics().getMinimalEquivalenceClassSize()))
        txtData.append("       + SuppressedRecords: " + str(stats.getEquivalenceClassStatistics().getNumberOfSuppressedRecords()))

        txtData.append("       + Ambiguity          : " + str(stats.getQualityStatistics().getAmbiguity().getValue()))
        txtData.append("       + AECS               : " + str(stats.getQualityStatistics().getAverageClassSize().getValue()))
        txtData.append("       + Discernibility     : " + str(stats.getQualityStatistics().getDiscernibility().getValue()))
        txtData.append("       + Granularity        : " + str(stats.getQualityStatistics().getGranularity().getArithmeticMean(False)))
        txtData.append("       + MSE                : " + str(stats.getQualityStatistics().getRecordLevelSquaredError().getValue()))       
        txtData.append("       + Attribute-level SE : " + str(stats.getQualityStatistics().getAttributeLevelSquaredError().getArithmeticMean(False)))
        txtData.append("       + Non-Uniform Entropy: " + str(stats.getQualityStatistics().getNonUniformEntropy().getArithmeticMean(False) ))
        txtData.append("       + Precision          : " + str(stats.getQualityStatistics().getGeneralizationIntensity().getArithmeticMean(False) ))
        txtData.append("       + Record-level SE    : " + str(stats.getQualityStatistics().getRecordLevelSquaredError().getValue() ))


        txtData.append("       + Sample uniqueness: " + str(sampleUniqueness.getFractionOfUniqueRecords()));
        txtData.append("     - Population-based measures");
        txtData.append("       + Population unqiueness (Zayatz): " + str(populationUniqueness.getFractionOfUniqueTuples(PopulationUniquenessModel.ZAYATZ)))

        if showReport:
            for line in txtData:
                print(line)  

        # save the results to txt a file
        if outputPath:
            with open(outputPath, 'w') as txt_file:
                for line in txtData:
                    txt_file.write(line + "\n")

    def getStatsSummary(self, dataHandle, showReport=0, outputPath=None):        
        """
        Prints statitics of a data handle 
        Args:
            dataHandle: An instance of ARXDataHandle.
            showReport: A flag indicating whether to show the report.
            outputPath: The path to the output file.
        """
        txtData=[]

        stats = dataHandle.getStatistics().getSummaryStatistics(False);
        txtData.append("  Statistics :");
        txtData.append("       Summary: " + str(stats));    

        if showReport:
            for line in txtData:
                print(line)  

        # save the results to txt a file
        if outputPath:
            with open(outputPath, 'w') as txt_file:
                for line in txtData:
                    txt_file.write(line + "\n")
                    
    def __init__(self, anonyConfig=None):
        self.riskConfig= anonyConfig["riskMetric"]
