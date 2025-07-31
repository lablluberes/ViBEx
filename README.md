# ViBEx

This tool works as a visualizer for different binarizations of
time-series gene expressions. Time-series data must be in .csv
format to properly upload to the application.

## TO RUN ONLINE:

go to https://vibex.onrender.com

## TO RUN LOCALLY:

- Have Python3 installed
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

1. Click on **UPLOAD GENE EXPRESSION FILE** and upload a time series dataset in CSV format first column should be gene names. 
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
 - Click on *Select gene to visulize and binarize* dropdown to select another gene

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

1. Binarization State Table
- Shows each threshold method binarization as a table
- Allows values imputation for undecided states
2. Binarization State Path
- Drawing a plot of the binarization path
3. Inference Boolean Network
- Infers boolean Functions based on binarization
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

# PROBABILISTIC ANALYSIS

#### Credits

- loading.py -> https://github.com/Lguanghui/TermLoading
