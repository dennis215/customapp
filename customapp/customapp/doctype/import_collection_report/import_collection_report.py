# Copyright (c) 2023, mysite and contributors
# For license information, please see license.txt
# search for 'for_uat', please remove 

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta, date, time
import csv, requests, json, calendar, os
# from frappe.utils.file_manager import upload
# from frappe.core.doctype.file.file import File
import io
from customapp.general_function import *

class ImportCollectionReport(Document):
	# pass
    def before_insert(self):
        global domain 
        # domain = 'http://175.136.236.153:8003'
        # domain = 'http://127.0.0.1:8000'
        domain = getDomain()
        start_date = self.start_date
        end_date = self.end_date
        start_date = datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
		# if self.end_date == '':
		# 	self.end_date = start_date
        # end_date = datetime.strptime(end_date,'%Y-%m-%d')
        
        if end_date < start_date:
            raise Exception('Error: End Date Can Not Be Less Than Start Date!')
        today = datetime.now().date()
        if end_date > today:
            raise Exception('Error: End Date Can Not Be Latter Than Today!')
        
        # for_uat
        # doUAT(start_date,end_date)
        # file = checkFile(start_date,end_date)
        return_dict = checkFile(start_date,end_date)
        doc_name = return_dict['doc_name']
        cr_dict = return_dict['cr_dict']
        batch_id = return_dict['batch_id']
        new_date = return_dict['new_posting_date']

        exist, name = checkExist(batch_id,'Collection')
        date_str = getDateString(new_date)

        if exist:
            domains = domain + '/app/journal-entry/'+ name
            journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+date_str+"</a>"
            print('Journal Entry of Collection for ',date_str,' is already create. You can see here '+name)
            raise Exception('Journal Entry of Collection for ',date_str,' is already create. You can see here '+journal_link)
        else:
            print('------------------date is ',new_date)
        
        error,error_log_name_list,error_link = importfrombs(cr_dict)
        if error:
            frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
        else:
            je_name,journal_links = createJE(cr_dict,end_date,batch_id)
            self.append('journal_entry',{
                'journal_entry':je_name,
            })
            frappe.msgprint('Journal Entries has been created, See Here '+journal_links)


        # je_exist,link_list = checkJEExist(start_date, end_date,file)

        # if je_exist == True:
        #     if len(link_list) > 1:
        #         link_str = ''
        #         for l in link_list:
        #             link_str += l +','
        #         raise Exception('Journal Entry For The Dates Already Exist. See here '+link_str)
        #     else:
        #         raise Exception('Journal Entry For The Date Already Exist. See here '+link_list[0])
		# print('---------IMPORT-----------')
        # print(type(start_date))
        # print(type(end_date))
        # # print('--------------------------')
        # status,name_lists = importfrombs(start_date,end_date,file)

        # if not status:
        #     for name in name_lists:
        #         self.append('journal_entry_error_log',{
        #             'journal_entry_error_log':name
        #         })
        #     # frappe.db.set_single_value('Import Collection Report',self.name,'journal_entry_error_log','No Journal Entry Error Generated')
        #     # self.journal_entry_error_log.description = 'No Journal Entry Error Generated'
        # else:
        #     for name in name_lists:
        #         self.append('journal_entry',{
        #             'journal_entry':name
        #         })

        # if not status:
        #     print('status: ',status)
		# 	# frappe.validated = False
		# 	# raise Exception('apapapapa')
		# 	# frappe.throw('blablabla')
		# 	# return False
        #     self.status = 0
        #     return False
        # return True


def checkFile(start_date,end_date):
    if start_date == end_date:
        much = False
        # if start_date == date(day=31,month=12,year=2022):
        #     file = frappe.get_last_doc('File',filters={'file_name':'CollectionReport (1).csv'})
        #     batch_id = 20221231
        # else:
        #     file = frappe.get_last_doc('File',filters={'file_name':'11_CollectionReport.csv'})
            # batch_id = 
        new_posting_date = start_date
        month = new_posting_date.month
        filename = '23_string(23) perfect data.csv'
        # if month == 1:
        #     filename = '23_string(23) perfect data.csv'
            # file = frappe.get_last_doc('File',filters={'file_name':filename})
            # getCrString15(template,'')
            # cr_dict,cr = getCr2(filename,new_posting_date)
            # print('typeeeee: ',type(cr_dict))
            # print('crdict after type: ',cr_dict)
        if month == 2:
            filename = '24_string(24) perfect data.csv'
            # file = frappe.get_last_doc('File', filters={'file_name':filename})
            # template = True
            # cr_dict,cr = getCrString15(template,new_posting_date)
            # cr_dict = getCrString15(template,new_posting_date)
            # print('typeeeee: ',type(cr_dict))
            # print('crdict after type: ',cr_dict)
            # cr_dict,cr = getCr2(filename,new_posting_date)
        elif month == 3:
            filename = '25_string(25) perfect data.csv'
            # file = frappe.get_last_doc('File', filters={'file_name':filename})
            # template = True
            # cr_dict,cr = getCrString15(template,new_posting_date)
            # cr_dict = getCrString15(template,new_posting_date)
            # cr_dict,cr = getCr2(filename,)
            # print('typeeeee: ',type(cr_dict))
            # print('crdict after type: ',cr_dict)
        elif month == 4:
            filename = '26_string(26) perfect data.csv'
            # file = frappe.get_last_doc('File', filters={'file_name':filename})
            # cr_dict,cr = getCr2(filename)
        cr_dict,cr = getCr2(filename,new_posting_date)
        # else:
        #     now = datetime.now().date()
        #     print('month: ',month)
        #     filename = 'Invalid'
        #     cr_dict = 'Invalid'
        #     if month >= now.month:
        #         raise Exception('Cannot import next month billing report')
    else:
        raise Exception('There is an error occur during execution.')

    date_str = getDateString(new_posting_date)
    doc_name = 'Collection - '+date_str

    batch_id = getBatchID2(filename,month,new_posting_date.day)
    print('batch id in checkfile: ',batch_id)
    return_dict = {'doc_name':doc_name,'new_posting_date':new_posting_date,'cr_dict':cr_dict,'batch_id':batch_id}

    try:
        return_dict['cr'] = cr
    except:
        pass
    return return_dict    
    # else:
    #     much = True
    #     ready,cr_able,cr_unable = checkReadyCR(much,start_date,end_date)

    # return much, file

def importfrombs(cr_dict):
    cr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    error_log_name_list = []

    error_result, error_list = handleError2(cr_dict)
    print('ERROR RESULT: ',error_result)
    print('ERROR LIST: ', error_list)
    print('LENGTH CR: ',len(cr_dict))
    if error_result == True:
        error_link,error_name = createErrorLog(False,error_list,cr_date)
        error_log_name_list.append(error_name)
        # frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
        return error_result,error_log_name_list,error_link
    return error_result,'',''


# def getBatchIDDate(dates):
#     if isinstance(dates, str):
#         dates = datetime.strptime(dates, '%Y-%m-%d').date()
#     month = dates.month
#     day = dates.day
#     year = dates.year
#     days = str(day)
#     months = str(month)

#     if len(str(day)) < 2:
#         days = '0'+str(day)
    
#     if len(str(month)) < 2:
#         months = '0' + str(month)
    
#     batch_id = days + months + str(year)
#     return batch_id

def getAccountManagerEmail():
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
                if r.role == 'Accounts Manager':
                    userlist.append(u.email)
                    break
    
    return userlist

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
#     user_remark = row_list['user_remark']
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
#     # # objParentAccount = {'field2':'parent_account','val2':'Bank - I'}
#     # # checkError(objURaccount,1,objParentAccount,row,errors,error_list,'') # check bank account exist
#     # objURdate = {'field':'user_remark','value':user_date}
#     # checkError(objURdate,5,'',row,errors,error_list,'')
#     # # posting date
#     # checkError(objPostingDate,6,'',row,errors,error_list,'')

#     return balance  

# def getDate(scheduler,crdate):
#     if scheduler:
#         today = datetime.now()
#         today = today.strftime('%Y-%m-%d')
#         today = datetime.strptime(today, '%Y-%m-%d')
#         start_date = today + timedelta(hours=0,minutes=0,seconds=0,milliseconds=0)
#         start_date = start_date.isoformat()+"Z"
#         end_date = today + timedelta(hours=23,minutes=59,seconds=59)
#         end_date = end_date.isoformat()+"Z"
#         year = today.year
#         return start_date, end_date, year

#     else:
#         start_date = crdate['start_date']
#         end_date = crdate['end_date']
#         year = start_date.year
#         times = time(0,0,0)
#         start_date = datetime.combine(start_date,times)
#         end_date = datetime.combine(end_date,times)
#         print('------type: ',type(start_date))
#         start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
#         start_date = start_date.isoformat()+"Z"
#         print('++++++++++++++STARTDATE')
#         print(start_date)
#         end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
#         end_date = end_date.isoformat()+"Z"

#         return start_date, end_date, year

# def getDateFormat(dates):
#     if isinstance(dates, str):
#         dates = datetime.strptime(dates,'%Y-%m-%d')
#     return dates

# def getCR(start_end_year,existcr):
#     start_date = start_end_year['start_date']
#     end_date = start_end_year['end_date']
#     year = start_end_year['year']
#     reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextMthEndJob'})
# 	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
#     reqUrl = reportcr.url +reportcr.api_key
#     print('reqURL: ',reqUrl)

#     payload = json.dumps({
#     "startDate": start_date,
#     "endDate": end_date,
#     "name": "string",
#     "year": year
#     }, default=str)

#     print('payload: ',payload)

#     headersList = {
#     "Accept": "*/*",
#     "Content-Type": "application/json" 
#     }

#     response = requests.request("POST", reqUrl, data=payload, headers=headersList)

#     headers = response.headers
#     # print(headers)
#     msg = headers.get('return-message')
#     textt = response.content.decode('utf-8')
#     cr = csv.reader(textt.splitlines(), delimiter=',')
#     cr = list(cr)
#     print('===========CR==============')
#     print(cr)
#     # return True,cr
#     if 'filename=string.csv.tmp' in msg:
#         existcr['exist'] = False
#         return False,''
#         # raise Exception('The file you are trying to get is not in CSV format. Please try again later.')
#     else:
#         textt = response.content.decode('utf-8')
#         cr = csv.reader(textt.splitlines(), delimiter=',')
#         cr = list(cr)
#         # print('========cr=========:',cr)
#         return True,cr  

# for uat
# def getCR(start_end_year,existcr):
#     print('getCR')
#     start_date = start_end_year['start_date']
#     if start_date == date(day=1,month=12,year=2022):
#         filename = 'CollectionReport(1).csv'
#     else:
#         filename = '11_CollectionReport.csv'
#     file = frappe.get_last_doc('File',filters={'file_name':filename})
#     print('filename: ',filename)
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
#             # r[30] = getDateOnly(start_date)
#             r[30] = datetime.now().date()
#             cr_able.append(r)
#             # print('cr1: ',r)
#     # print('CR ABLE: ',cr_able)
#     # print('length: ',len(cr_able))

#     return True,cr_able


# def checkReadyCR(much,start_date,end_date):

#     # today = datetime.now()
#     # today = today.strftime('%Y-%m-%d')
#     # today = datetime.strptime(today, '%Y-%m-%d')
#     # start_date = today + timedelta(hours=0,minutes=0,seconds=0,milliseconds=0)
#     # start_date = start_date.isoformat()+"Z"
#     # end_date = today + timedelta(hours=23,minutes=59,seconds=59)
#     # end_date = end_date.isoformat()+"Z"
#     # year = today.year
#     scheduler = False
#     dates_list = []
#     start_end_year = {}

#     # if start_date != end_date:
#     if much:
#         diff = end_date - start_date
#         diff_day = diff.days + 1
# 		# print('startdaate: ',start_date)
#         counter = 0

#         for i in range(diff_day):
#             if i == 0:
#                 startdate = enddate = start_date
#                 date_dic = {'start_date':startdate,'end_date':enddate}
#                 startdate,enddate,year = getDate(scheduler,date_dic)
#                 start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#                 # date_dic = {'start_date':startdate,'end_date':enddate}
#                 dates_list.append(start_end_year)
#                 counter += 1
#             else:
#                 next_date = start_date + timedelta(days=counter)
#                 counter += 1
#                 startdate = enddate = next_date
#                 date_dic = {'start_date':startdate,'end_date':enddate}
#                 startdate,enddate,year = getDate(scheduler,date_dic)
#                 start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#                 dates_list.append(start_end_year)

#         # print('---------DATE LIST')
#         # print(dates_list)
#     else:
#         date_dic = {'start_date':start_date,'end_date':end_date}
#         startdate,enddate,year = getDate(scheduler,date_dic)
#         start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#     # scheduler = False   # for manual
#     # start_date = self.start_date
#     # end_date = self.end_date
#     # dates = {'start_date':start_date,'end_date':end_date}
#     # start_date, end_date, year = getDate(scheduler,dates)    

#     existcr = {}
#     cr_able = []
#     cr_unable = []
#     if much:
#         for d in dates_list:
#             ready,cr = getCR(d,existcr)
#             if cr == '':
#                 print('KOSONGGGG')
#             else:
#                 print('TAK KOSONGGGG')
#             if ready:
#                 cr_start = {'cr':cr,'date':d['start_date']}
#                 cr_able.append(cr_start)
#             else:
#                 cr_unable.append(d['start_date'])
#         if not len(existcr):
#             return True,cr_able,cr_unable
#         else:
#             return False,cr_able,cr_unable
#     else:
#         # print('====date_dic====')
#         # print(date_dic)
#         ready,cr = getCR(start_end_year,existcr)
#         # if len(cr) == 0:
#         #     print('KOSONGSSS')
#         # else:
#         #     print('TAK KOSONGSSS')
#         #     print(cr)
#         # print('CR IN CHECKREADY: ',cr)
#         cr_start = {'cr':cr,'date':start_end_year['start_date']}
#         cr_able.append(cr_start)
#         # print('CR-DATE')
#         # print(cr_date)
#         if ready:
#             return True,cr_able,''
#         else:
#             return False,cr_able,''

# def handleError(cr):
#     # print('CR:')
#     # print(cr)
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
#             print('year: ',row[0])
#             print('account: ',row[1])
#             print('postingdate: ',row[30])
#             print('group: ',row[31])
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
#         # print('error_list: ',error_list)
#         return False,error_list
#     else:
#         print('errors: ',errors)
#         for p in error_list:
#             print(p)
#         return True,error_list

# def createCSV(cr,errordate):
#     path = 'collection_report'
#     pathtofile = path+'/Error_Log_'+ str(errordate)
#     filename = 'Error_Log_' + str(errordate)

#     if os.path.exists(path):
#         with open(pathtofile,'w') as file:
#             writer = csv.writer(file)
#             # for row in cr:
#             #     # row_content = ''
#             #     # print('rorr: ',row)
#             #     # for r in row:
#             #     row_content = ','.join(row)
#             #     # print('row content: ',row_content)
#             #     writer.writerow(row_content)
#             row1 = ['ahmad','1','2']
#             row2 = ['abu','3','4']
#             rows = [row1,row2]
#             # for row in rows:
#             #     for r in row:

#             writer.writerows(rows)
#             # myss = ''
#             # myss2 = []
#             # for row in cr:
#             #     mys = ''
#             #     for r in row:
#             #         mys = ','.join(str(r))
#             #         print('mys: ',mys)
#             #         myss2.append(mys)
#             #     myss = myss.join(mys)
#             #     print('myss: ',myss)
#             # writer.writerows(myss)
#             print('Successfully created CSV file')
#     # else:
#     #     os.makedirs(path)
#     #     with open(pathtofile,'w') as file:
#     #         writer = csv.writer(file)
#     #         for row in cr:
#     #             writer.writerow(row)
#     #         # writer.writerows(cr)
#     #         print('Successfully created CSV file')
    
#     with open(pathtofile,'r') as file:
#         filedata = csv.reader(file)
#         # print('filedatasss: ',filedata)
#         # for r in filedata:
#         #     print('row: ',r)
#         # file_url = upload(filename,file.read(),)
#     return pathtofile, filename, filedata,cr

def createErrorLog(much,error_list,errordate):
    errordate = errordate[:10]
    errordate = datetime.strptime(errordate,'%Y-%m-%d')
    errordate = errordate.date()
    errorlog = frappe.new_doc('Collection Journal Entry Error Log')
    errorlog.date = datetime.now().date()
    errorlog.collection_report_date = errordate
    errorlog.start_date = errordate
    errordate_str = errordate.strftime('%Y-%m-%d')
    for e in error_list:
        errorlog.append('error_list',{
            'row':e['row'],
            'field':e['field'],
            'value':e['val'],
            'description':e['desc']
        })
    errorlog.save()
    print('name:: ',errorlog.name)
    # domain = 'http://175.136.236.153:8003' + '/app/journal-entry-error-log/'+ errorlog.name
    # domain = 'http://127.0.0.1:8000' + '/app/journal-entry-error-log/'+ errorlog.name
    domains = domain + '/app/collection-journal-entry-error-log/'+ errorlog.name
    error_link = "<a href='"+domains+"' target='_blank'>Error Log "+str(errordate_str)+"</a>"
    msg = 'A Collection Journal Entry Error Log has been made for Collection Report '+str(errordate)+'. Please see here '+error_link
    title = 'ERPNext: Collection Journal Entry Error Log '+str(errordate)
    sendEmail(msg,title,errorlog.doctype,errorlog.name)
    # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
    # email_args = {
    #     'recipients':user1.email,
    #     'message':msg,
    #     'subject':title,
    #     'reference_doctype':errorlog.doctype,
    #     'reference_name':errorlog.name
    # }
    # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)

    # user1 = frappe.get_last_doc('User',filters={'username':'kt'})
    # email_args = {
    #     'recipients':user1.email,
    #     'message':msg,
    #     'subject':title,
    #     'reference_doctype':errorlog.doctype,
    #     'reference_name':errorlog.name
    # }
    # frappe.enqueue(method=frappe.sendmail, queue='shoPRINT('FILENAMErt',timeout='300',**email_args)
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

# def getIsoDate(crdate):
# 	start_date = crdate['start_date']
# 	end_date = crdate['end_date']
# 	year = start_date.year
# 	times = time(0,0,0)
# 	start_date = datetime.combine(start_date,times)
# 	end_date = datetime.combine(end_date,times)
# 	# print('------type: ',type(start_date))
# 	start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
# 	start_date = start_date.isoformat()+"Z"
# 	# print('++++++++++++++STARTDATE')
# 	# print(start_date)
# 	end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
# 	end_date = end_date.isoformat()+"Z"

# 	return start_date, end_date, year

# def getDateString(dates):
#     if not isinstance(dates, str):
#         dates = dates.strftime('%Y-%m-%d')
#     return dates

# def getDateOnly(start_date):
#     date_only = start_date[:10]
#     new_date = datetime.strptime(date_only,'%Y-%m-%d')
#     return new_date

# def getTitleName(posting_date):
#     # if isinstance(posting_date, str):
#     #    posting_date = datetime.strptime(posting_date, '%Y-%m-%d') 
#     # month = posting_date.strftime('%B')
#     # year = posting_date.year

#     if not isinstance(posting_date,str):
#         posting_date = posting_date.strftime('%Y-%m-%d')

#     # title = 'Collection - ' + month +' '+ str(year)
#     title = 'Collection - ' + posting_date
#     return title

# def createJE(cr,start_date,batch_id):
#     journal = frappe.new_doc("Journal Entry")
#     posting_date = ''

#     if not len(cr):
#         now = datetime.now().strftime('%Y-%m-%d')
#         # new_date = datetime.strptime(now, '%Y-%m-%d').date() + timedelta(days=1)
#         # journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         tag_id = getDateOnly(start_date)
#         tag_id_str = tag_id.strftime('%Y-%m-%d')
#         journal.tag_id = tag_id
#         journal.title = getTitleName(tag_id)
#         journal.posting_date = tag_id
#         journal.save()
#         journal.submit()
#         je_name = journal.name
#         return je_name,''
#     else:
#         counter = 1
#         for row in cr:
#             # debit
#             print('ROW')
#             # print(row)
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
#                     'cost_center_number':cost_center_number,
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
#                     'cost_center_number':cost_center_number,
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
#         # journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         # journal.posting_date = now
#         journal.posting_date = posting_date
#         tag_id = getDateOnly(start_date)
#         tag_id_str = tag_id.strftime('%Y-%m-%d')
#         # journal.tag_id = tag_id
#         journal.tag_id = batch_id

#         # journal.title = getTitleName(posting_date)
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
#         # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
#         # email_args = {
#         #     'recipients':user1.email,
#         #     'message':msg,
#         #     'subject':title,
#         #     'reference_doctype':journal.doctype,
#         #     'reference_name':journal.name
#         # }
#         # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)


#         return je_name,journal_link

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

    # print('batchid after save: ',journal.tag_id)
    # createDeferredAccountingEntries(journal,date(year=2023,month=2,day=28))
    # createBillingAccountingEntries(journal)
    # dates = cr[0][30]

    je_name = journal.name
    domains = domain + '/app/journal-entry/'+ je_name
    journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+getDateString(end_date)+"</a>"
    # msg = 'A Collection journal entry has been created for Collection Report '+str(posting_date)+'. Please see here '+journal_link
    # title = 'ERPNext: Collection Journal Entry '+str(posting_date)
    # sendEmail(msg,title,journal.doctype,journal.name)

    return je_name,journal_link


def sendEmail(msg,subject,doctype,name):
    userlist = []
    users = frappe.get_all('User')
    for user in users:
        u = frappe.get_last_doc('User',filters={'name':user.name})
        rolelist = u.roles
        if rolelist:
            for r in rolelist:
                if r.role == 'IWK User':
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

def getBatchID(filename):
    split = filename.split('_')
    # print('split: ',split)
    batchid = split[0]
    print('batchid: ',batchid)
    return batchid

# latest
# def importfrombs(start_date,end_date,file):
#     print('yes1')
#     batch_id = getBatchID(file.file_name)
#     much = False
#     if start_date != end_date:
#         much = True
#         ready,cr_able,cr_unable = checkReadyCR(much,start_date,end_date)
#     else:
#         much = False
#         # ready,cr_able,cr_unable = checkReadyCR(much,start_date,end_date)
#         ready = True
#         # print('1')
#         print('yes2')
#         # if start_date == date(day=31,month=12,year=2022):
#         #     file = frappe.get_last_doc('File',filters={'file_name':'CollectionReport (1).csv'})
#         #     print('yes')
#         # else:
#         #     file = frappe.get_last_doc('File',filters={'file_name':'11_CollectionReport.csv'})
#         # print('2')
#         attach_csv = file.file_url
#         # print('3')
#         site = frappe.utils.get_site_path()
#         # print('4')
#         split = site.split('/')
#         site = split[1]
#         attach_csv = site+attach_csv
#         cr_able = []
#         now = datetime.now().date()
#         # print('5')
#         with open(attach_csv,'r') as file:
#             print('6')
#             reader = csv.reader(file)
#             # print('reader')
#             # print(reader)
#             for r in reader:
#                 # print('row: ',r)
#                 r[30] = now
#                 cr_able.append(r)
#             # print('8')
#         # print('CR ABLE: ',cr_able)
#         print('length cr able: ',len(cr_able))

#     # much,exist,cr_able,cr_unable = checkReadyCR(start_date,end_date)
#     error_log_name_list = []
#     journal_entry_name_list = []
#     # journal_entry_link = []
#     if not much:
#         print('READY: ',ready)
#         # cr = cr_able[0]['cr']   # real punya
#         cr = cr_able
#         # empty_cr = False
#         # if not len(cr):
#         #     empty_cr = True
#         # if empty_cr:
#         #     createJE(cr,cr_date)
#         # else:
#         # cr_date = cr_able[0]['date']        # real punya
#         cr_date = start_date
#         if ready:
#             # print('------------cr------------')
#             # print(cr_able)
#             error_result, error_list = handleError(cr)
#             print('ERROR RESULT: ',error_result)
#             # print('ERROR LIST: ', error_list)
#             cr_dates = cr_date.strftime('%Y-%m-%d %H-%m-%s')
#             if error_result == True:
#                 error_link,error_name = createErrorLog(False,error_list,cr_dates)
#                 error_log_name_list.append(error_name)
#                 frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
#                 return False,error_log_name_list
#             else:
#                 journal_name, journal_link = createJE(cr,cr_dates,batch_id)
#                 journal_entry_name_list.append(journal_name)
#                 frappe.msgprint('One Journal Entry has been created, See Here '+journal_link)
#                 return True,journal_entry_name_list
#         else:
#             raise Exception('Collection Report Is Not Available Yet.')
#     else:
#         if not ready:
#             unable_list = ''
#             for un in cr_unable:
#                 unable_list += un+', '
#             raise Exception('The Following(s) Collection Report Is Not Available Yet : ',unable_list)
#         if ready:   
#             error_log_link_list = []
#             error_lists = []
#             error_exist = False
#             # print('///////cr able')
#             # print(cr_able)
#             for c in cr_able:
#                 error_result, error_list = handleError(c['cr'])
#                 print('C[CR]')
#                 # print(c['cr'])
#                 if error_result:
#                     error_exist = True
#                     error_item = {'error_list':error_list,'date':c['date']}
#                     error_lists.append(error_item)
            
#             if error_exist:
#                 for e in error_lists:
#                     error_link,error_name = createErrorLog(True,e['error_list'],e['date'])
#                     error_log_link_list.append(error_link)
#                     error_log_name_list.append(error_name)
#                 error_links = ''
#                 for n in error_log_link_list:
#                     error_links += n +', '
                
#                 frappe.msgprint('There is error(s) when trying to import the Collection Report. No Journal Entry is created. You can see the list of the errors here '+error_links)
#                 return False,error_log_name_list
#             # return False,''
#             else:
#                 journal_links = ''
#                 for cr in cr_able:
#                     journal_name, journal_link = createJE(cr['cr'],cr['date'],batch_id)
#                     journal_entry_name_list.append(journal_name)
#                     journal_links += journal_link+', '

#                 frappe.msgprint('Journal Entries has been created, See Here '+journal_links)
#                 return True,journal_entry_name_list

#     # error_result, error_list = handleError(cr)
#     # print('error result: ',error_result)
#     # if error_result == True:
#     #     createErrorLog(error_list,cr,datetime.now().date())
#     # else:
#     #     createJE(cr)

def checkJEExist(start_date, end_date,file):
    batch_id = getBatchID(file.file_name)
    print('batch_id: ',batch_id)
    start_year = start_date.year
    end_year = end_date.year
    report_exist = []
    journal_link_list = []
    if start_year != end_year:
        raise Exception('Start Date and End Date Must Be In The Same Year')
    
    if start_date == end_date:
        try:
            je = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','tag_id':batch_id})
            print('JE START DATE: ',start_date)
            print('JE TAG IDS: ',type(je.tag_id))
            # tag_id = je.tag_id.strftime('%Y-%m-%d')
            # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
            # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je.name
            domains = domain + '/app/journal-entry/'+ je.name
            # journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+tag_id+"</a>"
            journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+getDateString(start_date)+"</a>"
            journal_link_list.append(journal_link)
            # frappe.throw('Journal Entry already exist!')
            return True, journal_link_list
            # raise Exception('Journal Entry already existgfgth!')
        except Exception as e:
            # report_exist.append(str(start_date))
            print('exception at checkjeexist: ',e)
            pass
    else:
        diff = end_date - start_date
        diff_day = diff.days + 1
        start_day = start_date.day - 1
        year = start_year
        month = start_date.month
		# print('startdaate: ',start_date)
        # report_exist = []

        for i in range(diff_day):
            start_day += 1
            new_date = date(year,month,start_day)
            try:
                je = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','tag_id':batch_id})
                report_exist.append(str(new_date))
                # tag_id = je.tag_id.strftime('%Y-%m-%d')
                # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
                # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je.name
                domains = domain + '/app/journal-entry/'+ je.name
                # journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+tag_id+"</a>"
                journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+getDateString(batch_id)+"</a>"
                journal_link_list.append(journal_link)
            except:
                pass
        
        length = len(report_exist)
        if length != 0:
            # warning = ''
            # for i in range(length):
            #     warning += report_exist[i]+', '
            #     if length > 1:
            #         raise Exception('Following Journal Entries Already Exists: '+warning)
            #     else:
            #         raise Exception('This Journal Entry Already Exists: '+warning)
            return True,journal_link_list
    return False,''


# def importfrombs(start_date,end_date):
# 	print('------------------------------IMPORTFROMBS----------------------------------------')
# 	# Get the Token from BS
# 	year = end_date.year
# 	start_date_report = start_date.isoformat()+"Z"
# 	end_date_report = end_date + timedelta(hours=23,minutes=59,seconds=59)
# 	end_date_report = end_date.isoformat()+"Z"

# 	report = getReportCR(start_date_report,end_date_report,year)
# 	textt = report.content.decode('utf-8')
# 	cr = csv.reader(textt.splitlines(), delimiter=',')
# 	cr = list(cr)
# 	# print('cr: ')
# 	# print(cr)
# 	# error_log = frappe.new_doc('Journal Entry Error Log')

# 	error,row_lists,error_log_name, tagging_sync, tagging_unsync = checkJEError(cr,start_date,end_date)
# 	print('error: ',error)
# 	print('row list: ---------')
# 	print(row_lists)
# 	if error:
# 		# error_log = frappe.get_last_doc('Journal Entry Error Log', filters={'name':error_log_name})
# 		domain = 'http://175.136.236.153:8003' + '/app/journal-entry-error-log/'+ error_log_name
# 		error_link = "<a href='"+domain+"' target='_blank'>Error Log</a>"
# 		frappe.msgprint("There is error(s) in Collection Report. See here <a href='"+domain+"' target='_blank'>Error Log</a>")
# 	if row_lists != '':
# 		createJE(row_lists,start_date,end_date)

# 	return True
# 	# else:
# 	# 	# frappe.throw('testtesttest123456')
# 	# 	frappe.msgprint('There is error(s) in Collection Report.')
# 	# 	return False



# def checkJEError(cr,start_date,end_date):
# 	counter = 1
# 	row_counter = 0
# 	error = False
# 	error_count= 0
# 	error_log = frappe.new_doc('Journal Entry Error Log')
# 	error_log.start_date = start_date
# 	print('start_date: ',start_date)
# 	error_log.end_date = end_date
# 	row_lists = []
# 	# tagging_number_sync = []
# 	# tagging_number_unsync = []

# 	for row in cr:
# 		# debit
# 		if counter == 1:
# 			counter+=1
# 			row_counter+=1

# 			year = row[1]
# 			debit_account_number = row[2]
# 			cost_center_number = row[3]
# 			currency = row[12]
# 			debit = row[15]
# 			remark = row[23]
# 			posting_date = row[30]
# 			group = row[31]
# 			tagging_number = row[33]
# 			# tagging = {'tagNumber':tagging_number}

# 			row_list = {
# 				"Year":year,
# 				"Debit Account Number":debit_account_number,
# 				"Cost Center Number":cost_center_number,
# 				"Currency":currency,
# 				"Debit":debit,
# 				"Remark":remark,
# 				"Posting Date":posting_date,
# 				"Group":group
# 			}
			
# 			error_list = {}
# 			error_return,error_list = checkValueEmpty(row_list,row_counter)
			
# 			print('error_list: ',error_list)

# 			if error_return:
# 				if not error:
# 					error = True
# 					error_count += 1
# 				elif error:
# 					error_count += 1
# 				# tagging_number_unsync.append(tagging)
# 				for e in error_list:
# 					error_log.append('error_list',e)
# 			else:
# 				row_lists.append(row_list)
# 				# tagging_number_sync.append(tagging)
				
				
# 		# credit
# 		elif counter == 2:
# 			counter = 1
# 			row_counter+=1
# 			year = row[1]
# 			credit_account_number = row[2]
# 			cost_center_number = row[3]
# 			currency = row[12]
# 			credit = row[15]
# 			remark = row[23]
# 			posting_date = row[30]
# 			group = row[31]

# 			# if not credit_account_number or not cost_center_number:
# 			# 	continue

# 			row_list = {
# 				"Year":year,
# 				"Credit Account Number":credit_account_number,
# 				"Cost Center Number":cost_center_number,
# 				"Currency":currency,
# 				"Credit":credit,
# 				"Remark":remark,
# 				"Posting Date":posting_date,
# 				"Group":group
# 			}
			
# 			error_list = {}
# 			error_return,error_list = checkValueEmpty(row_list,row_counter)
# 			print('error_list: ',error_list)

# 			if error_return:
# 				if not error:
# 					error = True
# 					error_count += 1
# 				elif error:
# 					error_count += 1
# 				# tagging_number_unsync.append(tagging)
# 				for e in error_list:
# 					error_log.append('error_list',e)
# 			else:
# 				row_lists.append(row_list)
# 				# tagging_number_sync.append(tagging)
			
# 	if error:
# 		error_log.save()
# 		error_log.submit()
# 		# print('error_log name: ',error_log.name)
# 		# raise Exception("There is error in Collection Report, Please refer to this Error Log here.")
# 		# return True, row_lists, error_log.name, tagging_number_sync, tagging_number_unsync
# 		return True, row_lists, error_log.name
# 	else:
# 		# return False, row_lists, '', tagging_number_sync, tagging_number_unsync
# 		return False, row_lists, ''


# def checkValueEmpty(row_list,row_counter):
# 	error_list = []
# 	error = False
# 	for k,v in row_list.items():
# 		# print('k,v')
# 		if v == '':
# 			error_content = {
# 				'row':row_counter,
# 				'field':k,
# 				'description':'Missing Data'
# 			}
# 			error_list.append(error_content)
# 			# error_log.append('error_list',{
# 			# 	'row':row_counter,
# 			# 	'field':k,
# 			# 	'description':'Missing Data'
# 			# })
# 			if not error:
# 				error = True

# 	return error,error_list


# def createJE(row_lists,start_date,end_date):
# 	print('-------------------------------------------CREATEJE--------------------------------')
# 	journal = frappe.new_doc("Journal Entry")
# 	counter = 1
# 	print('row_lists: ')
# 	print(row_lists)
# 	posting_date = ''
# 	group = ''

# 	for row in row_lists:
# 		# debit
# 		if counter == 1:
# 			counter+=1
# 			# print('row_list in createJE------------')
# 			# print(row)
# 			posting_date = row['Posting Date']
# 			group = row['Group']
# 			print('row------')
# 			print(row)

# 			# year = row[1]
# 			# debit_account_number = row[2]
# 			# cost_center_number = row[3]
# 			# currency = row[12]
# 			# debit = row[15]
# 			# remark = row[23]
# 			# posting_date = row[30]
# 			# group = row[31]
				
# 			# print('debit acc_number: ',debit_account_number)
# 			debit_acc = frappe.get_last_doc("Account", filters={"account_number":row['Debit Account Number']})
# 			cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['Cost Center Number']})
			

# 			journal.append('accounts',{
# 				'account':debit_acc.name,
# 				'account_number':debit_acc.account_number,
# 				'cost_center':cost_center.name,
# 				'currency':row['Currency'],
# 				'debit_in_account_currency' : float(row['Debit']),
# 				'credit_in_account_currency' : float(0),
# 				'remark':row['Remark'],
# 				'group':row['Group'],
# 				'year': row['Year']
# 			})

# 		# credit
# 		elif counter == 2:
# 			counter = 1
# 			posting_date = row['Posting Date']
# 			group = row['Group']
# 			print('row------')
# 			print(row)
# 			# year = row[1]
# 			# credit_account_number = row[2]
# 			# # print('credit_account_number: ',credit_account_number)
# 			# cost_center_number = row[3]
# 			# currency = row[12]
# 			# credit = row[15]
# 			# remark = row[23]
# 			# posting_date = row[30]
# 			# group = row[31]

# 			# if not credit_account_number or not cost_center_number:
# 			# 	continue

# 			# row_list = {
# 			# 	"year":year,
# 			# 	"credit account number":credit_account_number,
# 			# 	"cost center number":cost_center_number,
# 			# 	"currency":currency,
# 			# 	"debit":debit,
# 			# 	"remark":remark,
# 			# 	"posting_data":posting_date,
# 			# 	"group":group
# 			# }

# 			# if credit_account_number == '' or cost_center_number == '':
# 			# 	continue
			
# 			# print('credit_account_number: ',credit_account_number)
# 			credit_acc = frappe.get_last_doc("Account", filters={"account_number":row['Credit Account Number']})
# 			# print('credit acc name: ',credit_acc.name)
# 			cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['Cost Center Number']})
			
# 			journal.append('accounts',{
# 				'account':credit_acc.name,
# 				'account_number':credit_acc.account_number,
# 				'cost_center':cost_center.name,
# 				'currency':row['Currency'],
# 				'debit_in_account_currency' : float(0),
# 				'credit_in_account_currency' : abs(float(row['Credit'])),
# 				'remark':row['Remark'],
# 				'group':row['Group'],
# 				'year': row['Year']
# 			})

# 	now = datetime.now().date()
# 	journal.entry_type = "Journal Entry"
# 	print('posting_date: ',posting_date)
# 	print('group: ',group)
# 	new_date = datetime.strptime(posting_date, '%Y-%m-%d').date() + timedelta(days=1)
# 	journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
# 	journal.save()
# 	journal.submit()


def getoptionlist():
	doc_field = frappe.get_doc("DocField",{"fieldname":"type","parent":"Journal Entry Error Log","fieldtype":"Select"})

	# option_string = get_field_options("type","Journal Entry Error Log")
	# options = option_string.split("\n")
	# options = doc_field.split("\n")
	options = doc_field.options.split("\n")
	# print('docfield:')
	# print(doc_field.name)
	# print('options: ',options[0])


def getReportCR(start_date, end_date, year):
	reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextMthEndJob'})
	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
	reqUrl = reportcr.url +reportcr.api_key
	print('reqURL: ',reqUrl)

	payload = json.dumps({
	# "startDate": "2022-12-01T08:19:50.970Z",
	# "endDate": "2022-12-22T08:19:50.970Z",
	"startDate": start_date,
	"endDate": end_date,
	"name": "string",
	"year": year,
	"isErpNext":True
	}, default=str)

	headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json" 
    }

	response = requests.request("POST", reqUrl, data=payload, headers=headersList)

	headers = response.headers
	msg = headers.get('return-message')
	if 'filename=string.csv' not in msg:
		raise Exception('The file you are trying to get is not in CSV format. Please try again later.')

	# print('type text:',type(response.text))
	# print('text: ',response.text)
	# print('response: ',response)
	return response

def sendTagging(tagging_sync):
	tagging_api = frappe.get_last_doc('API Key', filters={'name':'ERPNextUpdateTagNumber'})
	reqUrl = tagging_api.url +tagging_api.api_key
	print('reqURL: ',reqUrl)

	payload = json.dumps(tagging_sync, default=str)
	headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json" 
    }

	requests.request("POST", reqUrl, data=payload, headers=headersList)

# def getDomain():
# 	# domain = frappe.get_request_host()
# 	# domain = requests.META['HTTP_HOST']
# 	# domain = socket.getfqdn()
# 	# domain = frappe.local.site
# 	# domain = frappe.get_request_header("Host")
# 	# domain = frappe.get_url()
# 	domain = frappe.request.host
# 	print('domain: ',domain)

def createTaggingObject():
	year = 2023
	start_date_report = "2023-01-01T00:00:00.00Z"
	# end_date_report = end_date + timedelta(hours=23,minutes=59,seconds=59)
	end_date_report = "2023-01-31T00:00:00.00Z"

	report = getReportCR(start_date_report,end_date_report,year)
	textt = report.content.decode('utf-8')
	cr = csv.reader(textt.splitlines(), delimiter=',')
	cr = list(cr)

	tagging_number_sync = []
	counter = 1
	for row in cr:
		# debit
		if counter == 1:
			counter+=1

			tagging_number = row[33]
			tagging = {'tagNumber':tagging_number, 'synced': True}
			tagging_number_sync.append(tagging)

		elif counter == 2:
			counter = 1

			tagging_number = row[33]
			tagging = {'tagNumber':tagging_number, 'synced': True}
			tagging_number_sync.append(tagging)
	
	print('tagging object')
	print(tagging_number_sync)
	return tagging_number_sync


def getReportTest():
	reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextMthEndJob'})
	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
	reqUrl = reportcr.url +reportcr.api_key
	print('reqURL: ',reqUrl)

	payload = json.dumps({
	# "startDate": "2022-12-01T08:19:50.970Z",
	# "endDate": "2022-12-22T08:19:50.970Z",
	"startDate": '2023-01-01T00:00:00.00Z',
	"endDate": '2023-01-01T23:59:59.00Z',
	"name": "string",
	"year": 2023,
	"isErpNext":True
	}, default=str)

	headersList = {
    "Accept": "*/*",
    "Content-Type": "application/json" 
    }

	response = requests.request("POST", reqUrl, data=payload, headers=headersList)

	headers = response.headers
	msg = headers.get('return-message')
	if 'filename=string.csv' in msg:
		print('yes')
		# print(msg)

	# print('type text:',type(response.text))
	# print('text: ',response.text)
	# print('response: ',response)
	return response


