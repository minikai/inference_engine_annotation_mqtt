# 程式功能
  
  (1) 	利用Docker在Windows環境中執行inference_engine.py預測程式，預測程式接收到設備端利用api送來的設備即時資料，讀取預測模型.pkl檔判斷設備目前的狀態是正常或異常並把判斷結果紀錄在model_predict_result.txt中，判斷正常時結果會記為[1]，判斷正常時結果會記為[-1]。
  
  (2)	如果API中的 "annotation_enable":0 時會進行grafana annotation標註錯誤的功能，判斷設備並目前的狀態是正常或異常並把判斷結果紀錄在model_predict_result.txt中，如果為"annotation_enable": 1時只會判斷設備並目前的狀態是正常或異常並把判斷結果紀錄在model_predict_result.txt中。
  
  (3)	"annotation_enable":0 時會進行grafana annotation標註錯誤的功能，功能為標註 [-1]的資料時間並在grafana上的儀表板上作呈現，會依據api 中tags的內容顯示測點編號及error code，在指定的"dashboardId": ,"panelId":。 
  
  (4)	如備標註為[-1]的資料為前後筆資料的時間為連續的話，則會在grafana annotation的儀表板上呈現為一個區塊，區塊的起始時間為第一筆資料的"time":，區塊的結束時間為最後一筆資料的"timeEnd":
  
  (5)	每發生一次異常狀態判斷為[-1]時，即會依據config.ini裡記錄的RabbitMQ(mqtt)的連線資訊送一筆資料進到指定的Queue中。

---------------------------------------

# 參考用API格式
  
## 正確的資料Json
  
{
"data": [4.721318, 2.724564, 13.606851, 5.768173, 17.639400, 7.930324, 3.847886, 10.201441, 5.847981, 0.002122, 0.000251, 0.001077, 0.000429, 0.001402, 0.000552, 0.000226, 0.000807, 0.000350, 0.016217, -0.000001, 0.021435, 0.018081, 0.001140, 0.003952, 0.000800, 0.002367, 0.008363, 0.001770, 0.006017, 170.863373, 4.249046, 54.803432, 8.312798, 77.792358, 14.838584, 4.643997, 28.894154, 9.419409, -10.623612, -0.482818, -0.349481, -0.062485, 0.041577, -0.253825, 0.005035, -0.226610, -0.153362] ,"dashboardId":13,"panelId":2,"time":1531293099000,"isRegion":true,"timeEnd":1531293199000,"tags":"point 1","url":"https://dashboard-demo-demo.iii-arfa.com/api/annotations","user":"dujakivuk@storiqax.com",
"password":"QWer123!","model_name":"model","annotation_enable":0
}
  
##  錯誤的資料Json
  
{
"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.008363, 0.001770, 0.006017, 170.863373, 4.249046, 54.803432, 8.312798, 0, 14.838584, 4.643997, 0, 9.419409, -10.623612, -0.482818, -0.349481, -0.062485, 0, 0, 0.005035, -0.226610, -0.153362] ,"dashboardId":13,"panelId":2,"time":1531293099000,"isRegion":true,"timeEnd":1531293199000,"tags":"point 1","url":"https://dashboard-demo-demo.iii-arfa.com/api/annotations","user":"dujakivuk@storiqax.com",
"password":"QWer123!","model_name":"model","annotation_enable":0
}


---------------------------------------
# API參數說明


  (1) Api 參數 user、password、url為要呈現的grafana的網址及登入帳密
  
  (2) Api 參數 "dashboardId"、"panelId"為grafana要呈現的anntation的dashboard及panel
  
  (3) Api參數 "time"、"timeEnd"為資料的時間區間(起始、結束)
  
  (4) Api參數 "tags" 為anntation要標註的tag名稱
  
---------------------------------------
# 程式執行步驟

  1.	在c:\inference_engine的資料夾內放入inference_engine_annotation_mqtt.py檔及config.ini
  
  2.	在c:\inference_engine的資料夾內建立models資料夾及results資料夾，在models放入model.pkl檔在windows cmd中輸入Docker run --name inference_python –it –p 2000:7500 -v C:\inference_engine:/inference_engine/ inference_python 
  
  3.	pip install sklearn flask requests numpy pandas paho-mqtt scipy
  
  4.	python /inference_engine/inference_engine_annotation_mqtt.py
  
  5.	利用postman打上面提供的json代在body裡，headers代”Content-Type”:” application/json”，url為127.0.0.1:2000/predict
