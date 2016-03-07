#!/usr/bin/env python

import csv
import sys

BLANK = "NA"

files_names = sys.argv[1:-1]
output_csv_name = sys.argv[-1]

files_names = [f.split(":") for f in files_names]

if len(files_names) < 1:
	print "Usage: " + sys.argv[0] + "file:column_with_key [file:column_with_key]+ outputfile.csv"
	print "merges multiple CSV files with their headers into single lines."
	exit()


def get_data(filename, columnname):
	rows = []
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		
		rows = [ row for row in reader]
	
	header = rows[0]
	rows   = rows[1:]
	
	if not columnname in header:
		print columnname + " is not in the header of " + filename + " aborting"
		exit(1)
	
	col = [i for i, name in enumerate(header) if name == columnname][0]
	
	newheader = header[:col] + header[col + 1:]  # split out the column header
	prefix = filename.split("/")[-1].split(".")[0]
	newheader = [prefix + " " + h for h in newheader]
	
	data = {}
	for row in rows:
		rowid = row[col]
		rowdata = (row[:col] + row[col + 1:])
		datadict = {x:y for x,y in zip(newheader, rowdata)}
		data[rowid] = datadict

	return columnname, data, newheader
	


columnname, data, header = get_data(*files_names[0])


for f, n in files_names[1:]:
	_,d2,n2 = get_data(f,n)
	
	# merge the two datasets
	for key in d2.keys():
		d = d2[key]
		if key in data:
			data[key].update(d)
		else:
			data[key] = d
	
	header = header + n2


# write back

# add back in the primary key column as the first one
fieldnames = [columnname] + header

# write out the data sorted by primary key



with open(output_csv_name, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    keys = sorted(data.keys())
    
    for key in keys:
    	d = data[key]
    	d[columnname] = key
    	writer.writerow(d)
