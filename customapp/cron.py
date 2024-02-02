import frappe
from datetime import datetime,date,timedelta
import csv, requests, json, calendar, os,zipfile,io
# from frappe.utils.file_manager import upload
# from frappe.core.doctype.file.file import File
import io
from customapp.general_function import *

def getEmail(role_name):
    userlist = []
    users = frappe.get_all('User')
    for user in users:
        u = frappe.get_last_doc('User',filters={'name':user.name})
        
        rolelist = u.roles
        # print('namee: ',u.name)
        # print('u: ',u)
        # print('rolelist: ',u.roles)
        if rolelist:
            for r in rolelist:
                if r.role == role_name:
                    userlist.append(u.email)
                    break
    
    return userlist

#latest
# def checkError(f1,f2,f3,row,errors,error_list,balance):
#     # f1(data), f2(error type), f3(number/string, length), f4(),balance
#     # checkExist('Account','account_number',row_list['account_number'],row,error_list,errors)
#     field = f1['field']
#     val = f1['value']
#     error = {
#         'row':row,
#         'field':field,
#         'val':val
#     }

#     if f2 == 1: # check record existence and ..
#         doctype = f1['doctype']
#         if f3 == '':
#             try:
#                 obj = frappe.get_last_doc(doctype,filters={field:val})
#             except:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Data'
#                 error_list.append(error)
#                 # print('error: ',error_list)
#         else:
#             field2 = f3['field2']
#             val2 = f3['val2']
#             objs = frappe.get_all(doctype,filters={field2:val2})
#             filter_count = 0
#             for o in objs:
#                 if val in o.name:
#                     filter_count+=1

#             if filter_count < 1:
#                 errors['error'] = True
#                 error['desc'] = doctype + ' Not Exist'
#                 error_list.append(error)
#                 # print(error_list)

#     elif f2 == 2: # check format
#         if f3 == 'string':  # only string
#             if not val.isdigit():
#                 return True
#             else:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
        
#         elif f3 == 'number': # only number
#             try: 
#                 val_int = int(val)
#                 return True
#             except:
#                 # print('type: ',type(val))
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
#             # if f4 != '': # year
#             #     year = datetime.now().year
#             #     if int(val) != year:
#             #         error['desc'] 
#             #         error_list.append(error)
#         elif f3 == 'float':
#             # if not isinstance(val, float):
#             try:
#                 float(val)
#                 if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
#                     # print(val)
#                     if val <= 0.0:
#                         errors['error'] = True
#                         error['desc'] = 'Invalid Value'
#                         error_list.append(error)
#                         return False
#                     return True
#                 return True
#             except:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
#             # else:
#             #     return True


#     elif f2 == 3:   # check if follow format eg, length
#         if f3 != '':
#             valstr = str(val)
#             length = len(valstr)
#             if length != f3:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Length'
#                 error_list.append(error)
#                 # print(error_list)
#             else:
#                 if field == 'current month':
#                     month = str(val)[0:2]
#                     year = str(val)[2:]
#                     if int(month) > 12 or int(month) < 0:
#                         errors['error'] = True
#                         error['desc'] = 'Invalid Month Value'
#                         error_list.append(error)
#                         # print(error_list)
#                     if int(year) < 0:
#                         errors['error'] = True
#                         error['desc'] = 'Invalid Year Value'
#                         error_list.append(error)
#                         # print(error_list)
    
#     elif f2 == 4: # check exact value
#         # if f3 == 'MYR':
#         #     if val != 'MYR':
#         #         errors['error'] = True
#         #         error['desc'] = 'Invalid Currency'
#         #         error_list.append(error)
#         if val != f3:
#             errors['error'] = True
#             if field == 'currency':
#                 error['desc'] = 'Invalid Currency'
#             elif field == 'year':
#                 error['desc'] = 'Invalid Year'
#             error_list.append(error)
#             # print(error_list)

#     elif f2 == 5: # date for user remark
#         current_date = datetime.now().date()
#         current_date = current_date.strftime('%y%m%d')
        
#         user_date = val[:6]
#         # if current_date != user_date:
#         #     print('user_date: ',user_date)
#         #     print('ccurent_date: ',current_date)
#         #     errors['error'] = True
#         #     error['desc'] = 'Wrong Date'
#         #     error_list.append(error)
#             # print(error_list)
#         user_year = int(user_date[:2])
#         user_month = int(user_date[2:4])
#         user_day = int(user_date[4:6])
#         if user_month < 0 or user_month > 12:
#             errors['error'] = True
#             error['desc'] = 'Invalid Date'
#             error_list.append(error)
#         else:
#             first_day, lastday = calendar.monthrange(user_year,user_month)
#             if user_day < 0 or user_day > lastday:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Date'
#                 error_list.append(error)

#         # print('year: ',str(int(user_year)),' '+str(int(user_month))+' '+str(int(user_day)))

#         user_time = val[-4:]
#         hour = int(user_time[:2])
#         minute = int(user_time[2:])
#         if hour > 23 or hour < 0 or minute > 59 or minute < 0:
#             errors['error'] = True
#             error['desc'] = 'Invalid Time'
#             error_list.append(error)
#             # print(error_list)

#     elif f2 == 6: # compare to current date
#         current_date = datetime.now().date()
#         current_date = current_date.strftime('%Y-%m-%d')
#         if current_date != val:
#             errors['error'] = True
#             error['desc'] = 'Wrong Date'
#             error_list.append(error)
#             # print(error_list)

#     elif f2 == 7: # check current_month length
#         val_str = str(val)
#         length = len(val_str)

#         month = 0
#         if length == 3:
#             month = val_str[:1]
#         elif length == 4:
#             month = val_str[:2]
#         else:
#             errors['error'] = True
#             error['desc'] = 'Invalid Length'
#             error_list.append(error)
#             # print(error_list)

#         if int(month) <= 0 or int(month) > 12:
#             errors['error'] = True
#             error['desc'] = 'Invalid Month'
#             error_list.append(error)
#             # print(error_list)

#         year = val_str[-2:]
#         if int(year) <= 0:
#             errors['error'] = True
#             error['desc'] = 'Invalid Year'
#             error_list.append(error)
#             # print(error_list)

#     if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
#         # if balance['counter'] == 1:
#         #     balance['val'] = abs(val)
#         # elif balance['counter'] == 2:
#         if balance['counter'] == 2:
#             # print('val1: ', balance['val'],' val2: ',val)
#             if balance['val'] != val:
#                 errors['error'] = True
#                 error['row'] = row
#                 error['val'] = balance['val']
#                 if field == 'debit_in_account_currency':
#                     error['desc'] = 'Not Balanced With Credit Row '+str(row-1)
#                 elif field == 'credit_in_account_currency':
#                     error['desc'] = 'Not Balanced With Debit Row '+str(row-1)
#                 print('error1: ',error,' val: ',val,' another: ',balance['val'])
#                 error_list.append(error)

#         # balance = val
#         # print('balance: ',balance,' val: ',val)
#     #     return balance
#     # elif field == 'credit_in_account_currency':
#     #     if balance != val:
#     #         # print('error row: ',error['row'])
#     #         errors['error'] = True
#     #         error['row'] = row-1
#     #         error['val'] = balance
#     #         error['desc'] = 'Not Balanced With Credit Row '+str(row)
#     #         error_list.append(error)
#     #         err_credit = {'row':row,'field':field,'val':val,'desc':'Not Balanced With Debit Row '+str(row-1)}
#     #         # error['row'] = error['row']-1
#     #         # error['val'] = val
#     #         # error['desc'] = 'Credit Is Not Balanced With Debit Row '+str(row)
#     #         error_list.append(err_credit)
#             # print(error_list)


# def checkError(f1,f2,f3,row,errors,error_list,balance):
#     # f1(data), f2(error type), f3(number/string, length), f4(),balance
#     # checkExist('Account','account_number',row_list['account_number'],row,error_list,errors)
#     field = f1['field']
#     val = f1['value']
#     error = {
#         'row':row,
#         'field':field,
#         'val':val
#     }

#     if f2 == 1: # check record existence and ..
#         doctype = f1['doctype']
#         if f3 == '':
#             try:
#                 obj = frappe.get_last_doc(doctype,filters={field:val})
#             except:
#                 errors['error'] = True
#                 error['desc'] = 'Missing Data'
#                 error_list.append(error)
#                 # print('error: ',error_list)
#         else:
#             field2 = f3['field2']
#             val2 = f3['val2']
#             objs = frappe.get_all(doctype,filters={field2:val2})
#             filter_count = 0
#             for o in objs:
#                 if val in o.name:
#                     filter_count+=1

#             if filter_count < 1:
#                 errors['error'] = True
#                 error['desc'] = doctype + ' Not Exist'
#                 error_list.append(error)
#                 # print(error_list)

#     elif f2 == 2: # check format
#         if f3 == 'string':  # only string
#             if not val.isdigit():
#                 return True
#             else:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
        
#         elif f3 == 'number': # only number
#             try: 
#                 val_int = int(val)
#                 return True
#             except:
#                 # print('type: ',type(val))
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
#             # if f4 != '': # year
#             #     year = datetime.now().year
#             #     if int(val) != year:
#             #         error['desc'] 
#             #         error_list.append(error)
#         elif f3 == 'float':
#             # if not isinstance(val, float):
#             try:
#                 float(val)
#                 if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
#                     print(val)
#                     if val <= 0.0:
#                         errors['error'] = True
#                         error['desc'] = 'Invalid Value'
#                         error_list.append(error)
#                         return False
#                     return True
#                 return True
#             except:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Format'
#                 error_list.append(error)
#                 return False
#                 # print(error_list)
#             # else:
#             #     return True


#     elif f2 == 3:   # check if follow format eg, length
#         if f3 != '':
#             valstr = str(val)
#             length = len(valstr)
#             if length != f3:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Length'
#                 error_list.append(error)
#                 # print(error_list)
    
#     elif f2 == 4: # check exact value
#         # if f3 == 'MYR':
#         #     if val != 'MYR':
#         #         errors['error'] = True
#         #         error['desc'] = 'Invalid Currency'
#         #         error_list.append(error)
#         if val != f3:
#             errors['error'] = True
#             if field == 'currency':
#                 error['desc'] = 'Invalid Currency'
#             elif field == 'year':
#                 error['desc'] = 'Invalid Year'
#             error_list.append(error)
#             # print(error_list)

#     elif f2 == 5: # date for user remark
#         current_date = datetime.now().date()
#         current_date = current_date.strftime('%y%m%d')
        
#         user_date = val[:6]
#         # if current_date != user_date:
#         #     print('user_date: ',user_date)
#         #     print('ccurent_date: ',current_date)
#         #     errors['error'] = True
#         #     error['desc'] = 'Wrong Date'
#         #     error_list.append(error)
#             # print(error_list)
#         user_year = int(user_date[:2])
#         user_month = int(user_date[2:4])
#         user_day = int(user_date[4:6])
#         if user_month < 0 or user_month > 12:
#             errors['error'] = True
#             error['desc'] = 'Invalid Date'
#             error_list.append(error)
#         else:
#             first_day, lastday = calendar.monthrange(user_year,user_month)
#             if user_day < 0 or user_day > lastday:
#                 errors['error'] = True
#                 error['desc'] = 'Invalid Date'
#                 error_list.append(error)

#         # print('year: ',str(int(user_year)),' '+str(int(user_month))+' '+str(int(user_day)))

#         user_time = val[-4:]
#         hour = int(user_time[:2])
#         minute = int(user_time[2:])
#         if hour > 23 or hour < 0 or minute > 59 or minute < 0:
#             errors['error'] = True
#             error['desc'] = 'Invalid Time'
#             error_list.append(error)
#             # print(error_list)

#     elif f2 == 6:
#         current_date = datetime.now().date()
#         current_date = current_date.strftime('%Y-%m-%d')
#         if current_date != val:
#             errors['error'] = True
#             error['desc'] = 'Wrong Date'
#             error_list.append(error)
#             # print(error_list)


#     if field == 'debit_in_account_currency':
#         balance = val
#         # print('balance: ',balance,' val: ',val)
#         return balance
#     elif field == 'credit_in_account_currency':
#         if balance != val:
#             # print('error row: ',error['row'])
#             errors['error'] = True
#             error['row'] = row-1
#             error['val'] = balance
#             error['desc'] = 'Not Balanced With Credit Row '+str(row)
#             error_list.append(error)
#             err_credit = {'row':row,'field':field,'val':val,'desc':'Not Balanced With Debit Row '+str(row-1)}
#             # error['row'] = error['row']-1
#             # error['val'] = val
#             # error['desc'] = 'Credit Is Not Balanced With Debit Row '+str(row)
#             error_list.append(err_credit)
#             # print(error_list)

# def checkEmpty(f1,row,errors,error_list):
#     field = f1['field']
#     val = f1['value']
#     error = {
#         'row':row,
#         'field':field,
#         'val':val
#     }

#     if val == '':
#         errors['error'] = True
#         error['desc'] = 'Missing Value'
#         error_list.append(error)

# def checkDominant(f1,errors,error_list):
#     val_list = []
#     for o in f1:
#         if not len(val_list):
#             val = {'val':o['val'],'count':1}
#             val_list.append(val)
#         else:
#             exist = False
#             for v in val_list:
#                 if v['val'] == o['val']:
#                     v['count']+=1
#                     exist = True
#             if not exist:
#                 val = {'val':o['val'],'count':1}
#                 val_list.append(val)

#     if len(val_list) > 1:
#         dominant = 0
#         dominant_val = ''
#         for v in val_list:
#             if dominant == 0:
#                 dominant = v['count']
#                 dominant_val = v['val']
#             else:
#                 if v['count'] > dominant:
#                     dominant = v['count']
#                     dominant_val = v['val']
        
#         for o in f1:
#             if dominant_val != o['val']:
#                 errors['error'] = True
#                 error = {
#                         'row':o['row'],
#                         'field':o['field'],
#                         'val':o['val'],
#                         'desc':'Wrong Data'
#                     }
#                 # if '_' in o['field']:
#                 #     split = o['field'].split('_')
#                 #     if len(split) > 1:
#                 #         field = ''
#                 #         for i in range(len(split)):
#                 #             if field == '':
#                 #                 field = split[i]
#                 #             else:
#                 #                 field += ' '+split[i]
#                 #     error['desc'] = 'Wrong '+field
#                 # else:
#                 #     error['desc'] = 'Wrong '+o['field']

#                 error_list.append(error)

# latest
# def getError(row_list,row,error_list,errors,balance):
#     year = row_list['year']
#     account_number = row_list['account_number']
#     cost_center_number = row_list['cost_center_number']
#     currency = row_list['currency']
#     # print('debit credit type: ',type(row_list['debit']))
#     # print('debit credit: ',row_list['debit'])
#     # print('year: ',year)

#     amt_type = ''
#     try:
#         debit_credit = row_list['debit']
#         amt_type = 'debit'
#     except:
#         debit_credit = row_list['credit']
#         amt_type = 'credit'
#     remark = row_list['remark']
#     posting_date = row_list['posting_date']
#     group = row_list['group']

    
#     objYear = {'field':'year','value':year}
#     objAccount = {'field':'account_number','value':account_number,'doctype':'Account'}
#     objCost = {'field':'cost_center_number','value':cost_center_number,'doctype':'Cost Center'}
#     objCurrency = {'field':'currency','value':currency}
#     objPostingDate = {'field':'posting_date', 'value':posting_date}
#     objGroup = {'field':'group','value':group}
#     # objRevenueAccount = {'field':'revenue_account','value':revenue_account,'doctype':'Account'}
#     objUserRemark = {'field':'user_remark','value':remark}
    
#     # year
#     result = True
#     checkEmpty(objYear,row,errors,error_list)
#     result = checkError(objYear,2,'number',row,errors,error_list,'')  # check number type
#     if result:
#         current_year = datetime.now().date().year
#         checkError(objYear,4,str(current_year),row,errors,error_list,'')  # check current year
#     # account
#     checkEmpty(objAccount,row,errors,error_list)
#     checkError(objAccount,2,'number',row,errors,error_list,'')  # check number type
#     checkError(objAccount,1,'',row,errors,error_list,'')    # check exist
#     # # cost center
#     checkEmpty(objCost,row,errors,error_list)
#     checkError(objCost,1,'',row,errors,error_list,'') # check exist
#     # #currency
#     # checkError(objCurrency,2,'string',row,errors,error_list,'') # check string type
#     checkEmpty(objCurrency,row,errors,error_list)
#     checkError(objCurrency,4,'MYR',row,errors,error_list,'') # check value MYR
#     # # debit
#     if amt_type == 'debit':
#         f1 = {'field':'debit_in_account_currency','value':float(debit_credit)}
#         checkError(f1,2,'float',row,errors,error_list,'') # check float type
#         checkEmpty(f1,row,errors,error_list)
#         # balance = checkError(f1,'','',row,errors,error_list,'') # get value
#         checkError(f1,'','',row,errors,error_list,balance) # get value
#     # credit
#     elif amt_type == 'credit':
#         f1 = {'field':'credit_in_account_currency','value':abs(float(debit_credit))}
#         checkError(f1,2,'float',row,errors,error_list,'') # check float type
#         checkEmpty(f1,row,errors,error_list)
#         checkError(f1,'','',row,errors,error_list,balance)  # check balance
    
#     # # user remark
#     # checkEmpty(objUserRemark,row,errors,error_list)
#     # split = user_remark.split(' / ')
#     # print('------------user remark: ',user_remark)
#     # bank_account = split[0]
#     # user_date = split[1]
#     # objURaccount = {'field':'account_name','value':bank_account,'doctype':'Account'}
#     # checkEmpty(objURaccount,row,errors,error_list)
#     # objParentAccount = {'field2':'parent_account','val2':'Bank - I'}
#     # checkError(objURaccount,1,objParentAccount,row,errors,error_list,'') # check bank account exist
#     # objURdate = {'field':'user_remark','value':user_date}
#     # checkError(objURdate,5,'',row,errors,error_list,'')
#     # # posting date
#     # checkError(objPostingDate,6,'',row,errors,error_list,'')

#     return balance  


# def getError(row_list,row,error_list,errors,balance):
#     year = row_list['year']
#     account_number = row_list['account_number']
#     cost_center_number = row_list['cost_center_number']
#     currency = row_list['currency']
#     amt_type = ''
#     try:
#         debit = row_list['debit']
#         amt_type = 'debit'
#     except:
#         credit = row_list['credit']
#         amt_type = 'credit'
#     user_remark = row_list['remark']
#     posting_date = row_list['posting_date']
#     group = row_list['group']

    
#     objYear = {'field':'year','value':year}
#     objAccount = {'field':'account_number','value':account_number,'doctype':'Account'}
#     objCost = {'field':'cost_center_number','value':cost_center_number,'doctype':'Cost Center'}
#     objCurrency = {'field':'currency','value':currency}
#     objPostingDate = {'field':'posting_date', 'value':posting_date}
#     objGroup = {'field':'group','value':group}
    
#     # year
#     result = True
#     checkEmpty(objYear,row,errors,error_list)
#     result = checkError(objYear,2,'number',row,errors,error_list,'')  # check number type
#     # if result:
#     #     current_year = datetime.now().date().year
#     #     checkError(objYear,4,str(current_year),row,errors,error_list,'')  # check current year
#     # account
#     checkEmpty(objAccount,row,errors,error_list)
#     checkError(objAccount,2,'number',row,errors,error_list,'')  # check number type
#     checkError(objAccount,1,'',row,errors,error_list,'')    # check exist
#     # # cost center
#     checkEmpty(objCost,row,errors,error_list)
#     checkError(objCost,1,'',row,errors,error_list,'') # check exist
#     # #currency
#     # checkError(objCurrency,2,'string',row,errors,error_list,'') # check string type
#     checkEmpty(objCurrency,row,errors,error_list)
#     checkError(objCurrency,4,'MYR',row,errors,error_list,'') # check value MYR
#     # # debit
#     if amt_type == 'debit':
#         f1 = {'field':'debit_in_account_currency','value':float(debit)}
#         checkError(f1,2,'float',row,errors,error_list,'') # check float type
#         checkEmpty(f1,row,errors,error_list)
#         balance = checkError(f1,'','',row,errors,error_list,'') # get value
#     # credit
#     elif amt_type == 'credit':
#         f1 = {'field':'credit_in_account_currency','value':abs(float(credit))}
#         checkError(f1,2,'float',row,errors,error_list,'') # check float type
#         checkEmpty(f1,row,errors,error_list)
#         checkError(f1,'','',row,errors,error_list,balance)  # check balance

#     # # user remark
#     # split = user_remark.split(' / ')
#     # bank_account = split[0]
#     # user_date = split[1]
#     # objURaccount = {'field':'account_name','value':bank_account,'doctype':'Account'}
#     # checkEmpty(objURaccount,row,errors,error_list)
#     # objParentAccount = {'field2':'parent_account','val2':'Bank - I'}
#     # checkError(objURaccount,1,objParentAccount,row,errors,error_list,'') # check bank account exist
#     # objURdate = {'field':'user_remark','value':user_date}
#     # checkError(objURdate,5,'',row,errors,error_list,'')
#     # # posting date
#     # checkError(objPostingDate,6,'',row,errors,error_list,'')

#     return balance  

def getDate(crdate):
    # if scheduler:
    # today = datetime.now().date()
    # today = today - timedelta(days=1)
    today = crdate['start_date']
    today = today.strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    start_date = today + timedelta(hours=0,minutes=0,seconds=0,milliseconds=0)
    start_date = start_date.isoformat()+"Z"
    end_date = today + timedelta(hours=23,minutes=59,seconds=59)
    end_date = end_date.isoformat()+"Z"
    year = today.year
    return start_date, end_date, year

    # else:
    #     start_date = crdate['start_date']
    #     end_date = crdate['end_date']
    #     year = start_date.year
    #     times = time(0,0,0)
    #     start_date = datetime.combine(start_date,times)
    #     end_date = datetime.combine(end_date,times)
    #     print('------type: ',type(start_date))
    #     start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
    #     start_date = start_date.isoformat()+"Z"
    #     print('++++++++++++++STARTDATE')
    #     print(start_date)
    #     end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
    #     end_date = end_date.isoformat()+"Z"

    #     return start_date, end_date, year


def getCR(start_end_year,existcr):
    start_date = start_end_year['start_date']
    end_date = start_end_year['end_date']
    year = start_end_year['year']
    reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextMthEndJob'})
	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
    reqUrl = reportcr.url +reportcr.api_key
    print('reqURL: ',reqUrl)

    payload = json.dumps({
    # "startDate": '2023-01-01T00:00:00Z',
    # "endDate": '2023-01-01T23:059:59Z',
    "startDate": start_date,
    "endDate": end_date,
    "name": "string",
    "year": year
    }, default=str)

    print('payload: ',payload)

    headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json" 
    }

    response = requests.request("POST", reqUrl, data=payload, headers=headersList)

    headers = response.headers
    # print(headers)
    msg = headers.get('return-message')
    textt = response.content.decode('utf-8')
    cr = csv.reader(textt.splitlines(), delimiter=',')
    cr = list(cr)
    print('===========CR==============')
    print(cr)
    # return True,cr
    if 'filename=string.csv.tmp' in msg:
        existcr['exist'] = False
        return False,''
        # raise Exception('The file you are trying to get is not in CSV format. Please try again later.')
    else:
        textt = response.content.decode('utf-8')
        cr = csv.reader(textt.splitlines(), delimiter=',')
        cr = list(cr)
        # print('========cr=========:',cr)
        return True,cr  

def checkReadyCR(start_date,end_date):

    # today = datetime.now()
    # today = today.strftime('%Y-%m-%d')
    # today = datetime.strptime(today, '%Y-%m-%d')
    # start_date = today + timedelta(hours=0,minutes=0,seconds=0,milliseconds=0)
    # start_date = start_date.isoformat()+"Z"
    # end_date = today + timedelta(hours=23,minutes=59,seconds=59)
    # end_date = end_date.isoformat()+"Z"
    # year = today.year
    # scheduler = True
    # dates_list = []
    start_end_year = {}

    date_dic = {'start_date':start_date,'end_date':end_date}
    # startdate,enddate,year = getDate(scheduler,date_dic)
    startdate,enddate,year = getDate(date_dic)
    start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}

    existcr = {}
    # cr_able = []
    
    ready,cr = getCR(start_end_year,existcr)
    # if len(cr) == 0:
    #     print('KOSONGSSS')
    # else:
    #     print('TAK KOSONGSSS')
    #     print(cr)
    # print('CR IN CHECKREADY: ',cr)
    cr_start = {'cr':cr,'date':start_end_year['start_date']}
    # cr_able.append(cr_start)
    # print('CR-DATE')
    # print(cr_date)
    if ready:
        return True,cr_start,''
    else:
        return False,'',''

# latest
# def handleError(cr):
#     # print('CR:')
#     # print(cr)
#     error_list = []
#     counter = 1
#     row_count = 0
#     errors = {}
#     posting_date_list = []
#     group_list = []
#     # rows = cr['cr']
#     balance_counter = 1
#     balance = {'val':0,'counter':balance_counter}
#     print('######cr: ',cr)
#     for row in cr:
#         # debit
#         # try:
#         #     row['debit']
#         #     counter = 1
#         # except:
#         #     counter = 2
#         print('---: ',row)
#         # print(row)

#         row_count += 1
#         posting_date = row['posting_date']
#         group = row['group']

#         posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
#         posting_date_list.append(posting_dates)
#         groups = {'row':row_count,'field':'group','val':group}
#         group_list.append(groups)
            
#         # if counter == 1:
#         balance['counter'] = balance_counter
#         getError(row,row_count,error_list,errors,balance)

#         if balance_counter == 1:
#             try:
#                 balance['val'] = row['debit']
#             except:
#                 balance['val'] = row['credit']
#             balance_counter = 2

#         elif balance_counter == 2:
#             # balance['counter'] = balance_counter
#             getError(row,row_count,error_list,errors,balance)
#             balance_counter = 1
            


#     # check posting date dominant error
#     # checkDominant(posting_date_list,errors,error_list)
#     # check group dominant error
#     checkDominant(group_list,errors,error_list)
    
#     if not len(errors):
#         # print('no error')
#         # print('error_list: ',error_list)
#         return False,error_list
#     else:
#         # print('errors: ',errors)
#         print('errors')
#         for p in error_list:
#             print(p)
#         return True,error_list


# def handleError(cr):
#     # print('CR:')
#     # print(cr)
#     error_list = []
#     counter = 1
#     row_count = 0
#     errors = {}
#     posting_date_list = []
#     group_list = []
#     # rows = cr['cr']
#     balance_counter = 1
#     balance = {'val':0,'counter':balance_counter}
#     print('######cr: ',cr)
#     for row in cr:
#         # debit
#         # try:
#         #     row['debit']
#         #     counter = 1
#         # except:
#         #     counter = 2
#         print('---: ',row)
#         # print(row)

#         row_count += 1
#         posting_date = row['posting_date']
#         group = row['group']

#         posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
#         posting_date_list.append(posting_dates)
#         groups = {'row':row_count,'field':'group','val':group}
#         group_list.append(groups)
            
#         # if counter == 1:
#         balance['counter'] = balance_counter
#         getError(row,row_count,error_list,errors,balance)

#         if balance_counter == 1:
#             try:
#                 balance['val'] = row['debit']
#             except:
#                 balance['val'] = row['credit']
#             balance_counter = 2

#         elif balance_counter == 2:
#             # balance['counter'] = balance_counter
#             getError(row,row_count,error_list,errors,balance)
#             balance_counter = 1
            


#     # check posting date dominant error
#     # checkDominant(posting_date_list,errors,error_list)
#     # check group dominant error
#     checkDominant(group_list,errors,error_list)
    
#     if not len(errors):
#         # print('no error')
#         # print('error_list: ',error_list)
#         return False,error_list
#     else:
#         # print('errors: ',errors)
#         print('errors')
#         for p in error_list:
#             print(p)
#         return True,error_list


# def handleError(cr):
#     print('CR in handle:')
#     print(cr)
#     balance = 0
#     error_list = []
#     counter = 1
#     row_count = 0
#     errors = {}
#     posting_date_list = []
#     group_list = []
#     # rows = cr['cr']
#     for row in cr:
#         # debit
#         row_count+=1
#         if counter == 1:
#             counter+=1

#             # year = row[1]
#             # account_number = row[2]
#             # cost_center_number = row[3]
#             # currency = row[12]
#             # debit = row[15]
#             # user_remark = row[23]
#             # print('#####################')
#             # print(row)
#             posting_date = row[30]
#             group = row[31]

#             row_list = {
#                 'year':row[1],
#                 'account_number':row[2],
#                 'cost_center_number':row[3],
#                 'currency':row[12],
#                 'debit':row[15],
#                 'user_remark':row[23],
#                 'posting_date':row[30],
#                 'group':row[31]
#             }
#             # other = {'row':row_count,'posting_date':posting_date,'group':group}
#             # others.append(other)
#             posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
#             posting_date_list.append(posting_dates)
#             groups = {'row':row_count,'field':'group','val':group}
#             group_list.append(groups)
#             balance = getError(row_list,row_count,error_list,errors,balance)

#             # checkExist('Account','account_number',account_number,row_count,error_list,errors)
#             # checkExist('Cost Center','cost_center_number',cost_center_number,row_count,error_list,errors)
#             # debit_acc = frappe.get_last_doc("Account", filters={"account_number":account_number})
#             # cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":cost_center_number})

#         # credit
#         elif counter == 2:
#             counter = 1
#             # year = row[1]
#             # account_number = row[2]
#             # cost_center_number = row[3]
#             # currency = row[12]
#             # credit = row[15]
#             # user_remark = row[23]
#             posting_date = row[30]
#             group = row[31]

            
#             row_list = {
#                 'year':row[1],
#                 'account_number':row[2],
#                 'cost_center_number':row[3],
#                 'currency':row[12],
#                 'credit':row[15],
#                 'user_remark':row[23],
#                 'posting_date':row[30],
#                 'group':row[31]
#             }
#             # other = {'row':row_count,'posting_date':posting_date,'group':group}
#             # others.append(other)
#             posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
#             posting_date_list.append(posting_dates)
#             groups = {'row':row_count,'field':'group','val':group}
#             group_list.append(groups)
#             getError(row_list,row_count,error_list,errors,balance)


#     # check posting date dominant error
#     checkDominant(posting_date_list,errors,error_list)
#     # check group dominant error
#     checkDominant(group_list,errors,error_list)
    
#     if not len(errors):
#         print('no error')
#         print('error_list: ',error_list)
#         return False,error_list
#     else:
#         print('errors: ',errors)
#         for p in error_list:
#             print(p)
#         return True,error_list

def createCSV(cr,errordate):
    path = 'collection_report'
    pathtofile = path+'/Error_Log_'+ str(errordate)
    filename = 'Error_Log_' + str(errordate)

    if os.path.exists(path):
        with open(pathtofile,'w') as file:
            writer = csv.writer(file)
            # for row in cr:
            #     # row_content = ''
            #     # print('rorr: ',row)
            #     # for r in row:
            #     row_content = ','.join(row)
            #     # print('row content: ',row_content)
            #     writer.writerow(row_content)
            row1 = ['ahmad','1','2']
            row2 = ['abu','3','4']
            rows = [row1,row2]
            # for row in rows:
            #     for r in row:

            writer.writerows(rows)
            # myss = ''
            # myss2 = []
            # for row in cr:
            #     mys = ''
            #     for r in row:
            #         mys = ','.join(str(r))
            #         print('mys: ',mys)
            #         myss2.append(mys)
            #     myss = myss.join(mys)
            #     print('myss: ',myss)
            # writer.writerows(myss)
            print('Successfully created CSV file')
    # else:
    #     os.makedirs(path)
    #     with open(pathtofile,'w') as file:
    #         writer = csv.writer(file)
    #         for row in cr:
    #             writer.writerow(row)
    #         # writer.writerows(cr)
    #         print('Successfully created CSV file')
    
    with open(pathtofile,'r') as file:
        filedata = csv.reader(file)
        print('filedatasss: ',filedata)
        for r in filedata:
            print('row: ',r)
        # file_url = upload(filename,file.read(),)
    return pathtofile, filename, filedata,cr

def createErrorLog(file,much,error_list,errordate):
    errordate = errordate[:10]
    errordate = datetime.strptime(errordate,'%Y-%m-%d')
    errordate = errordate.date()
    errorlog = frappe.new_doc('Collection Journal Entry Error Log')
    errorlog.date = datetime.now().date()
    errorlog.collection_report_date = errordate
    print('ERRORDATE: ',errordate)
    errordate_str = errordate.strftime('%Y-%m-%d')
    for e in error_list:
        errorlog.append('error_list',{
            'file':file,
            'row':e['row'],
            'field':e['field'],
            'value':e['value'],
            'description':e['description']
        })
        print('---------------------e----------------------------------------------')
        print(e)

    # print('error list ------------------------------------------------------------')
    # print(error_list)
    print('errorlog:: ',errorlog)
    errorlog.save()
    print('errorlog:: ',errorlog)
    print('name:: ',errorlog.name)
    # domain = 'http://175.136.236.153:8003' + '/app/journal-entry-error-log/'+ errorlog.name
    # domain = 'http://127.0.0.1:8000' + '/app/journal-entry-error-log/'+ errorlog.name
    domains = domain + '/app/collectin-journal-entry-error-log/'+ errorlog.name
    error_link = "<a href='"+domains+"' target='_blank'>Error Log "+str(errordate_str)+"</a>"

    msg = 'A collection journal entry error log has been made for Collection Report '+str(errordate)+'. Please see here '+error_link
    title = 'ERPNext: Collection Journal Entry Error Log '+str(errordate)
    sendEmail(msg,title,errorlog.doctype,errorlog.name)
    # email_list = getEmail('Accounts Manager')
    # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
    # email_args = {
    #     # 'recipients':user1.email,
    #     'recipients':email_list,
    #     'message':msg,
    #     'subject':title,
    #     'reference_doctype':errorlog.doctype,
    #     'reference_name':errorlog.name
    # }
    # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)

    if not much:
        # frappe.msgprint('There is error(s) when trying to import the Collection Report. You can see the list here ' +error_link)
        return error_link,errorlog.name
    else:
        return error_link,errorlog.name
    # name = errorlog.name
    # errorlog = frappe.get_doc({
    #     'doctype':'Journal Entry Error Log',
    #     'field_name':'collection_report_csv'
    # })
    # pathtofile, filename, filedata,cr = createCSV(cr,errordate)
    # print('path: ',pathtofile)
    # print('filename: ',filename)
    # with open(pathtofile,'r') as file:
    #     reader = csv.reader(file)
    #         # for i in row:
    #         #     print('type: ',type(i))
    #     for row in reader:
    #         print('types: ',type(row))
    #     filedata = io.StringIO(newline='').write('\n'.join([','.join(row) for row in reader]))
    #     print('filedata: ',filedata)

    # print('cr type: ',type(cr))
    # file_data = frappe.utils.file_manager.save_file_on_filesystem(filename,filedata)
    # print('file url: ',file_data['file_url'])
    # errorlog.collection_report_csv = file_data['file_url']
    # errorlog.save()

def getDateOnly(start_date):
    date_only = start_date[:10]
    new_date = datetime.strptime(date_only,'%Y-%m-%d')
    return new_date

def sendEmail(msg,subject,doctype,name):
    userlist = []
    users = frappe.get_all('User')
    for user in users:
        u = frappe.get_last_doc('User',filters={'name':user.name})
        rolelist = u.roles
        if rolelist:
            for r in rolelist:
                if r.role == 'Accounts Manager':
                    userlist.append(u.email)
                    break  
    email_args = {
        'recipients':userlist,
        'message':msg,
        'subject':subject,
        'reference_doctype':doctype,
        'reference_name':name
    }
    frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)

def getTitleName(posting_date):
    # if isinstance(posting_date, str):
    #    posting_date = datetime.strptime(posting_date, '%Y-%m-%d') 
    # month = posting_date.strftime('%B')
    # year = posting_date.year

    if not isinstance(posting_date,str):
        posting_date = posting_date.strftime('%Y-%m-%d')

    # title = 'Collection - ' + month +' '+ str(year)
    title = 'Collection - ' + posting_date
    return title

def createAccountingEntries(journal,cr,end_date):
    latest_posting = date(day=1,month=1,year=1900)
    posting_date = ''

    if len(cr) < 2:
        # now = datetime.now().strftime('%Y-%m-%d')
        # new_date = datetime.strptime(now, '%Y-%m-%d').date() + timedelta(days=1)
        # journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
        # tag_id = getDateOnly(dates)
        # tag_id_str = tag_id.strftime('%Y-%m-%d')
        # journal.tag_id = end_date
        journal.posting_date = end_date
        je_name = 'Collection - '+str(end_date)
        journal.title = je_name
        journal.noaccount = 'No Current Month Import Data For This Month'
        journal.save()
        domains = domain + '/app/journal-entry/'+ journal.name
        journal_link = "<a href='"+domains+"' target='_blank'>Collection Journal Entry "+str(end_date)+"</a>"
        # frappe.msgprint('One Journal Entry has been created, See Here ')
        return je_name,journal_link
    else:
        counter = 1
        total_debit = 0
        total_credit = 0
        
        for row in cr:
            # debit
            # print('ROW')
            # print(row)
            # row_list = []
            try:
                row['debit']
                counter = 1
            except:
                counter = 2
            print('rowww:----------: ',row)
            print('postinggg----dateeee: ',row['posting_date'])
            posting_date = getDatetimeDate(row['posting_date'])
            if latest_posting < posting_date:
                latest_posting = posting_date

            if counter == 1:
                
                debit_acc = frappe.get_last_doc("Account", filters={"account_number":row['account_number']})
                cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['cost_center_number']})
                row['account'] = debit_acc.name
                row['cost_center'] = cost_center.name
                total_debit += float(row['debit'])
                # print('total_debit: ',total_debit)
                # print('----debit: ',row['debit'])
                row['debit_in_account_currency'] = row['debit']
                
            # credit
            elif counter == 2:
                counter = 1
                

                credit_acc = frappe.get_last_doc("Account", filters={"account_number":row['account_number']})
                cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['cost_center_number']})
                total_credit += float(row['credit'])
                row['account'] = credit_acc.name
                row['cost_center'] = cost_center.name
                # print('----credit: ',row['credit'])
                row['credit_in_account_currency'] = row['credit']
                


        # --------------------------------------logic for deferred and revenue----------------
            # for l in last_acc_list:
            #     if row_list[0].account_number == l[0].account_number:
            #         if row_list[1].account_number == l[1].account_number:
            #             # update first row of last
            #             updateLastRow(journal,l[0],1,1)
            #             # update second row of last
            #             updateLastRow(journal,l[1],1,-1)
            #             # update third row of last
            #             updateLastRow(journal,l[2],2,1)
            #             # update fourth row of last
            #             updateLastRow(journal,l[3],2,-1)

            #             # create first new row
            #             createNewRow(journal,row_list[0])
            #             # create first new row
            #             createNewRow(journal,row_list[1])
        
        # --------------------------------------logic for deferred and revenue----------------
            journal.append('accounts',row)

        # now = datetime.now().date()
        journal.total_debit = total_debit
        journal.total_credit = total_credit
        journal.entry_type = "Journal Entry"
        
        journal.posting_date = latest_posting
        # print('--------------POSTING DATE: ',posting_date)
        # month = getMonth(posting_date)
        # year = latest_posting.year
        # tag_id = getDatetime(posting_date)

        # tag_id_str = tag_id.strftime('%Y-%m-%d')
        # journal.tag_id = tag_id
        # journal.save()
        # journal.submit()
        # company = frappe.get_last_doc('Company',filters={'company_name':journal.company})
        # journal.title = journal.report_type + ' - '+month+' '+str(year)
        journal.title = 'Collection - '+str(posting_date)
        # journal.save()
        # journal.submit()
        # je_name = journal.name
        # print('je_name: ',je_name)

        # domains = domain + '/app/journal-entry/'+ je_name
        # journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+tag_id_str+"</a>"
        # # frappe.msgprint('One Journal Entry has been created, See Here ')
        # msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
        # title = 'ERPNext: Journal Entry '+str(posting_date)
        # return je_name,journal_link


# def createJE(cr,start_date):
#     journal = frappe.new_doc("Journal Entry")

#     if not len(cr):
#         now = datetime.now().strftime('%Y-%m-%d')
#         new_date = datetime.strptime(now, '%Y-%m-%d').date() + timedelta(days=1)
#         journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         tag_id = getDateOnly(start_date)
#         tag_id_str = tag_id.strftime('%Y-%m-%d')
#         journal.tag_id = tag_id
#         journal.save()
#         journal.submit()
#         je_name = journal.name
#         return je_name,''
#     else:
#         counter = 1
#         posting_date = ''
#         row = cr
#         for row in cr:
#             # debit
#             print('ROW')
#             print(row)
#             if counter == 1:
#                 counter+=1

#                 year = row[1]
#                 account_number = row[2]
#                 cost_center_number = row[3]
#                 currency = row[12]
#                 debit = row[15]
#                 remark = row[23]
#                 posting_date = row[30]
#                 group = row[31]

                
#                 debit_acc = frappe.get_last_doc("Account", filters={"account_number":account_number})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":cost_center_number})

#                 journal.append('accounts',{
#                     'account':debit_acc.name,
#                     'account_number':debit_acc.account_number,
#                     'cost_center':cost_center.name,
#                     'currency':currency,
#                     'debit_in_account_currency' : float(debit),
#                     'credit_in_account_currency' : float(0),
#                     'remark':remark,
#                     'group':group,
#                     'year': year,
#                     'posting_date':posting_date
#                 })

#             # credit
#             elif counter == 2:
#                 counter = 1
#                 year = row[1]
#                 account_number = row[2]
#                 cost_center_number = row[3]
#                 currency = row[12]
#                 credit = row[15]
#                 remark = row[23]
#                 posting_date = row[30]
#                 group = row[31]

#                 credit_acc = frappe.get_last_doc("Account", filters={"account_number":account_number})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":cost_center_number})

#                 journal.append('accounts',{
#                     'account':credit_acc.name,
#                     'account_number':credit_acc.account_number,
#                     'cost_center':cost_center.name,
#                     'currency':currency,
#                     'debit_in_account_currency' : float(0),
#                     'credit_in_account_currency' : abs(float(credit)),
#                     'remark':remark,
#                     'group':group,
#                     'year': year,
#                     'posting_date':posting_date
#                 })

#         now = datetime.now().date()
#         journal.entry_type = "Journal Entry"
#         # new_date = datetime.strptime(posting_date, '%Y-%m-%d').date() + timedelta(days=1)
#         # journal.posting_date = now         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         journal.posting_date = posting_date
#         tag_id = getDateOnly(start_date)
#         tag_id_str = tag_id.strftime('%Y-%m-%d')
#         journal.tag_id = tag_id
#         journal.title = getTitleName(posting_date)
#         journal.save()
#         journal.submit()
#         je_name = journal.name

#         # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je_name
#         # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
#         domains = domain + '/app/journal-entry/'+ je_name
#         journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+tag_id_str+"</a>"
#         # frappe.msgprint('One Journal Entry has been created, See Here ')
#         msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
#         title = 'ERPNext: Journal Entry '+str(posting_date)
#         # sendEmail(msg,title,journal.doctype,journal.name)
#         # email_list = getEmail('Accounts Manager')
#         # email_args = {
#         #     'recipients':user1.email,
#         #     'message':msg,
#         #     'subject':title,
#         #     'reference_doctype':journal.doctype,
#         #     'reference_name':journal.name
#         # }
#         # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)

#         return je_name,journal_link

def createJE(cr,end_date,batch_id):
    print('=================================================cr======')
    print(cr)
    journal = frappe.new_doc("Journal Entry")
    journal.report_type = 'Collection'
    posting_date = ''
    # print('CRRRR')
    # print(cr)
    print('LENGTH: ',len(cr))
    latest_posting = date(day=1,month=1,year=1900)
    # je_name, journal_link = createAccountingEntries(journal,cr,end_date)
    createAccountingEntries(journal,cr,end_date)
    # print('journal_link: ',journal_link)
    # createDeferredAccountingEntries(journal,end_date)
    journal.save()
    # print('batchid je: ',batch_id)
    journal.tag_id = batch_id
    journal.save()
    journal.submit()
    frappe.db.commit()


def getNewDate():
    docs = frappe.get_list('Journal Entry',filters={'report_type':'Collection'})
    if docs:
        doc = frappe.get_last_doc('Journal Entry',filters={'report_type':'Collection'})
        tag_id = doc.tag_id
        month = tag_id.month
        year = tag_id.year
        month+=1
        if month==13:
            month = 1
            year +=1
        days = calendar.monthrange(year,month)
        new_date = date(day=days[1],month=month,year=year)
    else:
        new_date = date(year=2023,month=1,day=1)
    return new_date, new_date

def checkFile(cr_dict,cr,batch_id,new_date):
    date_str = getDateString(new_date)
    doc_name = 'Collection - '+date_str
    print('batch id in checkfile: ',batch_id)
    return_dict = {'doc_name':doc_name,'new_posting_date':new_date,'cr_dict':cr_dict,'batch_id':batch_id}
    try:
        return_dict['cr'] = cr
    except:
        pass
    return return_dict

def doImportCollectionReportSingle(file,cr_dict,cr,batch_id,new_date):
    global domain
    domain = getDomain()
    scheduler_cr = frappe.get_last_doc('Scheduler Manager',filters={'name':'Collection Report (Import)'})
    controller = scheduler_cr.control
    # if controller == 'Play':
    #     print('Scheduler: Play')
    #     pass
    # elif controller == 'Stop':
    #     print('Scheduler: Stop')
    #     return
    # much = False
    # if start_date != end_date:
    #     much = True
    #     ready,cr_able,cr_unable = checkReadyCR(much,start_date,end_date)
    # else:
    #     much = False
    #     ready,cr_able,cr_unable = checkReadyCR(much,start_date,end_date)
    #     print('CR ABLE: ',cr_able)

    #--------------------------------------
    # cr_exist = getDocList('Journal Entry',{'report_type':'Collection'},True)
    # if cr_exist:
    #     doc = getDoc('Journal Entry',{'report_type':'Collection'})
    #     last_posting_date = doc.posting_date
    #     month = last_posting_date.month
    #     year = last_posting_date.year
    #     new_posting_date = getNextDate(last_posting_date)
    #     if month == 1:
    #         filename = '24_string(24) perfect data.csv'
    #         file = frappe.get_last_doc('File',filters={'file_name':filename})
    #         # getCrString15(template,'')
    #         cr_dict,cr = getCr(filename)
    #         # print('typeeeee: ',type(cr_dict))
    #         # print('crdict after type: ',cr_dict)
    #     elif month == 2:
    #         filename = '25_string(25) perfect data.csv'
    #         file = frappe.get_last_doc('File', filters={'file_name':filename})
    #         # template = True
    #         # cr_dict,cr = getCrString15(template,new_posting_date)
    #         # cr_dict = getCrString15(template,new_posting_date)
    #         # print('typeeeee: ',type(cr_dict))
    #         # print('crdict after type: ',cr_dict)
    #         cr_dict,cr = getCr(filename)
    #     elif month == 3:
    #         filename = '26_string(26) perfect data.csv'
    #         file = frappe.get_last_doc('File', filters={'file_name':filename})
    #         # template = True
    #         # cr_dict,cr = getCrString15(template,new_posting_date)
    #         # cr_dict = getCrString15(template,new_posting_date)
    #         cr_dict,cr = getCr(filename)
    #         print('typeeeee: ',type(cr_dict))
    #         print('crdict after type: ',cr_dict)
    #     else:
    #         now = datetime.now().date()
    #         if month >= now.month:
    #             raise Exception('Cannot import next month billing report')
    # else:
    #     new_posting_date = date(year=2023,month=1,day=31)
    #     filename = '23_string(23) perfect data.csv'
    #     cr_dict,cr = getCr(filename)
    #     month = new_posting_date.month
    
    # date_str = getDateString(new_posting_date)
    # doc_name = 'Billing - '+date_str

    # batch_id = getBatchID(filename,month)
    # print('batch id in checkfile: ',batch_id)
    # return_dict = {'doc_name':doc_name,'new_posting_date':new_posting_date,'cr_dict':cr_dict,'batch_id':batch_id}

    # try:
    #     return_dict['cr'] = cr
    # except:
    #     pass
    # return return_dict
    # --------------------------------------
    return_dict = checkFile(cr_dict,cr,batch_id,new_date)
    doc_name = return_dict['doc_name']
    cr_dict = return_dict['cr_dict']
    batch_id = return_dict['batch_id']
    new_date = return_dict['new_posting_date']

    exist, name = checkExist(batch_id,'Collection')
    date_str = getDateString(new_date)
    if exist:
        print('Journal Entry of Collection for ',date_str,' is already create. You can see here '+name)
        # raise Exception('Journal Entry of Collection for ',date_str,' is already create. You can see here '+name)
    else:
        print('------------------date is ',new_date)

    error,error_log_name_list,error_link,error_list = importfrombs(file,cr_dict)
    if error:
        # for log in error_log_name_list:
        #     doc.append('journal_entry_error_log',{
        #         'journal_entry_error_log':log,
        #     })
        # print('-----error yes')
        frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
    else:
        print('no error')
        # journal = createJE(cr_dict,new_date)
        # je_name,journal_links = createJE(cr_dict,new_date,batch_id)
        createJE(cr_dict,new_date,batch_id)

    # # pervious ---------------------------------
    # now = datetime.now().date()
    # start_date = end_date = now - timedelta(days=1)
    # start_date, end_date = getNewDate()
    # print('start end: ',start_date,' ',end_date)
    # # start_date = date(2023,1,1)
    # # end_date = date(2023,1,1)
    # je_exist,link_list = checkJEExist(start_date, end_date)
    # if je_exist == True:
    #     # if len(link_list) > 1:
    #     #     link_str = ''
    #     #     for l in link_list:
    #     #         link_str += l +','
    #     #     print('Journal Entry For The Date Already Exist')
    #     #     return
    #     #     raise Exception('Journal Entry For The Dates Already Exist. See here '+link_str)
    #     # else:
    #     print('Journal Entry For The Date Already Exist')
    #     for i in link_list:
    #         print('link list: ',i)
    #     return
    #     raise Exception('Journal Entry For The Date Already Exist. See here '+link_list[0])
    # elif je_exist == False:
    #     # ready,cr_able,cr_unable = checkReadyCR(start_date,end_date)
    #     file = frappe.get_last_doc('File',filters={'file_name':'11_CollectionReport.csv'})
    #     attach_csv = file.file_url
    #     site = frappe.utils.get_site_path()
    #     split = site.split('/')
    #     site = split[1]
    #     attach_csv = site+attach_csv
    #     cr_able = []
        
    #     with open(attach_csv,'r') as file:
    #         reader = csv.reader(file)
    #         # print('reader')
    #         # print(reader)
    #         for r in reader:
    #             # print('row: ',r)
    #             r[30] = start_date
    #             cr_able.append(r)
            
    #     # much,exist,cr_able,cr_unable = checkReadyCR(start_date,end_date)
    #     error_log_name_list = []
    #     journal_entry_name_list = []
    #     # journal_entry_link = []
    #     # if not much:
    #     # print('READY: ',ready)
    #     ready = True
    #     print(cr_able)
    #     # cr = cr_able['cr']
    #     cr = cr_able
    #     print('CR:',cr)
    #     # print(cr)
    #     # empty_cr = False
    #     # if not len(cr):
    #     #     empty_cr = True
    #     # if empty_cr:
    #     #     createJE(cr,cr_date)
    #     # else:
    #     # cr_date = cr_able['date']
    #     if ready:
    #         # print('------------cr------------')
    #         # print(cr_able)
    #         error_result, error_list = handleError(cr)
    #         print('ERROR RESULT: ',error_result)
    #         print('ERROR LIST: ', error_list)
    #         cr_date = start_date.strftime('%Y-%m-%d')
    #         if error_result == True:
    #             error_link,error_name = createErrorLog(False,error_list,cr_date)
    #             error_log_name_list.append(error_name)
    #             frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
    #             print('end of scheduler')
    #             # return False,error_log_name_list
    #         else:
    #             journal_name, journal_link = createJE(cr,cr_date)
    #             journal_entry_name_list.append(journal_name)
    #             frappe.msgprint('One Journal Entry has been created, See Here '+journal_link)
    #             print('end of scheduler')
    #             # return True,journal_entry_name_list
    #     else:
    #         raise Exception('Collection Report Is Not Available Yet.')
    #     #------ end of previous --------------------------------------

    # error_result, error_list = handleError(cr)
    # print('error result: ',error_result)
    # if error_result == True:
    #     createErrorLog(error_list,cr,datetime.now().date())
    # else:
    #     createJE(cr)
    print('DONE SCHEDULER')
    return error_list

def importfrombs(file,cr_dict):
    cr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    error_log_name_list = []
    journal_entry_name_list = []
	# journal_entry_link = []
    # print('cr-dict: -------------------')
    # print(cr_dict)

    error_result, error_list = handleError2(file,cr_dict)
    print('ERROR RESULT: ',error_result)
    print('ERROR LIST: ', error_list)
    print('LENGTH CR: ',len(cr_dict))
    if error_result == True:
        error_link,error_name = createErrorLog(file,False,error_list,cr_date)
        error_log_name_list.append(error_name)
        # frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
        return error_result,error_log_name_list,error_link,error_list
    return error_result,'','',error_list

    # journal_links = ''
    # # for cr in cr:
    # #     journal_name, journal_link = createJE(cr,end_date)
    # #     journal_entry_name_list.append(journal_name)
    # #     journal_links += journal_link+', '
    # end_date = '31-01-2023'
    # journal_name, journal_link = createJE(cr,end_date)
    # journal_entry_name_list.append(journal_name)
    # journal_links += journal_link+', '

    # frappe.msgprint('Journal Entries has been created, See Here '+journal_links)
    # return error_result,journal_entry_name_list,journal_link

	# if not much:
	# 	print('READY: ',ready)
	# 	cr = cr_ready[0]['cr']
	# 	cr_date = cr_ready[0]['date']
	# 	if ready:
	# 		error_result, error_list = handleError(cr)
	# 		print('ERROR RESULT: ',error_result)
	# 		print('ERROR LIST: ', error_list)
	# 		if error_result == True:
	# 			error_link,error_name = createErrorLog(False,error_list,cr_date)
	# 			error_log_name_list.append(error_name)
	# 			frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
	# 			return False,error_log_name_list
	# 	else:
	# 		print('Collection Report Is Not Available Yet.')
	# 		raise Exception('Collection Report Is Not Available Yet.')
	# else:
	# 	if not ready:
	# 		notready_list = ''
	# 		for un in cr_notready:
	# 			notready_list += un+', '
	# 		raise Exception('The Following(s) Collection Report Is Not Available Yet : ',notready_list)
	# 	if ready:   
	# 		error_log_link_list = []
	# 		error_lists = []
	# 		error_exist = False
	# 		for c in cr_ready:
	# 			error_result, error_list = handleError(c['cr'])
	# 			print(c['cr'])
	# 			if error_result:
	# 				error_exist = True
	# 				error_item = {'error_list':error_list,'date':c['date']}
	# 				error_lists.append(error_item)
			
	# 		if error_exist:
	# 			for e in error_lists:
	# 				error_link,error_name = createErrorLog(True,e['error_list'],e['date'])
	# 				error_log_link_list.append(error_link)
	# 				error_log_name_list.append(error_name)
	# 			error_links = ''
	# 			for n in error_log_link_list:
	# 				error_links += n +', '
				
	# 			frappe.msgprint('There is error(s) when trying to import the Collection Report. No Journal Entry is created. You can see the list of the errors here '+error_links)
	# 			return False,error_log_name_list


def checkJEExist(start_date, end_date):
    start_year = start_date.year
    end_year = end_date.year
    report_exist = []
    journal_link_list = []
    # if start_year != end_year:
    #     raise Exception('Start Date and End Date Must Be In The Same Year')
    if start_date == end_date:
        try:
            je = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','tag_id':start_date})
            print('START DATE: ',start_date)
            tag_id = je.tag_id.strftime('%Y-%m-%d')
            # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
            # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je.name
            domains = domain + '/app/journal-entry/'+ je.name
            journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+tag_id+"</a>"
            journal_link_list.append(journal_link)
            # frappe.throw('Journal Entry already exist!')
            return True, journal_link_list
            # raise Exception('Journal Entry already existgfgth!')
        except:
            # report_exist.append(str(start_date))
            tag_id = start_date.strftime('%Y-%m-%d')
            return False,''
    # else:
    #     diff = end_date - start_date
    #     diff_day = diff.days + 1
    #     start_day = start_date.day - 1
    #     year = start_year
    #     month = start_date.month
	# 	# print('startdaate: ',start_date)
    #     # report_exist = []

    #     for i in range(diff_day):
    #         start_day += 1
    #         new_date = date(year,month,start_day)
    #         try:
    #             je = frappe.get_last_doc('Journal Entry', filters={'tag_id':new_date})
    #             report_exist.append(str(new_date))
    #             tag_id = je.tag_id.strftime('%Y-%m-%d')
    #             domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
    #             journal_link = "<a href='"+domain+"' target='_blank'>Journal Entry "+tag_id+"</a>"
    #             journal_link_list.append(journal_link)
    #         except:
    #             pass
        
    #     length = len(report_exist)
    #     if length != 0:
            # warning = ''
            # for i in range(length):
            #     warning += report_exist[i]+', '
            #     if length > 1:
            #         raise Exception('Following Journal Entries Already Exists: '+warning)
            #     else:
            #         raise Exception('This Journal Entry Already Exists: '+warning)
            # return False,journal_link_list
    # return True,''


# scheduler function for billing import collection report
# def doImportBillingReport():
#     billing_import_scheduler = frappe.get_last_doc('Scheduler Manager', filters={'scheduler':'Billing Report'})
#     control = billing_import_scheduler.control

#     if control == 'Play':
#         print('----------------------------Scheduler Import Billing Report : Playing')
#         # userlist = getEmail('Accounts Manager')
#         # print('User List: ',userlist)
#         # msg = 'A journal entry error log has been made for Collection Report '+'123'+'. Please see here '+'123 domain is ',domain
#         # title = 'ERPNext: Journal Entry Error Log '+'123'
#         # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
#         # email_args = {
#         #     'recipients':userlist,
#         #     'message':msg,
#         #     'subject':title,
#         #     'reference_doctype':'Billing Import Collection Report',
#         #     'reference_name':'84d680cd60'
#         # }
#         # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)
#         # print('Email sent')

#         now = datetime.now()
#         today = now.date()
#         start_date = end_date = today - timedelta(days=1)

#         # testing purpose
#         year = now.year
#         month = now.month
#         month = 1       # for testing only, january
#         start_date = date(day=1,month=month,year=year)
#         end_date = date(day=calendar.monthrange(year,month)[1], month=month, year=year)
#         print('start_date: ',start_date,' end_date: ',end_date)

#         doc = frappe.new_doc('Import Billing Report')
#         # billingcr.start_date = start_date
#         # billingcr.end_date = end_date
#         # csv_file = frappe.get_last_doc('File',filters={'name':})
#         doc.start_date = now
#         doc.end_date = now
#         doc.save()

#         # print('rolessss')
#     else:
#         print('----------------------Scheduler for Billing Import is Stop')

# def testcron():
#     print('POOOOOOOOOOOOOOOOPOPOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')

# def getDomain():
#     # domain = get_url()
#     # print('DOMAIN1 : ',domain)

#     # domain = frappe.utils.get_url_to_form('User','syafiq@gmail.com')
#     # doman = frappe.utils.get_request_url()
#     # domain = frappe.local
#     domain = frappe.utils.get_url()
#     print('----Domain: ',domain)

#     # domain = frappe.utils.get_host_name()
#     # print('DOmain: ',domain)

#     return domain

# @frappe.whitelist(allow_guest=True)
def doImportCollectionReport():
    errors=[]
    getFileData = {"name": "Collection"}
    headers = {
        "Content-Type": "application/json",
    }
    # prod internal
    getFileReqUrl = 'http://172.18.92.101:80/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    returnReqUrl = 'http://172.18.92.101:80/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
    # prod
    # getFileReqUrl = 'https://bsportal.indahwater.app:8443/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    # returnReqUrl = 'https://bsportal.indahwater.app:8443/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
    # Staging
    # getFileReqUrl = 'https://bsstg1.indahwater.app:8443/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    # returnReqUrl = 'https://bsstg1.indahwater.app:8443/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
    response = requests.request("POST", getFileReqUrl,headers=headers,json=getFileData, verify=False)  
    if response.status_code == 200:
        zip = response.content
        zip_file = zipfile.ZipFile(io.BytesIO(zip))
        file_list = zip_file.namelist()
        for file in file_list:
            if file in file_list:
                cr_dict,cr = getCr2_pass_file(zip_file,file,1)
                split = file.split('_')
                fileDate = split[2].split('.')[0]
                dateSplit = fileDate.split('-')
                year=dateSplit[0]
                month=dateSplit[1]
                day=dateSplit[2]
                new_date = date(year=int(year),month=int(month),day=int(day))
                batch_id = getBatchID2(file,day)
                print('--------------filenamessss: ',file)
                error_list = doImportCollectionReportSingle(file,cr_dict,cr,batch_id,new_date)
                errors.append(error_list)
    if errors !=[]:
        flattened_data = [item for sublist in errors for item in sublist]
        returnData =  {"name": "Collection", "errorFileSummary":flattened_data}
    else:
        returnData =  {"name": "Collection", "errorFileSummary":[]}
    print('errors: ',returnData)
    response = requests.request("POST", returnReqUrl,headers=headers,json=returnData, verify=False)  
    if response.status_code == 200:
        print("Request was successful (Status Code 200).")
    
