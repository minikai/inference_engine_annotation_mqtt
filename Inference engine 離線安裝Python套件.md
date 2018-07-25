**Inference engine 安裝Python套件**
=============

Inference engine為在霧端設備上透過Docker運行的Python runtime程式，因此有時需要更新Python需要的相關套件。

**透過網際網路的方式更新Python 套件(以下以安裝xgboost套件為例)**
-------------
1. 進入Docker運行的container 執行pip install

    ```pip install xgboost```
    
    ![image](https://github.com/minikai/inference_engine_annotation_mqtt/blob/master/pip%20install%20xgboost.png?raw=true)
    
    
**在無網路環境下透過whl檔的方式更新Python 套件(以下以安裝xgboost套件為例)**
-------------
1. 將xgboost的套件whl檔放至在c:\inference_engine目錄下

    ![image](https://github.com/minikai/inference_engine_annotation_mqtt/blob/master/whl%E8%B7%AF%E5%BE%91.png?raw=true)

2. 進入到Docker運行的container中的 /inference_engine資料夾

   ```cd /inference_engine/```
 
3. 利用pip install 安裝xgboost的whl檔

   ```pip inference xgboost-0.72.1-py2.py3-none-manylinux1_x86_64.whl```
   
     ![image](https://github.com/minikai/inference_engine_annotation_mqtt/blob/master/pip%20install%20whl.png?raw=true)
