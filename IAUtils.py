import os, sys, shutil

from java.text import DecimalFormat
from java.util import ArrayList

class IAUtils:
    """
    This class contains some utility methods for the ARX Python API.
    """ 

    @staticmethod
    def arxPrintResult(result, data,showReport=0,outputPath=None):
        """
        Prints the result of the anonymization process.
        Args:
            result: An instance of ARXResult.
            data: An instance of ARXData.
            showReport: A flag indicating whether to show the report.
            outputPath: The path to the output file.            
        """        
        txtData = [] 
        df1 = DecimalFormat("#####0.00")
        sTotal = df1.format(result.getTime() / 1000.0) + "s"
        txtData.append(" - Time needed: " + sTotal + " \n")
        
        optimum = result.getGlobalOptimum()
        qis = ArrayList(data.getDefinition().getQuasiIdentifyingAttributes())

        if not optimum:
            txtLine = " - No solution found! "  + " \n"
            print(txtLine)
            txtData.append(txtLine)
            return

        identifiers = [""] * len(qis)
        generalizations = [""] * len(qis)
        lengthI = 0
        lengthG = 0

        for i in range(len(qis)):
            identifiers[i] = qis.get(i)
            generalizations[i] = str(optimum.getGeneralization(qis.get(i)))
            if data.getDefinition().isHierarchyAvailable(qis.get(i)):
                generalizations[i] += "/" + str(len(data.getDefinition().getHierarchy(qis.get(i))[0]) - 1)
            lengthI = max(lengthI, len(identifiers[i]))
            lengthG = max(lengthG, len(generalizations[i]))

        for i in range(len(qis)):
            while len(identifiers[i]) < lengthI:
                identifiers[i] += " "
            while len(generalizations[i]) < lengthG:
                generalizations[i] = " " + generalizations[i]
        txtData.append(" - Information loss: " + " \n")
        txtData.append(str(result.getGlobalOptimum().getLowestScore()) + " / " + str(result.getGlobalOptimum().getHighestScore())  + " \n")
        txtData.append(" - Optimal generalization" + " \n")        
        for i in range(len(qis)):
            txtData.append("   * " + identifiers[i] + ": " + generalizations[i] + " \n")
        txtData.append(" - Statistics \n")    
        txtData.append(str(result.getOutput(result.getGlobalOptimum(), False).getStatistics().getEquivalenceClassStatistics()))

        if showReport:
            for line in txtData:
                print(line)  

        # save the results to txt a file
        if outputPath:
            with open(outputPath, 'w') as txt_file:
                for line in txtData:
                    txt_file.write(line)

    @staticmethod
    def arxCharting(result, data, datasetName, cfgName):
        """
        Create different charting of the data and the results
        Args:
            result: An instance of ARXResult.
            data: An instance of ARXData.
            outputPath: The path to the output folder.
        """
        # TODO: implement this method
        # TODO: Add more statitics similar to the GUI
        # TODO: Improve the charts look
        # TODO: Test on rare datasets

        print(" - Charting: ")
        print("   - 1. Distribution of each attribute")
        print("   - 2. Contingency map of each attribute")
        print("   - 3. Quality Models")
        print("   - 4. Risk Distribution for each attribute")
        print("   - 5. Risk Quasi-identifiers")        
        print("   - 6. Risk Attacker models for each attribute")
        print("   - 7. RISK HIPAA identifiers")
        print("   - 8. RISK Population uniques")
        print("   - 9. RISK HIPAA identifiers")        
        cmd = "python3 ./doCharting.py " + datasetName +" "+cfgName
        print(cmd)
        os.system(cmd)

