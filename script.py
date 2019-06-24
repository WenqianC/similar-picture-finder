import requests
import os
import numpy as np
import heapq
import time

global deno #用来降低计算量。ml包返回的结果长2048
deno = 16

def getVectors():
    file_name = open('./vectors.txt', 'r')
    lines = file_name.readlines()
    picNames = []
    picFeatures = []
    for idx, line in enumerate(lines):
        if idx % 2 == 0:
            # idx为偶数时存储的是图片名称
            picNames.append(line.replace('\n', ""))
        else:
            # idx为奇数时存储的是特征向量
            picFeatures.append(list(map(float, line.replace('\n', "")[1:-1].split(","))))
    return picNames, picFeatures

def resToTxt(s1, l1):
    # Hardcode的用以存储特征向量的txt
    file_name = open('./result.txt', 'a+')
    # 将图片名写入txt
    file_name.write(s1 + '\n')
    # 将特征向量转换为字符串写入txt
    file_name.write('\t' + str(l1) + '\n\n')
    file_name.close()


def getFeature(pic):
    # Leonardo API URL
    url = 'https://sandbox.api.sap.com/mlfs/api/v2/image/feature-extraction'
    # http request的header，记得把<API-KEY>换成你自己的key
    headers = {
        "Accept": "application/json",
        "APIKey": "记得把<API-KEY>换成你自己的key"
    }
    # 打开参数指向的图片
    files = {'files': open(pic, 'rb')}
    r = requests.post(url, files=files, headers=headers)
    #print(r.json())
    if not ("error" in r.json()):
        # 返回图片的特征向量
        return r.json()['predictions'][0]['featureVectors']
    else:
        print("%s has error!\n" %pic)

def decreaseArray(arr, deno):
    l = int(np.size(arr)/deno)
    for i in range(l):
        arr[i] = arr[deno*i]
    arr = arr[0:l]
    return arr

def findMostSimiliar(fileNames, featureVectors, feature):
    #维度为2048，想改成2048/16
    global deno;
    feature = decreaseArray(feature, deno);
    # 将数组都转换为numpy的ndarray，能极大的加速之后的计算
    featureVectors = np.array(featureVectors);
    feature = np.array(feature);
    # 计算目标特征向量和所有特征向量的向量距离
    distances = np.sum(np.square(featureVectors - feature), axis=1)
    # 找出2个最小距离对应的向量的index
    min2 = heapq.nsmallest(2, distances)
    minIdx1 = np.where(distances == min2[0])[0][0]
    minIdx2 = np.where(distances == min2[1])[0][0]
    ratio = min2[1]/min2[0];
    resName = [];
    print("最匹配文件：%s\n" %fileNames[minIdx1])
    resName.append(fileNames[minIdx1])
    resName.append(fileNames[minIdx2])
    # 返回index对应的图片名
    return resName, ratio

def matchSimiliar(pic):
    # 提取图片的特征向量
    feature = getFeature(pic);
    # 获取图片库以及鱼片库对应的向量
    # start = time.perf_counter() 
    fileNames, featureVectors = getVectors();
    # print("读取图片指纹时间： %f" %(time.perf_counter() - start))
    # 找到最近似的图片，并返回图片名
    # start = time.perf_counter() 
    res, ratio = findMostSimiliar(fileNames, featureVectors, feature)
    # print("计算时间： %f" %(time.perf_counter() - start))
    return res, ratio


pic_path = "./checkBoughtOrNot/"#需要查找重复与否的图片目录
dataPic_path = "./dataPic/";
path_list = os.listdir(pic_path)
for idx, each_path in enumerate(path_list):
    if each_path.endswith('jpg') or each_path.endswith('png') or each_path.endswith('bmp'):
        print("查重目标图片为：%s" %each_path)
        picName = pic_path + each_path
        res, ratio = matchSimiliar(picName)
        # 保存至txt中
        resToTxt(each_path, res)
        cm1 = "open " + dataPic_path + res[0];
        
        os.system(cm1);
        if ratio > 2: #第二张图差太多就不用看了
            cm2 = "open " + dataPic_path + res[1];
            os.system(cm2);





