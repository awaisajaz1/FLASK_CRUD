import os
# import tempfile
import pytest
import json
# from app import my_app
#import requests
import json
# from credentials import credentials
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sys
import urllib.parse
#from kaykrooutils import jqsecurity, jqutils
import jwt


# def test_login(client):
#     do_login(client)

def do_login(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: test_login')
 
    email = 'admin@kaykroo.com'
    username = 'admin'
    password = 'alburaaq424'
    # password = "alburaaq424"
    password_bytes = password.encode()

    request_body = {
        'username': username,
        'password': password
    }
    response = client.post('/kaykroo/login',  json=request_body)
    j = json.loads(response.data)
    print("CLIENT: RECEIVED SERVER BODY DATA: ")
    print(j)
    server_status = j['status']
    username = j['username']
    # print(server_status)
    print("CLIENT: RECEIVED SERVER HEADER DATA: ")

    access_token=response.headers.get('X-Access-Token')

    public_key = jqsecurity.read_rsa_public_key_bytes_from_file_to_key('server-key.public')

    access_token_decoded = jwt.decode(access_token, public_key, algorithms=['RS256'])
    print('CLIENT: JWT  TOKEN: ', access_token_decoded)
    access_token_value = access_token_decoded['access_token']
    # print('client got this access token in the header from server response', access_token)

    assert server_status == 'successful-login'
 
 # TEST BAD USERNAME/PASSWORD

    email = 'admin@kaykroo.com'
    username = 'admin'
    password = 'alburaaq425'
    # password = "alburaaq424"
    password_bytes = password.encode()

    request_body = {
        'username': username,
        'password': password
    }
    response = client.post('/kaykroo/login',  json=request_body)
    j = json.loads(response.data)
    server_status = j['status']
    print(server_status)
    print("CLIENT: RECEIVED SERVER HEADER DATA: ")

    # access_token=response.headers.get('X-Access-Token')

    # public_key = jqsecurity.read_rsa_public_key_bytes_from_file_to_key('server-key.public')

    # access_token_decoded = jwt.decode(access_token, public_key, algorithms=['RS256'])
    # print('CLIENT: JWT  TOKEN: ', access_token_decoded)
    # access_token_value = access_token_decoded['access_token']
    # print('client got this access token in the header from server response', access_token)
    assert server_status == 'failed-login'

#######################################################################################################################################################
def test_add_user(client):
    do_add_user(client)
    # do_edit_user(client)

# def test_jq(client):
#     query = text(""" select username
#         from user
#         where
#         username = 'abdullaah-junaid'
#         """)   
#     db_engine = jqutils.get_db_engine('testkaykroo')         
#     with db_engine.connect() as conn:
#         result = conn.execute(query).fetchone()
#         print("the result of 2nd test function", result['username'])
    
#     assert True


def test_edit_user(client):
    do_edit_user(client)

def do_add_user(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_add_user')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST SAVE NAMES')
    username = 'abdullaah-junaid'
    email = 'junaid@kaykroo.com'
    first_names_en = 'abdullaah junaid'
    last_name_en = 'qureshi'
    phone_nr = '+971521123456'
    password = 'user1@123'
    
    request_body = {
        'username': username,
        'email': email,
        'first_names_en': first_names_en,
        'last_name_en': last_name_en,
        'phone_nr': phone_nr,
        'password': password
    }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.post('/kaykroo/user',  json=request_body, headers=header)
    j = json.loads(response.data)
    status = j['status']

    print(j)
# # LATER
 
#     query = text(""" select username
#         from testkaykroo.signup
#         where 
#         email= :email
#         and access_token is not null
#         """)   
#     db_engine = jqutils.create_db_engine('testkaykroo')         
#     with db_engine.connect() as conn:
#         result = conn.execute(query, email=email).fetchone()
#     reference_password_ciphered_bytes =  result['password'].encode()
#     key = jqsecurity.read_symmetric_key_from_file('test-password-protector.key')
#     reference_password_deciphered = jqsecurity.decrypt_bytes_symmetric_to_bytes(reference_password_ciphered_bytes, key)
#     print('db reference_password_deciphered', reference_password_deciphered)

# # TEST DATA PERSISTANCE
    print(response)
    assert status == 'successful'
    
    # print('in test: TEST SAVE NAMES')   
    # username = 'abdullaah-junaid'
    # first_names_en = 'junaid ibn ahmed'
    # last_name_en = 'al-qureshi'
    # phone_nr = '+971999999999'
    
    # request_body = {
    #     'username': username,
    #     'first_names_en': first_names_en,
    #     'last_name_en': last_name_en,
    #     'phone_nr': phone_nr
    # }

    # header = {
    #     'X-Access-Token': access_token,
    #     'X-User': user,    
    # }
    # response = client.put('/kaykroo/user',  json=request_body, headers=header)
    # j = json.loads(response.data)
    # status = j['status']

 


# TEST BAD TOKEN
    # access_token = "9GdJaJxa7O0B-mk0fxzYN22" 
    # header = {
    #     'X-Access-Token': access_token,
    #     'X-User': user,    
    # }
    # response = client.post('/kaykroo/user',  json=request_body, headers=header)
    # # j = json.loads(response.data)
    # print(response.status_code)
    # print(response)
    
    # # print(response)
    # # status = j['status']
    # # print(status)
    # # assert server_status == 'error'
    # assert response.status_code == 500

# TEST ADD USER END



def do_edit_user(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_edit_user')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST SAVE NAMES')
    username = 'abdullaah-junaid'
    first_names_en = 'junaid ibn ahmed'
    last_name_en = 'al-qureshi'
    phone_nr = '+971999999999'
    
    request_body = {
        'username': username,
        'first_names_en': first_names_en,
        'last_name_en': last_name_en,
        'phone_nr': phone_nr
    }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.put('/kaykroo/user',  json=request_body, headers=header)
    j = json.loads(response.data)
    status = j['status']

    print(status)
    print(response)
    assert status == 'successful'


def test_get_user(client):
    do_get_user(client)


def do_get_user(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_get_user')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST SAVE NAMES')
    username = 'abdullaah-junaid'
    username = 'admin'    
    
    request_body = {
        'username': username
    }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.get('/kaykroo/user',  json=request_body, headers=header)
    j = json.loads(response.data)
    status = j['status']
    print(j)
    print(status)
    print(response)
    
    assert status == 'successful'

 
 
 # DELETE USER


# def test_delete_user(client):
#     do_delete_user(client)


def do_delete_user(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_delete_user')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST DELETE USER')
    username = 'abdullaah-junaid'
  
    
    request_body = {
        'username': username
    }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.delete('/kaykroo/user',  json=request_body, headers=header)
    j = json.loads(response.data)
    status = j['status']
    print(j)
    print(status)
    print(response)
    
    assert status == 'successful'



def test_do_get_role(client):
    do_get_role(client)

def do_get_role(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_get_roles')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST GET ROLE')
    username = 'abdullaah-junaid'
  
    
    # request_body = {
    #     'username': username
    # }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.get('/kaykroo/role', headers=header)
    j = json.loads(response.data)
    status = j['status']
    print(j)
    print(status)
    print(response)
    
    assert status == 'successful'

# ASSIGN ROLE TO USER


def test_do_assign_role_to_user(client):
    do_assign_role_to_user(client)

def do_assign_role_to_user(client):
    # TEST SAVE EMAIL BEGIN
    print('in test: do_assign_role_to_user')
# TEST SAVE NAMES BEGIN
    access_token = "9GdJaJxa7O0B-mk0fxzYNw" 
    user = 'admin'  

    print('in test: TEST GET ROLE')
    username = 'abdullaah-junaid'
    role_name = 'admin'
  
    
    request_body = {
        'username': username,
        'role_name': role_name
    }

    header = {
        'X-Access-Token': access_token,
        'X-User': user,    
    }
    response = client.post('/kaykroo/user-role', json=request_body, headers=header)
    j = json.loads(response.data)
    status = j['status']
    print(j)
    print(status)
    print(response)
    
    assert status == 'successful'











# SOME HELP BELOW IN CASE IT IS NEEDED AS A REFERENCE   
#######################################################################################################################################################
# def test_signup(client):
#     # TEST SAVE EMAIL BEGIN
#     print('in test: test_signup_save_email')
 
#     email = 'jqkaykrootest.com'
#     password = 'password123'
#     password_bytes = password.encode()
#     request_body = {
#         'email': email,
#         'password': password
#     }
#     response = client.post('/kaykroo/v2/signup/email',  json=request_body)
#     j = json.loads(response.data)
#     # print(j)
#     print("CLIENT: RECEIVED SERVER HEADER DATA: ")

#     access_token=response.headers.get('X-Access-Token')

#     public_key = jqsecurity.read_rsa_public_key_bytes_from_file_to_key('server-key.public')

#     access_token_decoded = jwt.decode(access_token, public_key, algorithms=['RS256'])
#     print('CLIENT: JWT SIGNUP TOKEN: ', access_token_decoded)
#     access_token_value = access_token_decoded['access_token']
#     # print('client got this access token in the header from server response', access_token)
 
#     query = text(""" select password
#         from testkaykroo.signup
#         where 
#         email= :email
#         and access_token is not null
#         """)   
#     db_engine = jqutils.create_db_engine('testkaykroo')         
#     with db_engine.connect() as conn:
#         result = conn.execute(query, email=email).fetchone()
#     reference_password_ciphered_bytes =  result['password'].encode()
#     key = jqsecurity.read_symmetric_key_from_file('test-password-protector.key')
#     reference_password_deciphered = jqsecurity.decrypt_bytes_symmetric_to_bytes(reference_password_ciphered_bytes, key)
#     print('db reference_password_deciphered', reference_password_deciphered)
    
#     assert reference_password_deciphered==password_bytes

#     # TEST SAVE EMAIL END

# # TEST SAVE NAMES BEGIN
#     print('in test: TEST SAVE NAMES')
 
#     first_names = 'abdullaah junaid 1st name'
#     last_name = 'qureshi'
#     password_bytes = password.encode()
#     request_body = {
#         'first_names': first_names,
#         'last_name': last_name
#     }

#     header = {
#         'X-Access-Token': access_token_value,
#         'X-User-Email': email,    
#     }
#     response = client.post('/kaykroo/v2/signup/name-detail',  json=request_body, headers=header)
#     j = json.loads(response.data)
#     print(j)

 
#     # query = text(""" select password
#     #     from testkaykroo.signup
#     #     where 
#     #     email= :email
#     #     and access_token is not null
#     #     """)   
#     # db_engine = jqutils.create_db_engine('testkaykroo')         
#     # with db_engine.connect() as conn:
#     #     result = conn.execute(query, email=email).fetchone()
#     # reference_password_ciphered_bytes =  result['password'].encode()
#     # key = jqsecurity.read_symmetric_key_from_file('test-password-protector.key')
#     # reference_password_deciphered = jqsecurity.decrypt_bytes_symmetric_to_bytes(reference_password_ciphered_bytes, key)
#     # print('db reference_password_deciphered', reference_password_deciphered)
    
#     # assert reference_password_deciphered==password_bytes

#     # TEST SAVE NAMES END    
#     print('i asserted up there peeps')

#     # TEST BUSINESS DETAIL BEGIN
#     business_name = "JQ Business Name"
#         # print(email)
#     business_country = "AE"
#     business_website = "htttps://www.jq-business.com"
#     request_body = {
#         'business_name': business_name,
#         'business_country': business_country,
#         'business_website': business_website
#     }

#     header = {
#         'X-Access-Token': access_token_value,
#         'X-User-Email': email,    
#     }
#     response = client.post('/kaykroo/v2/signup/business-detail',  json=request_body, headers=header)
#     j = json.loads(response.data)
#     print(j)


    # TEST BUSINESS DETAIL END

    # A Business Account ID is created in the Account table
    # The Account’FLASK_CRUD Business Account Payment Provider is set to kaykroo
    # A kaykroo Payment Provider ID is created for the Business Account
    # An kaykroo Payment Provider Secret Key is created for the Account 
    # The API version is set to v2-2020-08-20 [LAUNCH DATE]

    # A Zero Balance is created for the Account
    # Two capabilities are added to the Account: Transfer and Card Payments
    # For  Business Verification; the country specification for the country chosen at the time of sign up is attached to the business verification table for this account


    # An Admin Policy file is created in the Policy table from the Admin Policy Template
    # A user is created in the User table
    # The policy file is attached to the user.

