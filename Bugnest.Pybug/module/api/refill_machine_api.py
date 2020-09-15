#build-in modules
import requests
import json
from datetime import datetime
import urllib3
import unicodedata

#urs defined modules
from .helper import *
from .model import *

urllib3.disable_warnings()


# api đăng nhập
URL_LOGIN = 'https://betaapipartner.thegioididong.com/api/Login/LoginPartnerUser'
# api lấy thông tin nợ nhân viên (nạp tiền)
URL_GET_DEBT = 'https://betaapipartner.thegioididong.com/api/RefillMachine/GetDebtAmountByUserName'
# api cập nhật thông tin nợ nhân viên (nạp tiền)
URL_UPDATE_DEBT = 'https://betaapipartner.thegioididong.com/api/RefillMachine/UpdateDebtAmountByUserName'
# api lấy thông tin nợ của máy (rút tiền)
URL_CHECK_PERMISSION = 'https://betaapipartner.thegioididong.com/api/RefillMachine/CheckPermissionByUserName'
# api chuyển tiền từ máy sang thu ngân (rút tiền)
URL_CHANGE_BY_URS = 'https://betaapipartner.thegioididong.com/api/RefillMachine/ChangeByUserName'


RETRIES= 3
CLIENT_ERR_FLAG= 'app:err'

LOGIN_URS= None
LOGIN_PWD= None

TOKEN= None
LAST_LOGIN= datetime.now()
TOKEN_EXPERIED= ((datetime.now() - LAST_LOGIN).total_seconds() / 60) > 30

def login(username, password):
    global LAST_LOGIN, TOKEN, LOGIN_URS, LOGIN_PWD

    resp_data= LoginResponse(is_error= True, message= 'khong the ket noi den server', status= CLIENT_ERR_FLAG)
    req_data = {"userName":username,
                "password":password}

    resp = post(url= URL_LOGIN, json= req_data)
    if resp == None: 
        pass
    else:
        json_response = json.loads(resp.text)
        resp_data.is_error = json_response['IsError']
        resp_data.status = json_response['Status']
        resp_data.message = remove_sign(json_response['Message'])
        resp_data.key = json_response['Certificatekey']

        LOGIN_URS= username
        LOGIN_PWD= password

        TOKEN= json_response['Certificatekey']
        LAST_LOGIN= datetime.now()

    return resp_data

def get_debt(username, local_balance):
    if TOKEN == None: raise APIErorr('chua dang nhap')
    if TOKEN_EXPERIED: login(LOGIN_URS, LOGIN_PWD)

    resp_data= GetDebtResponse(is_error= True, message= 'khong the ket noi den server', status= CLIENT_ERR_FLAG)
    req_data = {"strAuthen":TOKEN,
                "strUserName":username,
                "decTotalMoneyMachine":local_balance}

    resp = post(url= URL_GET_DEBT, json= req_data)
    if resp == None: 
        pass
    else:
        json_response = json.loads(resp.json())
        debt_data = None
        if not json_response['IsError']:
            debt_data = GetDebtResponse.Data(
                json_response['Data']['UserName'],
                json_response['Data']['PaymentStatus'],
                json_response['Data']['TotalPayment'])

        resp_data.is_error = json_response['IsError']
        resp_data.status = json_response['Status']
        resp_data.message = remove_sign(json_response['Message'])
        resp_data.data = debt_data

    return resp_data

def update_debt(username, total_payment, local_balance):
    if TOKEN == None: raise APIErorr('chua dang nhap')
    if TOKEN_EXPERIED: login(LOGIN_URS, LOGIN_PWD)

    resp_data= GetDebtResponse(is_error= True, message= 'khong the ket noi den server', status= CLIENT_ERR_FLAG)
    req_data = {"strAuthen":TOKEN,
                "strUserName":username,
                "decTotalPayment":total_payment,
                "decTotalMoneyMachine": local_balance}

    resp = post(url= URL_UPDATE_DEBT, json= req_data)
    if resp == None: 
        pass
    else:
        try:
            json_response = resp.json()
            resp_data.is_error = json_response['IsError']
        except TypeError:
            json_response= json.loads(resp.json())
            resp_data.is_error = json_response['IsError']

        resp_data.status = json_response['Status']
        resp_data.message = remove_sign(json_response['Message'])

    return resp_data

def check_permission(username, otp, local_balance):
    if TOKEN == None: raise APIErorr('chua dang nhap')
    if TOKEN_EXPERIED: login(LOGIN_URS, LOGIN_PWD)

    resp_data= CheckPermissionResponse(is_error= True, message= 'khong the ket noi den server', status= CLIENT_ERR_FLAG)
    req_data = { "strAuthen":TOKEN,
                "strUserName":username,
                "strOTP": otp,
                "decTotalMoneyMachine": local_balance}

    resp = post(url= URL_CHECK_PERMISSION, json= req_data)
    if resp == None: 
        pass
    else:
        json_response = json.loads(resp.json())
        debt_data = None
        if not json_response['IsError']:
            debt_data = CheckPermissionResponse.Data()
            debt_data.username = json_response['Data']['UserName']
            debt_data.payment_status = json_response['Data']['PaymentStatus'],
            debt_data.total_payment = json_response['Data']['TotalPayment'],
            if debt_data.payment_status != 1:
                debt_data.otp = json_response['Data']['OTP']
                debt_data.otp_expire_date = datetime.strptime(json_response['Data']['OTPExpireDate'][:-6], '%d/%m/%Y %H:%M:%S.%f')

        resp_data.is_error = json_response['IsError']
        resp_data.status = json_response['Status']
        resp_data.message = remove_sign(json_response['Message'])
        resp_data.data = debt_data

    # fix da model
    if not resp_data.is_error:
        resp_data.data.payment_status = str(resp_data.data.payment_status[0])
        resp_data.data.total_payment = resp_data.data.total_payment[0]

    return resp_data

def change(username, total_payment,local_balance):
    if TOKEN == None: raise APIErorr('chua dang nhap')
    if TOKEN_EXPERIED: login(LOGIN_URS, LOGIN_PWD)

    resp_data= GetDebtResponse(is_error= True, message= 'khong the ket noi den server', status= CLIENT_ERR_FLAG)
    req_data = {"strAuthen":TOKEN,
                "strUserName":username,
                "decTotalPayment":total_payment,
                "decTotalMoneyMachine": local_balance}

    resp = post(url= URL_CHANGE_BY_URS, json= req_data)
    if resp == None: 
        pass
    else:
        json_response = json.loads(resp.json())
        resp_data.is_error = json_response['IsError']
        resp_data.status = json_response['Status']
        resp_data.message = remove_sign(json_response['Message'])

    return resp_data
