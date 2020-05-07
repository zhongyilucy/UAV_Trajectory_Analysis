import csv


sFileName='/Users/luzhongyi/Downloads/realtime_route_data.csv'
wFileName='/Users/luzhongyi/Downloads/realtime_route_data_edited.csv'
wwFileName='/Users/luzhongyi/Downloads/map.csv'

def openCSV(FileName):
	flight_status = []
	
	with open(wFileName, "w") as wcsvfile:
		writer = csv.writer(wcsvfile)
		writer.writerow(["name", "altitude_agl", "angular_vel_z", "compass_hdg", "yaw", "angular_vel_y", "angular_vel_x", "pitch", "linear_vel_x", "altitude_amsl", "altitude_relative", "battery_volts", "ros_time", "linear_vel_z", "linear_vel_y", "longitude", "latitude", "roll"])
		with open(sFileName,newline='',encoding='UTF-8') as csvfile:
			rows=csv.reader(csvfile)
			with open(wwFileName, "w") as wwcsvfile:
				wwriter = csv.writer(wwcsvfile)
				wwriter.writerow(["name", "longitude" ,"latitude"])
				i = 0
				for row in rows:
					element = dict()
					newRoww = [str(i) + "point"]
					newRow = [str(i) + "point"]
					for each in row:
						x = each.split(": ")
						element[x[0]] = x[1]
						if x[0]=="longitude" or x[0]=="latitude":
							newRoww.append(x[1]+'\t')
						newRow.append(x[1]+'\t')
					flight_status.append(element)
					wwriter.writerow(newRoww)
					writer.writerow(newRow)
					print(newRoww);
				
					i = i + 1
	return flight_status
openCSV(sFileName)
	