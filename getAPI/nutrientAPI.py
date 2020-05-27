import urllib.request as ul
import json


#----------------- 한국식품안전관리인증원_HACCP 제품이미지 및 포장지표기정보 API -------------#


key = "5166a2888d344272a613" # 인증키
dataType = "json"  # xml 혹은 json
startIx = 0 # 정수: 요청 시작 위치
endIx = 1000  # 정수: 요청 종료 위치
condition="우유"

url = "http://openapi.foodsafetykorea.go.kr/api/{0}/I0750/{1}/{2}/{3}/DESC_KOR={4}".format(key, dataType, startIx, endIx, condition.encode("utf-8"))
# 데이터를 받을 url

request = ul.Request(url) # url 데이터 요청
response = ul.urlopen(request) # 요청받은 데이터 오픈

## ---------- json --------------- ##
json_str = response.read().decode("utf-8")
json_object = json.loads(json_str)

body = json_object['I0750']['row']  # row data만 추출

body