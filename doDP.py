import os, sys,  csv, random, re
import numpy as np
#import tensorflow as tf
#from tensorflow_privacy.privacy.optimizers.dp_optimizer import DPGradientDescentGaussianOptimizer
import pandas as pd
from diffprivlib.mechanisms import Laplace, Gaussian

# Differential Privacy: a framework for measuring the privacy guarantees provided by an algorithm. 
# In the context of data analysis, it ensures that the output of the analysis doesn't reveal much about any individual data point.
#     Epsilon (ε): A smaller epsilon means stronger privacy.
#          It measures the maximum amount the presence or absence of a single
#                 individual can change the probability of a particular output.
#     Delta (δ): This is a small probability, typically close to the reciprocal of the dataset size.
#                  It measures the probability that the privacy guarantee might not hold.
# Differential privacy is achieved by adding noise to the data in such a way that the overall
#  results are not affected by the presence or absence of a single individual.
# 
# Usage example: 
#
# python3 doDP.py ./data/cf32093_200/cf32093_200.csv ./data/cf32093_200/results/DP/cf32093_200_output_dp.csv 1.0 0.01 1.0
 
def anonymize_numeric_column(column, epsilon, delta=0.0, sensitivity=1.0):
    # Choose the mechanism based on delta
    if delta == 0:
        print("Laplace ...")
        mech = Laplace(epsilon=epsilon, sensitivity=sensitivity)
    else:
        print("Gaussian ...")
        mech = Gaussian(epsilon=epsilon, delta=delta, sensitivity=sensitivity)

    # Anonymize and round each value in the column
    anonymized_column = column.apply(lambda x: round(mech.randomise(x), 0) if isinstance(x, int) else round(mech.randomise(x), 3))

    return anonymized_column


def anonymize_dataset(df, epsilon=1.0, delta=0.0, sensitivity=1.0):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = anonymize_numeric_column(df[col], epsilon, delta, sensitivity)
    return df


def main(datasetInPath,datasetOutPath, epsilon=1.0, delta=0.0, sensitivity=1.0):
    print("datasetInPath : ",datasetInPath) 
    print("datasetOutPath: ",datasetOutPath)
    print("epsilon       : ",epsilon)
    print("delta         : ",delta)

    epsilon = float(epsilon)
    delta = float(delta)

    db = pd.read_csv(datasetInPath, delimiter=';') 
    anonymized_db = anonymize_dataset(db, epsilon, delta, sensitivity)
    anonymized_db.to_csv(datasetOutPath, index=False, sep=';')

if __name__ == "__main__":    
    print("============================================================")
    print(" Anonymizing the data using differential privacy algorithm")
    print("============================================================")
   
    #main(datasetName,config_name=None,data_config_name=None)
    if len(sys.argv) < 5:        
        print(" Please provide input dataset path, output dataset path, epsilon and delta for e-d DP")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4]) 
