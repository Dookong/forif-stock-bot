import yaml
import requests
import json

info = None

#설정 파일 정보 로딩
with open('../helper/PersonalInfo.yaml', encoding='UTF-8') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)
    
    
#앱 키
def get_app_key(dist = "r"):
    global info
    
    key = ""
    
    if dist == "r":
        key = "REAL_APP_KEY"
    elif dist == "v":
        key = "VIRTUAL_APP_KEY"
        
    return info[key]


#앱시크릿
def get_app_secret(dist = "r"):
    global info
    
    key = ""
    
    if dist == "r":
        key = "REAL_APP_SECRET"
    elif dist == "v":
        key = "VIRTUAL_APP_SECRET"
        
    return info[key]


#계좌번호
def get_account_no(dist = "r"):
    global info
    
    key = ""
    
    if dist == "r":
        key = "REAL_CANO"
    elif dist == "v":
        key = "VIRTUAL_CANO"
        
    return info[key]


#계좌 정보(삼품코드)
def get_product_code(dist = "r"):
    global info
    
    key = ""
    
    if dist == "r":
        key = "REAL_ACNT_PRDT_CD"
    elif dist == "v":
        key = "VIRTUAL_ACNT_PRDT_CD"
        
    return info[key]


#URL주소
def get_url_base(dist = "r"):
    global info
    
    key = ""
    
    if dist == "r":
        key = "REAL_URL"
    elif dist == "v":
        key = "VIRTUAL_URL"
        
    return info[key]

def get_service_key():
    global info
    return info["SERVICE_KEY"]

def get_telegram_keys():
    global info
    return (info["CHAT_ID"], info["TELEGRAM_TOKEN"])

        
    
    