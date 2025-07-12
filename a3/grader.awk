# This is the grader.awk program.

# User defined function for the calculation of the average grade point.
function calc_avg(total, n) { #takes 2 arguments, note that in awk, you do not declare types for vars or fnct args
	return total  / n    # returns the result of total / n. Note the need for an escape character prior to /
}

BEGIN { # commands in this section are done once
	FS = "," #Set commas as a field separator
	print "Student results are as follows: "
	print " "

}

# commands in this section are done on each line
NR > 1 { # Number of Records is the line number. If it is not the heading line, then do smth
	id = $1 # id variable takes the first field on each line we are processing
	name = $2 # name variable takes field number 2
	sum = 0 # sum var is initiated to 0, because it should later be updated.

	# This for loop goes over the number of fields within the scope of "grades", which is fields 3+ inclusive, and finds sum


	for(i = 3; i <=  NF; i++){
		sum += $i # sum is equal to sum plus each updated value of variable (field) i
	}
	
	#Save total and average in arrays
	total[name] = sum # total is the array, [name] comes from the field, and it is assigned with sum that is calculated above
	avg[name] = calc_avg(sum, NF - 2) # This array is assigned with the result of the calc_avg function. NF-2 is the total fields minus name and SID fields.

	#These if statements determine if the student passed or failed, based on the 70 cut off.
	if(avg[name] >= 70){
		status[name] = "Pass" #This is an array named status that is associated with each student (line), and either "Pass" or "Fail" is assigned to it.
	} else {
		status[name] = "Fail"
	}

	#Track max and min. This compares the current min\max to each newly acquired value, and updates if needed.
	if(NR == 2 || sum > max){  #if NR is 2, then assign max with the only value we have so far, the sum for line 2.
		max = sum
		max_name = name
	}
	if(NR ==2 || sum < min){ # here again assign min with the first available sum. Note that we need 2 if statements, and not if-else. Otherwise you can only assign min or max for each NR
		min = sum
		min_name = name
	}
}

END{ #This section only runs once at the end. Not for each line
	for( n in total) { # for each available total (corresponds to num of students/lines below title, 
		printf "\nName of the student is: %s\n", n
		printf "Student's total score is: %d\n", total[n]
		printf "Student's average is: %.2f\n", avg[n]
		printf "Student's pass status is: %s\n", status[n]
	}
	printf "\nThe student with the following name scored the highest: " max_name "("max")"
	printf "\nThe student with the following name scored the lowest: " min_name "("min")\n"
}

