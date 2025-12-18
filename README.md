# ViBEx

This tool works as a visualizer, and probabilistic analysis for different binarizations of time-series gene expressions. In addition, it includes Gene Regulatory Network and Boolean Network analysis. Boolean functions can be inferred based on selected binarizations. Different value imputations are available for undecided states of each binarization (based on probabilistic framework). Boolan functions can be uploaded to draw Boolean function or perform metrics based on inferred boolean functions. Time-series data must be in .csv format to properly upload to the application.

## Experiments

- We performed various experiments using datasets for E coli. sos repair, Yeast cell, and p53-MDM2 network. 
- Go to folder "datasets" where each gene expression is available for each system. Each system boolean functions are available. 
- Experiments were run for each dataset with binarizations BASC A, K-Means, and Onestep (Elected binarization is created based on selected binarizations, this is from the probabilistic framework). 
- Two value imputations strategies were done as a case study comparing performance. These are:
  - (1) probabilistic imputation and MissForest imputation
  - (2) only MissForest imputation
- To run experiments we created the following script to simulate the app. This script is at src folder:
```
python script.py
```
- As a result a csv file will download once metrics evaluation is finished. Here the dynamic accuracy, accuracy, precision, recall, and F1-score for each inference method and binarization are downloaded. 

- To run experiments follow the previous explination of the experiments to obtain results. 
- We added a script called script.py to allow the performance evaluation be done without the tool. We recommend that if experiments are to be run, use the tool instead of the script. The following are how to use the tool. 

## TOOL ONLINE:
- The tool is available online at https://fury.hpcf.upr.edu/vibex/

## TO RUN LOCALLY:

- Have Python3.10 or higher installed
- Go to:
```
cd src
```
- Run Makefile command:
```
make all
```
- Install requirements with:
```
pip install -r /path/to/requirements.txt
```
- Go to the folder with the code and run:
```
python app.py
```
- Go to the local address stated on the terminal on your
	browser of choice
- Use CTRL + C to shut down the local server once finished

## HOW TO USE

1. Click on **UPLOAD GENE EXPRESSION FILE** and upload a time series dataset in CSV format first column should be gene names (each row is a gene expression).
2. Select individual genes by clicking on the checkboxes. Deselect by clicking the checkbox again
  - Select all genes by clicking **SELECT ALL**
  - Deselect all selections by clicking **DESELECT ALL**
3. Click on the *Select binarization method* dropdown to select a threshold algorithm
  - Multiple can be selected at once
  - Click on **SELECT ALL** to select all available algorithms
  - Click on **DOWNLOAD CSV** to obtain a CSV file of the threshold for each gene calculated by
	each selected algorithm

### BINARIZATION TAB

 - Displays binarization of a gene from each algorithm's thresholds
 - Click on *Select gene to visuliaze and binarize* dropdown to select another gene

### DISPLACEMENT TAB
 

1. Thresholds Tab
  - Displays a rough line graph of the gene with each threshold displayed
  - Shows the interpolation line of gene
  - Graph can be zoomed in or out
  - Graph view can be moved with click and drag
 - Hover over a point to see its value
 - Hover over a line to see the threshold value
 
2. Displacement Tab
 - Graphs according to selected algorithms
 - Displays the original gene points' line
 - Displays the displacement range of each threshold method
 - Hover over a point to see its value


### STATISTICS TAB

- Shows the highest probability string based on selected binarization methods.

### NETWORK TAB

1. Binarization Table
- Shows each threshold method binarization as a table
- Allows values imputation for undecided states
2. Binarization State Path
- Drawing a plot of the binarization path
3. Inference Boolean Network
- The "Run Script to Download Metrics" button allows the ability to download a CSV with performance metrics. This is based on the current uploaded dataset, boolean functions, and selected threshold methods. Make sure the data has no undecided states. 
- Infers Boolean Functions based on binarization
- Select inference method
- Select binarization to use
- Shows Boolean Function and Gene Regulatory Network Inferred
- Shows Boolean Network of inferred functions
- Computes Dynamic Accuracy based on binarization and path extracted from inferred rules
- Shows table comparing binarization and path extracted from inferred rules
4. Upload Boolean Functions
- Creates Boolean Network based on uploaded Boolean Functions
- Compares uploaded Boolean Functions with inferred Functions 
- Computes: Accuracy, precision, recall, and F1-score (comparing functions)
- Shows GRN and Boolean Network of uploaded and inferred Boolean Functions
5. Analysis
- Based on uploaded functions it extracts a path based on binarizations
- Does Hamming distance analysis comparing each chain 