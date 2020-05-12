# UAV_Trajectory_Analysis
This is the code implementation of UAV Trajectory Analysis.

Inside this repository is a python program and files that store the flight data.

There are five files: a raw data file, the dataset after process, a .kml file used to draw the path on Google Map, a .csv file used to mark all the points on Google Map, and a file that contains wrong data which will be used to detect.

In the code folder there is a process_data.py that process the raw data into processed data.

Inside Analysis.py there are mainly three parts:
	1) Use GPS to calculate distance
	2) Use Kalman Filter to which points are wrong
	3) Impute the false points

To run this program:
	1) Download the file to the computer.
	2) Change the path in the code into the path that the data stores.
	3) Run the python file with terminal.

