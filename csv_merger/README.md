Merges multiple CSV files based on a column key, sort of like doing a JOIN on SQL tables

For example, let's say you had the files:

`history.csv`

	Student,Grade
	Joe,A
	Bob,C
	Sally,B+
	George,F

`english.csv`

	student,midterm,final
	Bob,88,0
	Sally,73,30

`graduating.csv`

	ID,name,classrank
	0,Jenn,1
	1,Sally,2
	2,Joe,3

You could combine them using `csv_merger.py`:

	python csv_merger.py example/history.csv:Student example/english.csv:student \
	example/graduating.csv:name output.csv


	Student,history Grade,english midterm,english final,graduating ID,graduating classrank
	Bob,C,88,0,,
	George,F,,,,
	Jenn,,,,0,1
	Joe,A,,,2,3
	Sally,B+,73,30,1,2

Non-existant columns for a given element are entered as blanks.
