#!/usr/bin/env python3
"""
This program will look at the basename1, basename2 pjw files and attempt to assist a merge operation.

The way this may work is that there is an assertion Im making that the merging files are:
1. seperate parts of the same overall project, 
2. that the seperate parts are indeed seperate.
3. That one of the branches is more up to date than the other.

This will require asking the user which file is the main branch before proceding.
The files to be merged will not be edited, rather a merged file will be created.

steps:
0. run a diff on the projects to verfy the files are indeed different if so, proceed. 
create a project folder named merge ()or something.
decompress both projects into the project folder.
determine basenames of both files. 
create a new project file named basename merge
ask the user which basename is the main branch for merging.
# Gets hazy here...
***we're basicly making  diff function, for subsections
***with limited error checking. 
	**The error checking we want to do is for subsection headers, both the bytes, and 
	the N th order by extension, whereever they may appear. 

differential scans of basename1.data basename2.data
1. scan1: scan the main branch for relavent header types
	using N,basename.extension,,bytes
	make a reffernce file of these components.
	(we already know they differ)
2. 	scan2, scan basename2.data file
	 using N,basename.extension,,bytes
	2a. compare using N,basename.extension,,bytes to main branch
	
conditions:
		if mergerFile differs from main branch:
			1.print the byte difference
			2.log the subsectional difference of headers.
			3. ##ask user if they accept ?
			4.#### do the merge byte by byte
		
		If the subsections differ, but the byte count is the same:	
			1. print a warning
			2. log the warning
			3. ask the user about the change.
			4. proceed.
		if there are missing subsections:
			in main brach: add the missing subsections
			else proceed.
			
		if the missing subsections are out of order, 
			IDK man, try to put them in order with out creating duplicates
	
		
	

"""
