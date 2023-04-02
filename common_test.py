import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from helper import commons

print("REAL_APP_KEY:" , commons.get_app_key("r"))
print("REAL_APP_SECRET:" , commons.get_app_secret("r"))
print("REAL_CANO" , commons.get_account_no("r"))
print("REAL_ACNT_PRDT_CD" , commons.get_product_code("r"))
print("REAL_URL" , commons.get_url_base("r"))

print("----------------------------------------------------")

print("VIRTUAL_APP_KEY:" , commons.get_app_key("v"))
print("VIRTUAL_APP_SECRET:" , commons.get_app_secret("v"))
print("VIRTUAL_CANO" , commons.get_account_no("v"))
print("VIRTUAL_ACNT_PRDT_CD" , commons.get_product_code("v"))
print("VIRTUAL_URL" , commons.get_url_base("v"))
