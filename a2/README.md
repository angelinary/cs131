# datacollector

## what it does

this command reads a semicolon delimited .csv and generates a summary of the file which contains the column names as well as min, max, mean and standard deviation of the columns.

first the program will prompt you for a file. You will need to enter the url. Then the program will distinguish if it is a .zip file or not, then it will download the file(s) into a tempdirectory (literal name). 
Then the program runs `awk` to print the column names into the output file- it looks atthe first line of the .csv file and cuts it by delimiter.
To extract the statistical data first the program counts the number of columns by counting the # of delimiters +1 present in the first line. Then, it runs another `awk` on every column to extract all values from that column, and appends them to the output file.
Note: since the sample url had multiple .csv files, the summary files are pre-fixed with the name of the .csv. 
## how to run

```
bash datacollector.sh
```

## sample output

# Feature Summary for  tempdirectory/winequality-red.csv

## Feature Index and Names 
1. fixed acidity
2. volatile acidity
3. citric acid
4. residual sugar
5. chlorides
6. free sulfur dioxide
7. total sulfur dioxide
8. density
9. pH
10. sulphates
11. alcohol
12. quality
## Statistics (Numerical Features)
| Index | Feature           | Min  | Max  | Mean  | StdDev |
|-------|-------------------|------|------|-------|--------|
|1|fixed acidity|4.60|15.90|8.320|1.741|
|2|volatile acidity|0.12|1.58|0.528|0.179|
|3|citric acid|0.00|1.00|0.271|0.195|
|4|residual sugar|0.90|15.50|2.539|1.409|
|5|chlorides|0.01|0.61|0.087|0.047|
|6|free sulfur dioxide|1.00|72.00|15.875|10.457|
|7|total sulfur dioxide|6.00|289.00|46.468|32.885|
|8|density|0.99|1.00|0.997|0.002|
|9|pH|2.74|4.01|3.311|0.154|
|10|sulphates|0.33|2.00|0.658|0.169|
|11|alcohol|8.40|14.90|10.423|1.065|
|12|quality|3.00|8.00|5.636|0.807|
