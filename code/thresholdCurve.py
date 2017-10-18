# -*- coding: UTF-8 -*-
from __future__ import division
import re
import os
import matplotlib.pyplot as plt
#allResult 文件格式：pid,probility(预测为类别1的概率0-1),result(真实结果，即是否为类别1、类别2)
allResult = open("E:/test/ll.txt","r")
output = open("E:/test/result.txt","a")
imgOut = "E:/test/threshold.png"
thresholdR =[]
prob = []
classFlg = []
for line in allResult.readlines()[1:]:
    thresholdR.append(float(line.split(",")[1].strip("'")))
    prob.append(float(line.split(",")[1]))
    classFlg.append(int(line.split(",")[2]))
#各个坐标轴结果值的存储
thresholdX = []
infRecallY = []
infPrecisionY =[]
unRecallY = []
unPrecisionY = []
infFmY = []
unfFmY = []
#非重复的阈值个数
thresholdSet = set(thresholdR)
thresholdSet = sorted(thresholdSet)
outArr = []  # 将结果输出到文件
output.write("threshold,infectedRecall,infectedPrecision,infectedFM,unfectedRecall,unfectedPrecision,unfectedFM"+"\n")
output.flush()
for threshold in thresholdSet:
    TP = 0
    FN = 0
    FP = 0
    TN = 0
    infRecall = 0
    infPrecision = 0
    unRecall = 0
    unPrecision = 0
    for i in range(len(prob)):
        if (prob[i]>= float(threshold)):
           if (classFlg[i] == 1): TP = TP + 1
           if (classFlg[i] == 0): FP = FP + 1
        else:
           if (classFlg[i] == 1): FN = FN + 1
           if (classFlg[i] == 0): TN = TN + 1
    print(threshold,"TP=", TP,"FP=", FP,"TN=", TN, "FN=",FN)

    if(TP+FN==0):
        infRecall = 0
    else:
        infRecall = TP/(TP+FN)
    if(TP==0):
        infPrecision = 0
    else:
        infPrecision = TP/(TP+FP)
    if(FP+TN==0):
        unRecall=0
    else:
        unRecall = TN/(FP+TN)
    if(FN+TN==0):
        unPrecision = 0
    else:
        unPrecision = TN/(FN+TN)

    #若全部预测为感染或者全部预测为非感染
    if (infRecall + infPrecision == 0):
        infFm = 0
    else:
        infFm = (2 * infRecall * infPrecision) / (infRecall + infPrecision)
    if(unRecall + unPrecision==0):
        unfFm = 0
    else:
        unfFm = (2 * unRecall * unPrecision) / (unRecall + unPrecision)
    #将各个结果存储到数组中，并用于后期生成曲线
    thresholdX.append(threshold)
    infRecallY.append(infRecall)
    infPrecisionY.append(infPrecision)
    unRecallY.append(unRecall)
    unPrecisionY.append(unPrecision)
    infFmY.append(infFm)
    unfFmY.append(unfFm)
    outStr = str(threshold)+","+str(infRecall)+","+str(infPrecision)+","+str(infFm)+","+str(unRecall)+","+str(unPrecision)+","+str(unfFm)
    outArr.append(outStr)

#将结果存储到文件
for lins in outArr:
    output.write(lins+"\n")
    output.flush()
output.close()
allResult.close()
#plot the graph..
plt.plot(thresholdX,infRecallY,'r--',label='infRecallY')
plt.plot(thresholdX,unRecallY,'mo-',label='unRecallY')
plt.plot(thresholdX,infPrecisionY,'g-.',label='infPrecisionY')
plt.plot(thresholdX,unPrecisionY,'b--',label='unPrecisionY')
plt.plot(thresholdX,infFmY,'y--',label='infFmY')
plt.plot(thresholdX,unfFmY,'m-',label='unfFmY')
plt.title('threshold graph')
plt.xlabel("threshold")
plt.legend()
plt.ylabel("result")
plt.xticks(thresholdX,rotation=70)
plt.savefig(imgOut)
plt.show()
