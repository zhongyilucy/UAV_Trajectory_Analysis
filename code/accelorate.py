import csv

name = []
velocityX = []
velocityY = []
velocityZ = []
time = []
accX = []
accY = []
accZ = []
GPSLong = []
GPSAl = []
#read all the data
with open('/Users/luzhongyi/Desktop/data_velocity_GPS.csv','r',encoding='UTF-8') as f:
	reader = csv.reader(f)
	for i in reader:
		name.append(i[0])
		velocityX.append(float(i[1]))
		velocityY.append(round(float(i[2]),12))
		velocityZ.append(float(i[3]))
		time.append(int(i[4])-1579810097)
		GPSLong.append(float(i[5]))
		GPSAl.append(float(i[6]))
#calculate velocity of three directions
accX.append(0)
accY.append(0)
accZ.append(0)
i = 1
while i < len(name)-1:
	accX.append(velocityX[i+1]-velocityX[i])
	accY.append(velocityY[i+1]-velocityY[i])
	accZ.append(velocityZ[i+1]-velocityZ[i])
	i = i + 1