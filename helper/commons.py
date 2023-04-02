import yaml
import requests
import json

stock_info = None

#설정 파일 정보 로딩
with open('/home/ec2-user/forif-stock-bot/helper/StockInfo.yaml', encoding='UTF-8') as f:
    stock_info = yaml.load(f, Loader=yaml.FullLoader)
    
    
#앱 키
def get_app_key(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_APP_KEY"
    elif dist == "v":
        key = "VIRTUAL_APP_KEY"
        
    return stock_info[key]


#앱시크릿
def get_app_secret(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_APP_SECRET"
    elif dist == "v":
        key = "VIRTUAL_APP_SECRET"
        
    return stock_info[key]


#계좌번호
def get_account_no(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_CANO"
    elif dist == "v":
        key = "VIRTUAL_CANO"
        
    return stock_info[key]


#계좌 정보(삼품코드)
def get_product_code(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_ACNT_PRDT_CD"
    elif dist == "v":
        key = "VIRTUAL_ACNT_PRDT_CD"
        
    return stock_info[key]


#URL주소
def get_url_base(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_URL"
    elif dist == "v":
        key = "VIRTUAL_URL"
        
    return stock_info[key]


def get_token_path(dist = "r"):
    global stock_info
    
    key = ""
    
    if dist == "r":
        key = "REAL_TOKEN_PATH"
    elif dist == "v":
        key = "VIRTUAL_TOKEN_PATH"
    
    return stock_info[key]

#토큰 값을 리퀘스트 해서 실제로 만들어서 파일에 저장하는 함수!! 첫번째 파라미터: "REAL" 실계좌, "VIRTUAL" 모의계좌
def make_new_token(dist = "r"):
    headers = {"content-type":"application/json"}
    body = {
        "grant_type":"client_credentials",
        "appkey":get_app_key(dist), 
        "appsecret":get_app_secret(dist)
        }

    PATH = "oauth2/tokenP"
    URL = f"{get_url_base(dist)}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    

    if res.status_code == 200:
        my_token = res.json()["access_token"]

        dataDict = dict()

        #해당 토큰을 파일로 저장해 둡니다!
        dataDict["authorization"] = my_token
        with open(get_token_path(dist), 'w') as outfile:
            json.dump(dataDict, outfile)   

        return my_token

    else:
        print('Get Authentification token fail!')  
        return "FAIL"


#파일에 저장된 토큰값을 읽는 함수.. 만약 파일이 없다면 MakeToken 함수를 호출한다!
def get_token(dist = "r"):
        
    dataDict = dict()

    try:
        with open(get_token_path(dist), 'r') as json_file:
            dataDict = json.load(json_file)


        return dataDict['authorization']

    except Exception as e:
        print("Exception by First")
        return make_new_token(dist)


        
    
    