import os, sys,  csv, random, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

#pio.renderers.default = 'plotly_mimetype'  # or 'plotly_html'
# pio.renderers.default = 'browser'  # or 'notebook', 'svg', etc.

# color for spedo meter and bars
colorRanges = [
                    {'range': [0, 20], 'color': 'green'},
                    {'range': [21, 35], 'color': 'lightgreen'},
                    {'range': [36, 45], 'color': 'yellowgreen'},
                    {'range': [46, 55], 'color': 'yellow'},
                    {'range': [56, 66], 'color': 'orange'},
                    {'range': [67, 80], 'color': 'orangered'},
                    {'range': [81, 100], 'color': 'red'}
                ]
colorRangesRev = [
                    {'range': [0, 20], 'color': 'red'},
                    {'range': [21, 35], 'color': 'orangered'},
                    {'range': [36, 45], 'color': 'orange'},
                    {'range': [46, 55], 'color': 'yellow'},
                    {'range': [56, 66], 'color': 'yellowgreen'},
                    {'range': [67, 80], 'color': 'lightgreen'},
                    {'range': [81, 100], 'color': 'green'}
                ]
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

def createSideBySideFrequencyChart(Din,Dout,title,resultPath):
    print("createSideBySideFrequencyChart")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10)) # 20 to have enough space for both

    # Plotting the first chart
    ax1.bar(Din[0], Din[1], color='black')
    ax1.set_xlabel('Items')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of Items for Input Data: '+ title)
    ax1.legend(['Frequency'])
    ax1.tick_params(axis='x', labelsize=6)  # Adjust font size as needed
    ax1.set_xticklabels(Din[0], rotation=90)  

    # Plotting the second chart
    ax2.bar(Dout[0], Dout[1], color='black')
    ax2.set_xlabel('Items')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Items for Output Data: '+ title)
    ax2.legend(['Frequency'])
    ax2.tick_params(axis='x', labelsize=6)  # Adjust font size as needed
    ax2.set_xticklabels(Dout[0], rotation=90)  

    plt.tight_layout()

    # Save the figures to a file
    outputFilePath = resultPath+"/distribution_"+ title+".png"
    plt.savefig(outputFilePath)
    plt.close()

def createFrequencyCharts(data, resultPath):

    print("createFrequencyCharts")
    # loop through attributes and create a chart for each one
    dataIn, dataOut = data
    dataInLbl = dataIn[0];  dataIn  = dataIn[1:]
    dataOutLbl= dataOut[0]; dataOut = dataOut[1:];   
    dataLbl = []
    if len(dataInLbl) != len(dataOutLbl):
        # find similar attributes
        dataLbl = [attrib for attrib in dataInLbl if attrib in dataOutLbl]
    else:
        dataLbl = dataInLbl    
    
    # print("dataInLbl : ",dataInLbl)
    # print("dataLbl   : ",dataLbl)
    for attrib in dataLbl:
        # create a frequency chart
        print("attrib: ",attrib)
        # find unique values of this column
        attribInValues  = [x[dataInLbl.index(attrib)]  for x in dataIn]
        attribOutValues = [x[dataOutLbl.index(attrib)] for x in dataOut]
        # compute frequencies
        frequencyIn  = {item: attribInValues.count(item)  for item in set(attribInValues)}
        frequencyOut = {item: attribOutValues.count(item) for item in set(attribOutValues)}

        # Sorting the dictionaries by their keys
        frequencyIn  = {k: frequencyIn[k]  for k in sorted(frequencyIn)}
        frequencyOut = {k: frequencyOut[k] for k in sorted(frequencyOut)}

        #Creating lists for the plot
        X1 = list(frequencyIn.keys())
        Y1 = list(frequencyIn.values())
        X2 = list(frequencyOut.keys())
        Y2 = list(frequencyOut.values())
        # createFrequencyChart(X1,Y1,attrib+"_In" ,resultPath)
        # createFrequencyChart(X2,Y2,attrib+"_Out",resultPath)
        createSideBySideFrequencyChart([X1,Y1],[X2,Y2],attrib,resultPath)

 
def createSideBySideContingencyMap(contingency_table_in, contingency_table_out, title, resultPath):
    
    attrib1 = title.split("_")[0]  
    attrib2 = title.split("_")[1]  
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Create the heatmap for the first dataset (Input Data)
    sns.heatmap(contingency_table_in, ax=ax1, annot=False, 
                cmap='viridis', square=True, cbar_kws={'label': 'Values'})

    ax1.set_title("Contingency Map Input Data " + title)
    ax1.invert_yaxis()  # Invert the y-axis to start from the bottom left
    ax1.set_aspect('auto')
    ax1.set_xlabel(attrib2)  
    ax1.set_ylabel(attrib1)  
    # Create the heatmap for the second dataset (Output Data)
    sns.heatmap(contingency_table_out, ax=ax2, annot=False, 
                cmap='viridis', square=True, cbar_kws={'label': 'Values'})

    ax2.set_title("Contingency Map Output Data " + title)
    ax2.invert_yaxis()  # Invert the y-axis to start from the bottom left
    ax2.set_aspect('auto')
    ax2.set_xlabel(attrib2)  
    ax2.set_ylabel(attrib1)  

    plt.tight_layout()

    # Save the figures to a file
    outputFilePath = f"{resultPath}/contingencyMap_{title}.png"
    plt.savefig(outputFilePath)
    plt.close()  # Close the figure 

def createContengencyMapCharts(data, resultPath):
    print("createContengencyMapCharts")
    # loop through attributes and create a chart for each pair
    dataIn, dataOut = data
    dataInLbl  = dataIn[0]
    dataOutLbl = dataOut[0]
    dataLbl = list(set(dataInLbl) & set(dataOutLbl))  # find common attributes

    for attribX in dataLbl:
        for attribY in dataLbl:
            print("Attributes: ", attribX, attribY)
            # Get the column data for each attribute
            attribXInValues  = [x[dataInLbl.index(attribX)] for x in dataIn[1:]]
            attribYInValues  = [x[dataInLbl.index(attribY)] for x in dataIn[1:]]
            attribXOutValues  = [x[dataOutLbl.index(attribX)] for x in dataOut[1:]]
            attribYOutValues  = [x[dataOutLbl.index(attribY)] for x in dataOut[1:]]

            # Create a contingency table
            contingency_table_in  = pd.crosstab(index=attribXInValues,  columns=attribYInValues)
            contingency_table_out = pd.crosstab(index=attribXOutValues, columns=attribYOutValues)
            createSideBySideContingencyMap(contingency_table_in,contingency_table_out, attribX+"_"+attribY, resultPath)


def getGgauge(fig, percentages,titles,rows,cols, startPos =3):
    print("getGgauge ...")
    for i, (percentage, title) in enumerate(zip(percentages, titles), start=startPos):
        nRows= (i-1)//cols + 1 if startPos==1 else (i)//cols + 1
        nCols= (i-1)%cols  + 1 if startPos==1 else i-2
        fig.add_trace(
            go.Indicator(
            mode="gauge+number",
            value=percentage,
            domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]},
            title={'text': title},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': "darkblue"},
                'bar': {'color': "black"},
                'steps': colorRanges,
            },
            number={'suffix': "%"}
        ), row=nRows, col=nCols)


def createSpeedoMeterCharts(percentagesIn, titlesIn, percentagesOut, titlesOut, resultPath, cols=1):
    rows = 2
    cols = 3
    specs = [ [{'type': 'indicator'}]*cols] *rows
    fig = make_subplots(rows=rows,
                        cols=cols,
                        specs=specs)
    getGgauge(fig, percentagesIn,  titlesIn, rows, cols, startPos =1)
    getGgauge(fig, percentagesOut, titlesOut,rows, cols, startPos =3)
    fig.update_layout(
        title_text="<b>InputDataSet: Max Risk</b>",
        title_x=0.5,
        title_font_size=20,
        annotations=[
            dict(
                text="<b>OutputDataSet: Max Risk</b>",  # Title for the second row
                x=0.5,  # x position (0.5 for center)
                y=0.55,  # y position (adjust this value as needed)
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=20)  # Font size of the title (adjust as needed)
            )
        ]
    )
    fig.update_layout(height=300*rows, width=300*cols)
    outputFilePath = resultPath+"/MaxRisks.png"    
    fig.write_image(outputFilePath)    

def create_color_segments(bar_width, ranges):
    # This function calculates the width and start position of each color segment within a bar
    segments = []
    start = 0
    for range_def in ranges:
        lower, upper = range_def['range']
        if lower >= bar_width:
            break
        upper = min(upper, bar_width)
        segment_width = upper - max(lower, start)
        if segment_width > 0:
            segments.append((start, segment_width, range_def['color']))
            start += segment_width
    return segments

def createTableChart(ax, df, title):
    ax.set_title(title)
    ax.set_xlabel('Percentage')
    ax.set_xlim(0, 100)
    
    for index, row in df.iterrows():
        color_ranges = colorRangesRev if index>2 else colorRanges
        measure = row['Measure']
        percentage = row['Percentage']
        bar_segments = create_color_segments(percentage, color_ranges)
        for start, width, color in bar_segments:
            ax.barh(measure, width, left=start, color=color)
        text_x_pos = percentage / 2
        text_color = 'black' #'white' if percentage >= 20 else 'black'
        ha = 'center' if percentage >= 20 else 'left'
        ax.text(text_x_pos, measure, f'{percentage}%', ha=ha, va='center', color=text_color, weight='bold')

def createTableCharts(dataIn, dataOut, title="test risk", resultPath=""):
    measuresIn, valuesIn = dataIn
    pdIn = pd.DataFrame({'Measure': measuresIn, 'Percentage': valuesIn})

    measuresOut, valuesOut = dataOut
    pdOut = pd.DataFrame({'Measure': measuresOut, 'Percentage': valuesOut})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    createTableChart(ax1, pdIn, "InputData")
    createTableChart(ax2, pdOut, "OutputData")

    fig.tight_layout()
    outputFilePath = resultPath + "/RiskTable.png"
    plt.savefig(outputFilePath)
    plt.close()


def extract_risk_values(file_path):
    risk_values = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Regular expression to match risk values
            match = re.search(r'\+\s(.*):\s([0-9.]+)', line)
            if match:
                key = match.group(1).strip()
                value = float(match.group(2).strip())
                risk_values[key] = value
    return risk_values

def getStats(df):
    # Initialize all stats lists as empty
    statsLst = {
        "age_stats_gender": [],
        "age_stats_overall": [],
        "age_stats_race": [],
        "sex_percentage": [],
        "race_percentage": [],
        "clinical_stats": [],
        "alive_dead_percentage": [],
        "lowest_highest_diag": [],
        "lowest_highest_death": [],
        "min_max_state": [],
        "min_max_zipcode": []
    }

    # Convert 'age' to numeric, ignoring non-numeric values
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    # Age and gender statistics
    if 'age' in df and 'sex' in df and not df['age'].eq('*').all() and not df['sex'].eq('*').all():
        statsLst['age_stats_gender'] = df.groupby('sex')['age'].agg(['min', 'max', 'median', 'mean'])
        statsLst['age_stats_overall'] = df['age'].agg(['min', 'max', 'median', 'mean'])

    # Race statistics
    if 'race' in df and not df['race'].eq('*').all():
        statsLst['age_stats_race'] = df.groupby('race')['age'].agg(['min', 'max', 'median', 'mean'])
        statsLst['race_percentage'] = df['race'].value_counts(normalize=True) * 100

    # Sex percentage
    if 'sex' in df and not df['sex'].eq('*').all():
        statsLst['sex_percentage'] = df['sex'].value_counts(normalize=True) * 100

    # Clinical parameters statistics
    clinical_params = df.select_dtypes(include=[np.number]).iloc[:, -2:]  # Adjust based on your dataset
    if not clinical_params.empty:
        try:
            statsLst['clinical_stats'] = clinical_params.agg(['min', 'max', 'median', 'mean'])
        except Exception as e:
            # print(e)
            statsLst['clinical_stats'] = []

    # Alive/dead percentage
    if 'deathDate' in df:
        df['deathDate'] = pd.to_datetime(df['deathDate'], errors='coerce')
        statsLst['alive_dead_percentage'] = df['deathDate'].notna().value_counts(normalize=True) * 100

        # Lowest/Highest Death Year
        df['deathYear'] = df['deathDate'].dt.year
        if not df['deathYear'].isna().all():
            death_counts = df['deathYear'].value_counts(dropna=True)
            statsLst['lowest_highest_death'] = [(death_counts.idxmin(), death_counts.min()), (death_counts.idxmax(), death_counts.max())]

    # Diagnosis year statistics
    if 'diagDate' in df:
        df['diagYear'] = pd.to_datetime(df['diagDate'], errors='coerce').dt.year
        if not df['diagYear'].isna().all():
            diag_counts = df['diagYear'].value_counts(dropna=True)
            statsLst['lowest_highest_diag'] = [(diag_counts.idxmin(), diag_counts.min()), (diag_counts.idxmax(), diag_counts.max())]

    # State statistics
    if 'state' in df and not df['state'].eq('*').all():
        state_counts = df['state'].value_counts()
        statsLst['min_max_state'] = [(state_counts.idxmin(), state_counts.min()), (state_counts.idxmax(), state_counts.max())]

    # Zipcode statistics
    if 'zipCode' in df and not df['zipCode'].eq('*').all():
        zipcode_counts = df['zipCode'].value_counts()
        statsLst['min_max_zipcode'] = [(zipcode_counts.idxmin(), zipcode_counts.min()), (zipcode_counts.idxmax(), zipcode_counts.max())]

    return statsLst



def getStatsAll(datasetName, cfgName):
    print("Charting data for ",datasetName, cfgName)
    inputDataPath  = os.path.join("./data",datasetName,datasetName+".csv")
    outputDataPath = os.path.join("./data",datasetName,"results",cfgName,datasetName+"_output.csv")    
    resultPath     = os.path.join("./data",datasetName,"results",cfgName)
    # read input and output csv data fiels 
    dataIn = pd.read_csv(inputDataPath, delimiter=';')
    dataOut = pd.read_csv(outputDataPath, delimiter=';')
    labels = ["age_stats_gender", "age_stats_overall", "age_stats_race","sex_percentage","race_percentage","clinical_stats",
               "alive_dead_percentage","lowest_highest_diag","lowest_highest_death","min_max_state","min_max_zipcode"]
    statsInLst  = getStats(dataIn)
    statsOutLst = getStats(dataOut)
    for lbl, x, y in zip(labels,statsInLst,statsOutLst):
        print(lbl + "   --------------------------")
        print(statsInLst[x])
        print(statsOutLst[y])

                
def main(datasetName, cfgName):
    print("Charting data for ",datasetName, cfgName)
    inputDataPath  = os.path.join("./data",datasetName,datasetName+".csv")
    outputDataPath = os.path.join("./data",datasetName,"results",cfgName,datasetName+"_output.csv")    
    resultPath     = os.path.join("./data",datasetName,"results",cfgName,"charts")
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    # read input and output csv data fiels 
    dataIn = []; dataOut = [] 
    with open(inputDataPath, newline='') as csvfile:
        dataIn = list(csv.reader(csvfile))
    with open(outputDataPath, newline='') as csvfile:
        dataOut = list(csv.reader(csvfile))

    dataIn  = [x[0].split(";") for x in dataIn]
    dataOut = [x[0].split(";") for x in dataOut]
    # for x in dataIn[:3]:
    #     print(x)
    # for x in dataOut[:3]:
    #     print(x)
    data = [dataIn,dataOut]

    # read risk results data
    riskInData  = extract_risk_values(os.path.join("./data",datasetName,"results",cfgName,datasetName+"_risk_rpt_input.txt"))
    riskOutData = extract_risk_values(os.path.join("./data",datasetName,"results",cfgName,datasetName+"_risk_rpt_output.txt"))
    for x in riskInData:
        print(x, riskInData[x])

    titles      = ["Max Risk Prosecutor","Max Risk Journalist","Max Risk Marketer"]    
    percentagesIn  = [round(riskInData[x]*100,2)  for x in titles]
    percentagesOut = [round(riskOutData[x]*100,2) for x in titles]

    titlesLbls      = ["Prosecutor","Journalist","Marketer"]    
    createSpeedoMeterCharts(percentagesIn, titlesLbls, percentagesOut, titlesLbls, resultPath)

    titles = ["Discernibility", "MSE", "Granularity", "Non-Uniform Entropy","Precision", "Ambiguity"]
    #titlesIn       = [x for x in riskInData if (x not in titles) and (riskInData[x]<=1) ]    
    percentagesIn  = [round(riskInData[x]*100,2) for x in titles]
    #titlesOut      = [x for x in riskOutData if (x not in titles) and (riskOutData[x]<=1) ]    
    percentagesOut = [round(riskOutData[x]*100,2) for x in titles]

    createTableCharts ([titles,percentagesIn],[titles,percentagesOut],"title", resultPath)
    createFrequencyCharts(data, resultPath)
    #createContengencyMapCharts(data, resultPath)
    
    
 
if __name__ == "__main__":    
    print("=============================================")
    print("    Data Charting Tool")
    print("=============================================")
   
    #main(datasetName,config_name=None,data_config_name=None)
    if len(sys.argv) < 3:        
        print(" Please provide dataset and config names")
        sys.exit(1)

    main(sys.argv[1],sys.argv[2]) 
    #getStatsAll(sys.argv[1],sys.argv[2])
