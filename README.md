This is a project to explore various PLC programing softwares, in an effort to create a means of producing 
source code from Ladder diagram project files. One component is the simple logic processing of ladder diagrams. Another component
is reading existing project files and performing a conversion to C, C++, python, or other high level languages. 
The general goal is to read in a project file and deconstruct it into configuration files, and source code. 
The extended goal is to be able to deconstruct a project, make modifications using high level language, 
then rebuild a viable project file. 

Example Useage:
$ plc2c PLC.project

A copy of the program is made in a subdirectory of the same basename, and the coppied source is then deconstructed into configuration files, 
and source files. 

An API is comming, but writing it sounds tedious. 

Current status of this project is analysis, and method development. 
I wanted to link a repo in some offical docuemtnation, so I created this repo. 
Analysis is on going, but I have enough info to be able to deconstruct 
and predict having a basic generator script going soon. This is an on going project.
