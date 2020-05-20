import csv
from math import sin, asin, cos, radians, fabs, sqrt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

#calculate distance with GPS
EARTH_RADIUS=6378137  

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
 
    return distance


name = []
velocityX = []
velocityY = []
velocityZ = []
time = []
accX = []
accY = []
accZ = []
GPSlng = []
GPSlat = []
GPSlngFake = []
position = []
positionFake=[]

#read false data
with open('/Users/luzhongyi/Desktop/test_10_false.csv','r',encoding='UTF-8') as file:
	reader1 = csv.reader(file);
	for i in reader1:
		GPSlngFake.append(float(i[5]))
#read all the data
with open('/Users/luzhongyi/Desktop/test_10.csv','r',encoding='UTF-8') as f:
	reader = csv.reader(f)
	for i in reader:
		name.append(i[0])
		velocityX.append(float(i[1]))
		velocityY.append(round(float(i[2]),12))
		velocityZ.append(float(i[3]))
		time.append(int(i[4])-7068959)
		GPSlng.append(float(i[5]))
		GPSlat.append(float(i[6]))

#calculate acceleration of three directions
accX.append(0)
accY.append(0)
accZ.append(0)
i = 1
while i < len(name)-1:
	accX.append(velocityX[i+1]-velocityX[i])
	accY.append(velocityY[i+1]-velocityY[i])
	accZ.append(velocityZ[i+1]-velocityZ[i])
	i = i + 1
#calculate the position change
i = 0
position.append(0)
positionFake.append(0)
while i < len(name)-1:
	position.append(get_distance_hav(GPSlat[i],GPSlng[i],GPSlat[i+1],GPSlng[i+1]))
	positionFake.append(get_distance_hav(GPSlat[i],GPSlngFake[i],GPSlat[i+1],GPSlngFake[i+1]))
	i = i + 1

pos = np.array(position)
posFake = np.array(positionFake)
t = np.array(time)

position_noise = posFake+np.random.normal(0,0.5,size=(t.shape[0]))



predicts = [position_noise[0]]
position_predict = predicts[0]

predict_var = 0#预测方差
odo_var = 0.01 #这是我们自己设定的位置测量仪器的方差，越大则测量值占比越低，位置误差方差
v_std = 1 # 速度标准差
for i in range(1,t.shape[0]):#循环从1开始到样本数前一个结束
  
    dv =  (positionFake[i]-positionFake[i-1]) + np.random.normal(0,1) # 模拟从IMU读取出的速度
    #------------------预测--------------------
    position_predict = position_predict + dv # 利用上个时刻的位置和速度预测当前位置
    predict_var += v_std**2 # 预测速度方差
    # ---------------更新------------------------
    #根据权重更新位置预测
    position_predict = position_predict*odo_var/(predict_var + odo_var)+position_noise[i]*predict_var/(predict_var + odo_var)
    predict_var = (predict_var * odo_var)/(predict_var + odo_var)**2#更新速度方差
    predicts.append(position_predict)


#show the lines above

plt.plot(time,posFake,label='Fake position')

#plt.plot(t,predicts,label='kalman filtered position')



error = []

print(predicts[28]-posFake[28])
print(predicts[29]-posFake[29])
print(predicts[30]-posFake[30])
print(predicts[31]-posFake[31])
for x in np.arange(0, t.shape[0]):
    if predicts[x] - posFake[x]<-0.5 or predicts[x] - posFake[x] > 0.5:
        error.append(x)

imputeRange =[]
posRenew = posFake
for each in error:
    print(each)
    posRenew[each] = np.nan
    GPSlngFake[each] = np.nan
    imputeRange.append([each-2,each-1,each,each+1,each+2])

imputation_transformer = SimpleImputer(np.nan, "mean")
posImpute = imputation_transformer.fit_transform(posRenew.reshape(-1,1))
#plt.plot(t,posImpute,label='Impute')

GPSRenew = GPSlngFake
for each in imputeRange:
    media = []
    for y in each:
        media.append(GPSRenew[y])
    mediaNd = np.array(media)
    mediaImp = imputation_transformer.fit_transform(mediaNd.reshape(-1,1))
    GPSRenew[each[2]] = mediaImp[2][0]

positionImpute = []
i = 0
positionImpute.append(0)
while i < len(name)-1:
    positionImpute.append(get_distance_hav(GPSlat[i],GPSRenew[i],GPSlat[i+1],GPSRenew[i+1]))
    i = i + 1

with open("/Users/luzhongyi/Desktop/result_test_2.csv", "w") as wcsvfile:
        writer = csv.writer(wcsvfile)
        i = 0
        while i < len(GPSlat):
            writer.writerow([GPSlat[i],GPSRenew[i]])
            i = i + 1




plt.plot(t,pos,label='truth position')
plt.plot(time,positionImpute,label='Imputation')

plt.legend()


plt.show()

