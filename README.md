# db_project
2020-1 Ajou univ. database course. 

알레르기 유무 및 채식 유형멸 맞춤 식품 검색 서비스 development with Python, PostgreSQL

## Requirements

Python 3.6, postgres

## Installatoin

1. Clone this repository
2. Install dependencies

```
pip3 install -r requirements.txt
```

## Upload Datasets

input command prompt like below 

```
cd src
python upload_data.py --user postgres --pwd 1234 --db projectDB --host localhost --port 5432
```

--user: user name
--pwd: sever password
--db: database name
--host: host address(default: localhost)
--port: port number

### Cuation

- All tables in that database are dropped.

## Use GUI

```
python main.py
```

 ### User Scenario
- initial window
<img width="336" alt="스크린샷 2020-06-20 오후 4 40 12" src="https://user-images.githubusercontent.com/58394729/85196803-aad61d00-b317-11ea-8b45-3ba25bc5937c.png">
- sign in window
<img width="335" alt="스크린샷 2020-06-20 오후 4 41 15" src="https://user-images.githubusercontent.com/58394729/85196834-de18ac00-b317-11ea-8835-ce797735b568.png">
- search & show result by personal account

  -  search with text or barcode scan 
     -  you can close barcode windows with **esc key.(not close window button.)**

  <img src="https://user-images.githubusercontent.com/42842339/85216126-0659e680-b3bc-11ea-8b14-784e96627eaf.PNG" alt="캡처" style="zoom: 50%;" />
-  alternative products in combobox 

<img width="1080" alt="스크린샷 2020-06-20 오후 4 53 15" src="https://user-images.githubusercontent.com/58394729/85196961-cdb50100-b318-11ea-89a4-a979418375c9.png">

<img width="1081" alt="스크린샷 2020-06-20 오후 4 53 24" src="https://user-images.githubusercontent.com/58394729/85196861-14562b80-b318-11ea-9297-cb8efa21b80b.png">



## Make Datasets

input command prompt like below 

```
cd src
python make_dataset.py
```

it will make AllergyRawMtrl\_{%y%m%d%H%M%S}.csv, haccp\_dataset\_{%y%m%d%H%M%S}csv, VegRawMtrl\_{%y%m%d%H%M%S}.csv

uplode_data.py will upload lastest csv file.

