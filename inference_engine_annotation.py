
# coding: utf-8

# In[7]:


#######
import os
import os.path
import requests
import pandas as pd 
import numpy as np 
from sklearn.externals import joblib###
from sklearn.metrics import accuracy_score###
from flask import Flask, jsonify
from flask import request
import base64
import json


jsonData_107 ={}
jsonData_107['timeEnd'] =' '

jsonData_106 ={}
jsonData_106['timeEnd'] =' '

app = Flask(__name__)



@app.route("/predict", methods=['POST'])
def query_prediction():
    global jsonData_107
    global jsonData_106
    ## Step 1, read the source data
    
    if request.method == 'POST':
        data=request.get_json()
        input_data = data['data']
        model_name = data["model_name"]
        print('===============================================================================')
        print('This time input json :')
        print(data)
        print(' ')
    
    X_ret = read_sample_db(input_data)
    
    ## Step2, load model and start to predict



    if(os.path.exists('/inference_engine/models/'+model_name+'.pkl')==False):
        message = {'error': 'model C:\inference_engine\models\{0} not found'.format(model_name)}
        print('Error 404 : model C:\inference_engine\models\{0}.pkl not found'.format(model_name))
        return jsonify(message), 404
    
    elif(os.path.exists('/inference_engine/models/'+model_name+'.pkl')==True):
        predict_data = load_sample_model('/inference_engine/models/'+model_name+'.pkl', X_ret)
        print('predict answer :')
        print(predict_data)
        print('              ')
        print('data point:')
        print(data['tags'])
        print(' ')
    ## Step3, write the predicted data into destination
    
        write_model_info(predict_data , model_name)


        #return jsonify({'message': 'predict success'})
    ##判斷是否有啟用annotation模式
        data['text'] = predict_data
        if data['annotation_enable'] == 0 :
    ##判斷是否被標註為異常並且是第一筆資料，如是就初始化所有的資訊
            if data['tags'] =='1Y520210107' :
                if data['text'] == '[-1]' and jsonData_107['timeEnd'] ==' ' :
                    header = {}
                    jsonData_107 = {}
                    jsonData_107['dashboardId']= data['dashboardId']
                    jsonData_107['panelId']= data['panelId']
                    jsonData_107['time']= data['time']
                    jsonData_107['isRegion']= True
                    jsonData_107['timeEnd']= data['timeEnd']
                    jsonData_107['tags']= data['tags']
                    jsonData_107['text']= data['text']
                    url = data['url']
                    header['Content-Type']= 'application/json'
                    header['Accept']= 'application/json'
                    user = data['user']
                    password = data['password']
                    header['Authorization'] =   encode_base64(user,password)
                    print('predict success(1): This Data is first predict answer = [-1] Data')
                    print(jsonData_107)
                    return jsonify({'message': 'predict success(1)'})
            ##判斷是否為正常並且是第一筆資料或為連續的正常資料，如是就不記
                elif data['text'] == '[1]' and jsonData_107['timeEnd'] == ' ' :
                    print('predict success(2): This Data is first predict answer = [1] or last predict answer and this time predict answer = [1]')
                    #print(jsonData)
                    return jsonify({'message': 'predict success(2)'})
            ##判斷是否為連續標註異常的資料，如是就更新timeEnd
                elif data['text'] == '[-1]' and jsonData_107['timeEnd'] != ' ' :
                    jsonData_107['timeEnd']= data['timeEnd']
                    print('predict success(3): Last predict answer and this time predict answer is [-1] too')
                    print(jsonData_107)
                    return jsonify({'message': 'predict success(3)'})
            ##判斷是否中斷了連續標註異常的資料，如是就把之前更新的annotation資訊送出
                elif data['text'] == '[1]' and jsonData_107['timeEnd'] != ' ' :
                    header = {}
                    jsonData_107['dashboardId']= data['dashboardId']
                    jsonData_107['panelId']= data['panelId']
                    jsonData_107['isRegion']= True
                    #jsonData['tags']= data['tags']
                    jsonData_107['text']= '[-1]'
                    url = data['url']
                    header['Content-Type']= 'application/json'
                    header['Accept']= 'application/json'
                    user = data['user']
                    password = data['password']
                    header['Authorization'] =   encode_base64(user,password)
                    #header_json = json.dumps(header)
                    jsonData_json = json.dumps(jsonData_107)
                    #test_header ={"Content-Type":"application/json","Accept":"application/json","Authorization":"Basic ZHVqYWtpdnVrQHN0b3JpcWF4LmNvbTpRV2VyMTIzIQ=="}
                    #print (header)
                    #print (url)
                    #print (jsonData_json)
                    rsp = requests.post(url, headers=header, data=jsonData_json)
                    status_code = str(rsp.status_code)
                    predict_success4 = 'predict success(4):'+ 'grafana status code ' +status_code
                    print(predict_success4)
                    print(' ')
                    print('post to grafana json is :')
                    print(jsonData_json)
                    #print(rsp.text)
                    jsonData_107['timeEnd']=' '
                    return jsonify({'message': predict_success4 })
                else :
                    return 'json error',404

            elif data['tags'] =='1Y520210106' :
                if data['text'] == '[-1]' and jsonData_106['timeEnd'] ==' ' :
                    header = {}
                    jsonData_106 = {}
                    jsonData_106['dashboardId']= data['dashboardId']
                    jsonData_106['panelId']= data['panelId']
                    jsonData_106['time']= data['time']
                    jsonData_106['isRegion']= True
                    jsonData_106['timeEnd']= data['timeEnd']
                    jsonData_106['tags']= data['tags']
                    jsonData_106['text']= data['text']
                    url = data['url']
                    header['Content-Type']= 'application/json'
                    header['Accept']= 'application/json'
                    user = data['user']
                    password = data['password']
                    header['Authorization'] =   encode_base64(user,password)
                    print('predict success(1): This Data is first predict answer = [-1] Data')
                    print(jsonData_106)
                    return jsonify({'message': 'predict success(1)'})
            ##判斷是否為正常並且是第一筆資料或為連續的正常資料，如是就不記
                elif data['text'] == '[1]' and jsonData_106['timeEnd'] == ' ' :
                    print('predict success(2): This Data is first predict answer = [1] or last predict answer and this time predict answer = [1]')
                    #print(jsonData)
                    return jsonify({'message': 'predict success(2)'})
            ##判斷是否為連續標註異常的資料，如是就更新timeEnd
                elif data['text'] == '[-1]' and jsonData_106['timeEnd'] != ' ' :
                    jsonData_106['timeEnd']= data['timeEnd']
                    print('predict success(3): Last predict answer and this time predict answer is [-1] too')
                    print(jsonData_106)
                    return jsonify({'message': 'predict success(3)'})
            ##判斷是否中斷了連續標註異常的資料，如是就把之前更新的annotation資訊送出
                elif data['text'] == '[1]' and jsonData_106['timeEnd'] != ' ' :
                    header = {}
                    jsonData_106['dashboardId']= data['dashboardId']
                    jsonData_106['panelId']= data['panelId']
                    jsonData_106['isRegion']= True
                    #jsonData['tags']= data['tags']
                    jsonData_106['text']= '[-1]'
                    url = data['url']
                    header['Content-Type']= 'application/json'
                    header['Accept']= 'application/json'
                    user = data['user']
                    password = data['password']
                    header['Authorization'] =   encode_base64(user,password)
                    #header_json = json.dumps(header)
                    jsonData_json = json.dumps(jsonData_106)
                    #test_header ={"Content-Type":"application/json","Accept":"application/json","Authorization":"Basic ZHVqYWtpdnVrQHN0b3JpcWF4LmNvbTpRV2VyMTIzIQ=="}
                    #print (header)
                    #print (url)
                    #print (jsonData_json)
                    rsp = requests.post(url, headers=header, data=jsonData_json)
                    status_code = str(rsp.status_code)
                    predict_success4 = 'predict success(4):'+ 'grafana status code ' +status_code
                    print(predict_success4)
                    print(' ')
                    print('post to grafana json is :')
                    print(jsonData_json)
                    #print(rsp.text)
                    jsonData_106['timeEnd']=' '
                    return jsonify({'message': predict_success4 })
                else :
                    return 'json error',404
            else:
                print('post data is not 107 or 106')
                return 'post data is not 107 or 106'

        else :
            print('predict succes(5)')
            return jsonify({'message': 'predict succes(5)'})




def load_sample_model(filepath, training_data):  
    clf = joblib.load(filepath) 
    y_pre = clf['model'].predict(clf['scaler'].transform(training_data)) 
    y_pred =y_pre[0]
    y_pred = str(y_pre) 
    return y_pred 
    pass 

def read_sample_db(df): 
     
    data1 = pd.DataFrame(df) 
    data1 = np.array(data1) 
    X_test = data1.reshape(1,47) 
    return X_test 
    pass

def write_model_info(pre , model_name):    
    if (os.path.exists("/inference_engine/results/"+model_name+"_predict_result.txt")==True):
        with open('/inference_engine/results/'+model_name+'_predict_result.txt','a') as df2:
            df2.write(",")
            df2.write(pre)
    elif (os.path.exists("/inference_engine/results/"+model_name+"_predict_result.txt")==False):
        with open('/inference_engine/results/'+model_name+'_predict_result.txt','w') as df1:
            df1.write(pre)
    pass

def encode_base64(username, password):
    str_user = username + ':' + password
    str_user_byte = str_user.encode('utf8') # string to byte
    str_user_encode64 = base64.b64encode(str_user_byte) # encode by base64
    str_user_string = str_user_encode64.decode('utf8') # byte to string
    str_auth = 'Basic ' + str(str_user_string)

    return str_auth

    

port = os.getenv('PORT', '7500')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(port))




