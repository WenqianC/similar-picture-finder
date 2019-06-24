import requests
import os
import numpy as np
import heapq

global deno #用来降低计算量。ml包返回的结果长2048
deno = 16

def appendToTxt(s1, l1):
    # Hardcode的用以存储特征向量的txt
    file_name = open('./vectors.txt', 'a+')
    # 将图片名写入txt
    file_name.write(s1 + '\n')
    # 将特征向量转换为字符串写入txt
    np.set_printoptions(suppress=True)
    file_name.write(str(l1) + '\n')
    file_name.close()

def decreaseArray(arr, deno):
    l = int(np.size(arr)/deno)
    for i in range(l):
        arr[i] = arr[deno*i]
    arr = arr[0:l]
    return arr

#用来生成目录下所有图片的指纹。之后把该目录下的图片移到dataPic就好了。
def readFeatures():
    # Leonardo API URL
    url = 'https://sandbox.api.sap.com/mlfs/api/v2/image/feature-extraction'
    # http request的header，记得把<API-KEY>换成你自己的key
    headers = {
        "Accept": "application/json",
        "APIKey": "记得把<API-KEY>换成你自己的key"
    }
    # 所有图片的地址
    pic_path = "./needCalc/"
    path_list = os.listdir(pic_path)
    for idx, each_path in enumerate(path_list):
        if each_path.endswith('jpg') or each_path.endswith('png') or each_path.endswith('bmp'):
            picName = pic_path + each_path
            picName = pic_path + each_path
            files = {'files': open(picName, 'rb')}
            r = requests.post(url, files=files, headers=headers)
            print(r)
            if not ("error" in r.json()):
                # 根据之前得到的JSON结构，获取特征向量
                featureVector = r.json()['predictions'][0]['featureVectors'];
                # 根据之前得到的JSON结构，获取图片名
                fileName = r.json()['predictions'][0]['name'];
                #维度为2048，想改成2048/16
                global deno;
                featureVector = decreaseArray(featureVector, deno);  
                # 保存至txt中
                appendToTxt(fileName, featureVector)
                cm = "mv " + picName + " " + "./dataPic/"
                os.system(cm);
            else:
                print("has error!\n")
    

# 调用readFeatures来将./needCalc下的图片全部转换为向量
# start = time.perf_counter()
readFeatures()
# print("生成图片指纹时间： %f" %(time.perf_counter() - start))