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
python uiTest/login.py
```

 ### User Scenario

## Make Datasets

input command prompt like below 

```
python make_dataset.py
```

it will make AllergyRawMtrl\_{%y%m%d%H%M%S}.csv, haccp\_dataset\_{%y%m%d%H%M%S}csv, VegRawMtrl\_{%y%m%d%H%M%S}.csv

uplode_data.py will upload lastest csv file.

