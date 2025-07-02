echo "Please enter the URL: " #Prompt user for input
read url #Read the URL and save it into url variable.
mkdir -p tempdirectory

if [[ "$url" == *.zip ]]; then   #[[]] provides for extrended patternmatching
	echo "The given URL leads to a .zip fie. Unzipping..."
	wget "$url" -O dataset.zip # wget is a command-tool downloading files fromt he internet, "$url" protects url from being mishandles due to spaces, and $indicates that it is a variable. -O is a flag that is like "output to this filename, and saves the url contents into a localized dataset.zip.
	unzip -d tempdirectory dataset.zip   # saves the files into the given directory  
else
	wget "$url" -O tempdirectory/dataset.csv  # saves into the given diretory instead of the current one 

fi

for FILE in tempdirectory/*.csv; do # for all files in the given directory
	OUTPUT="${FILE/.csv/-summary.md}"   #output is a nsw file with .csv replaced with summary.md
	OUTPUT="${OUTPUT/tempdirectory/.}"
	awk -F';' 'NR==1 {   #NR--> Number of rows
        print "# Feature Summary for  " FILENAME
        print "\n## Feature Index and Names "

        for(i=1; i<=NF; i++){  #NF --> number of fields
		field = $i
		gsub(/"/, "", field)	
		print i ". " field
        }

	print "## Statistics (Numerical Features)"
	print "| Index | Feature           | Min  | Max  | Mean  | StdDev |"
	print "|-------|-------------------|------|------|-------|--------|"

	}' "$FILE"  > "$OUTPUT"
	
cols=$(head -n 1 "$FILE" | tr -d -c ";" | wc -c) #This counts the number of delimiters and it is the column count for the second awk
	(( cols=cols+1 ))
	
	for (( c=1; c<=cols; c++ ))
	do 
		awk -F';' -v i="$c" '{
			if( NR==1){
				field = $i
				gsub(/"/, "", field)
			}
			else{
				sum += $i; sumsq += ($i)^2
			        if(min=="") {min=$i; max=$i}
			        if($i<min) min=$i
  		                if($i>max) max=$i
      				count++
			}
		}
		END {
			if(count>0){
	
				mean = sum/count
	      			stddev = sqrt((sumsq - (sum^2)/count)/count)
	      			printf "|%d|%s|%.2f|%.2f|%.3f|%.3f|\n", i, field, min, max, mean, stddev
			}
	
		}' "$FILE"  >> "$OUTPUT"
	done
	

done

