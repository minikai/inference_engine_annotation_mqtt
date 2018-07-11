
# coding: utf-8



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
#from influxdb import InfluxDBClient
#from influxdb import exceptions
import configparser
import paho.mqtt.client as paho
import time


jsonData ={}
jsonData['timeEnd'] =' '

app = Flask(__name__)



@app.route("/predict", methods=['POST'])
def query_prediction():
    global jsonData
    ## Step 1, read the source data
    
    if request.method == 'POST':
        data=request.get_json()
        input_data = data['data']
        model_name = data["model_name"]
    
    X_ret = read_sample_db(input_data)
    
    ## Step2, load model and start to predict



    if(os.path.exists('/inference_engine/models/'+model_name+'.pkl')==False):
        message = {'error': 'model C:\inference_engine\models\{0} not found'.format(model_name)}
        print('Error 404 : model C:\inference_engine\models\{0}.pkl not found'.format(model_name))
        return jsonify(message), 404
    
    elif(os.path.exists('/inference_engine/models/'+model_name+'.pkl')==True):
        predict_data = load_sample_model('/inference_engine/models/'+model_name+'.pkl', X_ret)
    
    ## Step3, write the predicted data into destination
    
        write_model_info(predict_data , model_name)
        print('predict success')
        print(jsonData)
        #return jsonify({'message': 'predict success'})
    ##判斷是否有啟用annotation模式
        data['text'] = predict_data
        if data['annotation_enable'] == 0 :
    ##判斷是否被標註為異常並且是第一筆資料，如是就初始化所有的資訊

            if data['text'] == '[-1]' and jsonData['timeEnd'] ==' ' :
                header = {}
                jsonData = {}
                jsonData['dashboardId']= data['dashboardId']
                jsonData['panelId']= data['panelId']
                jsonData['time']= data['time']
                jsonData['isRegion']= True
                jsonData['timeEnd']= data['timeEnd']
                tags_list= []
                tags_list.append(str(predict_data))
                tags_list.append(data['tags'])
                #tags_list_json = json.dumps(tags_list)
                jsonData['tags']= tags_list
                jsonData['text']= data['text']
                url = data['url']
                header['Content-Type']= 'application/json'
                header['Accept']= 'application/json'
                user = data['user']
                password = data['password']
                header['Authorization'] =   encode_base64(user,password)
                annotation_times_mqtt()
                return jsonify({'message': 'predict success(1)'})

        ##判斷是否為正常並且是第一筆資料或為連續的正常資料，如是就不記
            elif data['text'] == '[1]' and jsonData['timeEnd'] == ' ' :
                return jsonify({'message': 'predict success(2)'})

        ##判斷是否為連續標註異常的資料，如是就更新timeEnd
            elif data['text'] == '[-1]' and jsonData['timeEnd'] != ' ' :
                jsonData['timeEnd']= data['timeEnd']
                annotation_times_mqtt()
                return jsonify({'message': 'predict success(3)'})

        ##判斷是否中斷了連續標註異常的資料，如是就把之前更新的annotation資訊送出
            elif data['text'] == '[1]' and jsonData['timeEnd'] != ' ' :
                header = {}
                jsonData['dashboardId']= data['dashboardId']
                jsonData['panelId']= data['panelId']
                jsonData['isRegion']= True
                #jsonData['tags']= data['tags']
                jsonData['text']= '[-1]'
                url = data['url']
                header['Content-Type']= 'application/json'
                header['Accept']= 'application/json'
                user = data['user']
                password = data['password']
                header['Authorization'] =   encode_base64(user,password)
                jsonData_json = json.dumps(jsonData)
                print (header)
                print (url)
                print (jsonData_json)
                rsp = requests.post(url, headers=header, data=jsonData_json)
                status_code = str(rsp.status_code)
                predict_success4 = 'predict success(4)'+ ' grafana status code ' +status_code
                jsonData['timeEnd']=' '
                return jsonify({'message': predict_success4 })

            else :
                return 'json error',404
        else :
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

#def annotation_times_to_influxdb(num):
#    config = configparser.ConfigParser()
#    config.read('ex_config.ini')
#    host = config['influxdb']['host']
#    port = config['influxdb']['port']
#    database = config['influxdb']['database']
#    username = config['influxdb']['username']
#    password = config['influxdb']['password']
#    measurement = config['influxdb']['measurement']
#    data = {}
#    data['measurement'] = measurement
#    tags = {}
#    tags['topic'] = 'annotation times'
#    data['tags'] = tags
#    field = {}
#    field['times'] = num
#    data['fields'] = field
#    influxdb_post = []
#    influxdb_post.append(data)
#    client = InfluxDBClient(host, port, username, password, database)
#    try:
#       client.write_points(influxdb_post)
#        e = 'to InfluxDB success'
#   except exceptions.InfluxDBClientError as e:
#       print(e)
#   return e


def annotation_times_mqtt():
    config = configparser.ConfigParser()
    config.read('ex_config.ini')
    mqtthost = config['mqtt']['mqtthost']
    mqttuser = config['mqtt']['mqttuser']
    mqttpass = config['mqtt']['mqttpass']
    mqtttopic = config['mqtt']['mqtttopic']
    client = paho.Client()
    client.username_pw_set(mqttuser, mqttpass)
    client.connect(mqtthost, 1883, 60)
    client.loop_start()
    message = 1
    (rc, mid) = client.publish(mqtttopic, str(message), qos=0)
    client.loop_stop()
    return str(mid)






port = os.getenv('PORT', '7500')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(port))




