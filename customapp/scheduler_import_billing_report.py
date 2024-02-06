import frappe
from datetime import datetime, time, date, timedelta
import os, csv, json, calendar, time,zipfile,io,requests
from customapp.general_function import *

# def changeTemplate(cr,new_date):
#     site = getSite()
#     path = site+'/private/files/'
#     filename = 'string(15) perfect data.csv'
#     # date_name = getDateOnly(start_date)
#     # print('DATE NAME -------------------: ',date_name)
#     pathtofile = path+filename

#     for row in cr:
#         row[30] = new_date

#     if os.path.exists(path):
#         with open(pathtofile,'w',newline='') as file:
#             writer = csv.writer(file)
#             for row in cr:
#                 print('row: ',row)
#                 writer.writerow(row)
#             print('done1')
#     else:
#         os.makedirs(path)
#         with open(pathtofile,'w',newline='') as file:
#             writer = csv.writer(file)
#             for row in cr:
#                 print('row: ',row)
#                 writer.writerow(row)
#             print('done2')

# def makeDict(row,counter):
#     # print('counter: ',counter,' val: ',row[15])
#     dicts = {
#         # 'account':acc,
#         'year': row[1],
#         'account_number':row[2],
#         # 'cost_center': cost,
#         'cost_center_number': row[3],
#         'currency': row[12],
#         'remark': row[23],
#         'posting_date': row[30],
#         'group': row[31],
#         'tax_amount': row[32],
#         'tax_code': row[33],
#         'profit_or_cost_center_number': row[34],
#         'san_count': row[35],
#         'monthly_charge': row[36],
#         'month_count': row[37],
#         'current_month': row[38],
#     }
#     try:
#         dicts['revenue_account'] = row[39]
#     except:
#         # dicts['revenue_account'] = 0
#         pass
#     # debit
#     if counter == 1:
#         # acc = frappe.get_last_doc('Account',filters={'account_number'}:row[1])
#         # cost = frappe.get_last_doc('Cost Center', filters={'cost_Center_number':row[3]})
#         dicts['debit'] = abs(float(row[15]))
#     elif counter == 2:
#         dicts['credit'] = abs(float(row[15]))
    
#     return dicts

# def getDict(cr):
#     dict_list = []
#     counter = 1     # 1 for debit, 2 for credit
#     counters = 0    # 0 for next pair, 1 for current pair
#     seq = 0         # 0 for 1st partner, 1 for 2nd partner
#     for r in cr:
#         if counters == 0:
#             if float(r[15]) > 0:
#                 counter = 1
#             else:
#                 counter = 2
#             seq = 1
#             counters = 1
#         if counters == 1:
#             if counter == 1 and seq != 3:
#                 # for debit
#                 new_row = makeDict(r,counter)
#                 # print('1')
#                 counter = 2

#             elif counter == 2 and seq != 3:
#                 # for credit
#                 new_row = makeDict(r,counter)
#                 # print('2')
#                 counter = 1
#             dict_list.append(new_row)
#         seq += 1
#         if seq == 3:
#             seq = 0
#             counters = 0
#     # for l in dict_list:
#     #     try:
#     #         print('debit-- ',l['debit'])
#     #         # print(l['debit'])
#     #     except:
#     #         print('credit-- ',l['credit'])
#     #         # print(l['credit'])
#     return dict_list

# def getCr(filename):
#     print('filename in getcr: ',filename)
#     file = frappe.get_last_doc('File', filters={'file_name':filename})
#     file_url = file.file_url

#     # print(file_url)
#     site = frappe.utils.get_site_path()
#     split = site.split('/')
#     site = split[1]
#     file_path = site+file_url
#     cr = []
#     with open(file_path,'r') as file:
#         reader = csv.reader(file)
#         # print('reader')
#         # print(reader)
#         for r in reader:
#             # print('row: ',r)
#             cr.append(r)

#     cr_dict = getDict(cr)
#     return cr_dict,cr

# def getCrString15(template,new_date):
#     str_date = getDateString(new_date)
#     if not template:
#         new_date = '2023-03-31'
#     file_name = 'string(15) perfect data.csv'
#     cr_dict,cr = getCr(file_name)
#     changeTemplate(cr,str_date)
#     return cr_dict

# def getDateString(dates):
#     if not isinstance(dates, str):
#         dates = dates.strftime('%Y-%m-%d')
#     return dates

# def getSite():
#     site = frappe.utils.get_site_path()
#     split = site.split('/')
#     site = split[1]
#     return site

# def getNextDate(dates):
#     month = dates.month
#     year = dates.year
#     month += 1
#     if month == 13:
#         month = 1
#         year += 1
#     days = calendar.monthrange(year=year,month=month)
#     next_date = date(year=year,month=month,day=days[1])
#     return next_date

# def getPreviousDate(dates):
#     if isinstance(dates, str):
#         dates = datetime.strptime(dates,'%Y-%m-%d')
    
#     month = dates.month
#     year = dates.year
#     month-=1
#     if month <= 0:
#         month = 12
#         year -=1
#     days = calendar.monthrange(year,month)
#     prev_date = date(day=days[1],month=month,year=year)
#     return prev_date

def checkFile(cr_dict,cr,batch_id,new_date):
        date_str = getDateString(new_date)
        doc_name = 'Billing - '+date_str
        print('date string: ',date_str)
        print('batch id in checkfile: ',batch_id)
        return_dict = {'doc_name':doc_name,'new_posting_date':new_date,'cr_dict':cr_dict,'batch_id':batch_id}
        try:
            return_dict['cr_list'] = cr
        except:
            pass
        return return_dict

# def test():
#     test = False
#     # try:
#     #     doc = frappe.get_list('testdoctype2')
#     #     test = True
#     # except:
#     #     return
#     doc = frappe.get_list('testdoctype2')

#     if doc:
#         print('doc: ',doc)
#         for p in doc:
#             # docc = frappe.get_last_doc('testdoctype2',filters={'name':p['name']})
#             # print('name: ',docc.name1)
#             print('name: ',p.name)
#     else:
#         print('no')

# def getPostingDate(cr):
#     i = 0
#     for p in cr:
#         i += 1
#         print(i,': ',p)
#     posting_date = getDateOnly(cr[30])
#     print('Posting Date: ',posting_date)
#     return posting_date

# def getMonthName(name):
#     split = name.split(' ')
#     # print('name: ',split[2])
#     month = datetime.strptime(split[2],'%B').month
#     # print('month: ',month)
#     return month

# def getMonthNumber(month):
#     month = datetime.strptime(month, '%B').month
#     return month

# def doCalculate(row,f1):
#     # print('--row--: ',row)
#     # print('LENGTH: ',len(row))
#     # print('---row: ',row['month_count'])
#     # print('---type: ',type(row['month_count']))
#     # print('month count 1: ',row['month_count'])
#     # month_count = 1
#     if f1 == 1:
#         month_count = int(row['month_count']) - 1
#     else:
#         month_count = 1
#     row['month_count']  = month_count
#     # print('=month count: ',month_count)
#     # print('=row ',row['month_count'])
#     # print('month count 2: ',row['month_count'])
#     deferred_revenue = month_count*int(row['monthly_charge'])*int(row['san_count'])
#     # print('month count: ',month_count)
#     return deferred_revenue

# def doLogicDeferred(alist):
#     dje_list = alist.copy()
#     # new_list = [] # accounting entries that needed to be added to JE last month
#     update_list = []
#     counter = 1
#     revenue_counter = 0
#     # row_1 = {}
#     # row_2 = {}
#     # print('djelist: ',dje_list)
#     # for row in dje_list:
#         # print('row length: ',len(row))
#         # print(row)
#     # print('length: ',len(dje_list))
#     print('-----dje listsss: ')
#     print(dje_list)

#     for row in dje_list:
#         # if revenue_counter == 0:
#         if counter == 1:
#             counter += 1
#             deferred_revenue = doCalculate(row,1)
#             row['debit_in_account_currency'] = deferred_revenue
#             account = frappe.get_last_doc('Account',filters={'account_number':row['account_number']})
#             row['account'] = account.name
#             cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row['cost_center_number']})
#             row['cost_center'] = cost_center.name
#             update_list.append(row)
#         elif counter == 2:
#             counter = 1
#             revenue_counter += 1
#             deferred_revenue = doCalculate(row,1)
#             row['credit_in_account_currency'] = deferred_revenue
#             account = frappe.get_last_doc('Account',filters={'account_number':row['account_number']})
#             row['account'] = account.name
#             cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row['cost_center_number']})
#             row['cost_center'] = cost_center.name
#             update_list.append(row)
    
#     # for l in update_list:
#     #     print('-',l['month_count'])
#         # print(l)

#     # for l in update_list:
#     #     print(l['debit_in_account_currency'],' ',l['credit_in_account_currency'],' ',l['month_count'])
#     #     print(l)
#     # print('update')
#     # for p in update_list:
#     #     print(p['month_count'])
#     # print('update_list')
#     print('update')
#     # for p in update_list:
#     #     print('--------------- ',p['month_count'])
#     return update_list

def doLogicRevenue(dje_list):
    new_list = [] # accounting entries that needed to be added to JE last month
    update_list = []
    counter = 1
    revenue_counter = 0
    row1 = {}
    row2 = {}

    for row in dje_list:
        alist = []
        if revenue_counter == 0:
            if counter == 1:
                counter += 1
                row1 = row.copy()
                deferred_revenue2 = doCalculate(row1,2)
                row1['debit_in_account_currency'] = deferred_revenue2
                row1['credit_in_account_currency'] = 0
            elif counter == 2:
                counter = 1
                row2 = row.copy()
                deferred_revenue2 = doCalculate(row2,2)
                row2['debit_in_account_currency'] = 0
                row2['credit_in_account_currency'] = deferred_revenue2
                revenue_counter = 1
        if revenue_counter == 1:
            revenue_counter = 0
            row1['account_number'] = row2['account_number']
            row1['account'] = row2['account']
            row1['cost_center_number'] = row2['cost_center_number']
            row1['cost_center'] = row2['cost_center']
            row2['revenue_account'] = None
            row2['account_number'] = row1['revenue_account']
            # print('acc: ',row_2['account_number'])
            # print('acc: ',row_1['account_number'])
            # print('acc ',row_1['revenue_account'])
            # print(row_2)
            print('---------------row2 acc: ',row2['account_number'])
            print('---row2 ',row2)
            acc = frappe.get_last_doc('Account',filters={'account_number':row2['account_number']})
            row2['account'] = acc.name
            row1['month_count'] = 1
            row2['month_count'] = 1

            new_list.append(row1)
            new_list.append(row2)
    return new_list

# def convertToDict(dje):
#     new_list = []
#     for row in dje:
#         rows_dicts = {
#             'account':row.account_number,
#             'account_number':row.account_number,
#             'cost_center':row.cost_center,
#             'cost_center_number':row.cost_center_number,
#             # 'cost_center':row.cost_center.name,
#             'currency':row.currency,
#             'debit_in_account_currency' : row.credit,
#             'credit_in_account_currency' : row.credit,
#             'remark':row.remark,
#             'group':row.group,
#             'year': row.year,
#             'posting_date':row.posting_date,
#             'tax_amount':row.tax_amount,
#             'tax_code':row.tax_code,
#             'second_cost_center_number':row.second_cost_center_number,
#             'san_count':row.san_count,
#             'monthly_charge':row.monthly_charge,
#             'month_count':row.month_count,
#             'current_month':row.current_month,
#             'revenue_account':row.revenue_account
#         }
#         new_list.append(rows_dicts)
#     return new_list

# def getBatchID(filename):
#     split = filename.split('_')
#     # print('split: ',split)
#     batchid = split[0]
#     print('batchid: ',batchid)
#     return batchid

def doImportBillingReportSingle(file,cr_dict,cr,batch_id,new_date):
    global domain
    # domain = 'http://127.0.0.1:8000'
    # # domain = 'http://175.136.236.153:8003'
    domain = getDomain()
    
    # doUAT()
    # scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing Report'})
    # if scheduler.control == 'Stop':
    #     print('-----------------Billing Report Scheduler: Stopped')
    #     return
    # else:
    # # if True:
    #     print('-----------------Billing Report Scheduler: Playing')

    # ---------------------------------real one call api--------------------------


    #----------------------------------for uat purpose----------------------------

    
    # global doc_name
    # checkFile()
    # return

    # if isUnorganized == 1:
    #     new_date = date(day=31,month=1,year=2023)
    #     filename = '131_string(13) with rebate.csv'
    #     batch_id = getBatchID(filename)
    #     cr_dict,cr = getCr(filename)
    #     print('isUnorganized')
    # else:
        # doc_name, new_date,cr,cr_dict, batch_id = checkFile()
    # doc_name, new_date,cr,cr_dict, batch_id = checkFile()
    return_dict = checkFile(cr_dict,cr,batch_id,new_date)
    doc_name = return_dict['doc_name']
    cr_dict = return_dict['cr_dict']
    batch_id = return_dict['batch_id']
    new_date = return_dict['new_posting_date']

    print('---124---crdict:')
    print(cr_dict)

    # today = datetime.now().date()
    exist, name = checkExist(batch_id,'Billing')
    date_str = getDateString(new_date)
    if exist:
        print('Journal Entry of Billing for ',date_str,' is already create. You can see here '+name)
        # raise Exception('Journal Entry of Billing for ',date_str,' is already create. You can see here '+name)
    else:
        print('------------------date is ',new_date)

    # importfrombs(start_date, end_date)
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

    print('DONE SCHEDULER')
    return error_list
        
        # doc.append('journal_entry',{
        #     'journal_entry':je_name,
        # })

        # ---------------------------logic for deferred revenue
        # dje_list = []
        # get last drje data,
        
        # deffered_list = frappe.get_list('Deferred Revenue Journal Entry')
        # if deffered_list:
        #     prev_date = getPreviousDate(new_date)
        #     print('previous_date: ',prev_date)
        #     deferred = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
        #     last_dje = deferred.accounts
        
        # for row in last_dje:
        #     journal.append('deferred_accounts')
        #     last_dict = convertToDict(last_dje)
        # # put into list A
        #     for row in last_dict:
        #         # if row['month_count'] > 0:
        #         if row['month_count'] > 0:
        #             dje_list.append(row)

        # do logic for revenue
        # if len(dje_list):
        #     new_list = doLogicRevenue(dje_list)
        #     for row in new_list:
        #         journal.append('deferred_accounts',row)
        #         print('dididid')
        
        # new_date = datetime.strptime(tag_id_str,'%Y-%m-%d').date()
        # journal.posting_date = new_date
        # try:
        #     doc_name = 'Billing - '+new_date.strftime('%Y-%m-%d')
        #     journal.title = doc_name
        #     journal.save()
        #     journal.submit()
        #     frappe.db.commit()
        #     je_name = journal.name
            
        #     # domains = domain + '/app/journal-entry/'+ je_name
        #     # journal_link = "<a href='"+domains+"' target='_blank'>Billing - "+date_str+"</a>"
        #     # # frappe.msgprint('One Journal Entry has been created, See Here ')
        #     # msg = 'A journal entry has been made for Billing Report '+str(new_date)+'. Please see here '+journal_link
        #     # title = 'ERPNext: Journal Entry '+date_str
        #     # sendEmail(msg,title,journal.doctype,journal.name)
        #     # print('journal_link: ',journal_link)
        #     # frappe.msgprint('Journal Entries has been created, See Here '+journal_link)
        # except Exception as e:
        #     print('error: ',e)
        
        


        
        # # get current drje data
        # cur_list = []
        # counter = 1
        # for row in cr:
        #     if counter == 1:
        #         counter += 1
        #         rows_dict = {}
        #         try:
        #             revenue_account = row[39]
        #             # if revenue_account != '0' or revenue_account != '':
        #             revenue_account = int(revenue_account)
        #             print('revenue_account: ',revenue_account)
        #             #     rows_dict['revenue_account'] = revenue_account
        #             # else:
        #                 # continue
        #         except:
        #             continue
                
        #         year = row[1]
        #         account_number = row[2]
        #         cost_center_number = row[3]
        #         currency = row[12]
        #         debit = row[15]
        #         remark = row[23]
        #         posting_date = row[30]
        #         group = row[31]
        #         tax_amount = row[32]
        #         tax_code = row[33]
        #         second_cost_center_number = row[34]
        #         san_count = row[35]
        #         monthly_charge = row[36]
        #         month_count = row[37]
        #         current_month = row[38]
        #         rows_dicts = {
        #             # 'account':account_number,
        #             'account_number':account_number,
        #             # 'cost_center':cost_center.name,
        #             'cost_center_number':cost_center_number,
        #             # 'cost_center':cost_center.name,
        #             'currency':currency,
        #             'debit_in_account_currency' : float(debit),
        #             'credit_in_account_currency' : float(0),
        #             'remark':remark,
        #             'group':group,
        #             'year': year,
        #             'posting_date':posting_date,
        #             'tax_amount':tax_amount,
        #             'tax_code':tax_code,
        #             'second_cost_center_number':second_cost_center_number,
        #             'san_count':san_count,
        #             'monthly_charge':monthly_charge,
        #             'month_count':month_count,
        #             'current_month':current_month,
        #             'revenue_account':revenue_account
        #         }
        #         # rows_dict.update(rows_dicts)
        #         cur_list.append(rows_dicts)
                
        #     elif counter == 2:
        #         counter = 1
        #         rows_dict = {}
        #         try:
        #             revenue_account = row[39]
        #             # if revenue_account != '0' or revenue_account != '':
        #             revenue_account = int(revenue_account)
        #             # rows_dict['revenue_account'] = revenue_account
        #             # else:
        #             #     continue
        #         except:
        #             continue
                
        #         year = row[1]
        #         account_number = row[2]
        #         cost_center_number = row[3]
        #         currency = row[12]
        #         credit = row[15]
        #         remark = row[23]
        #         posting_date = row[30]
        #         group = row[31]
        #         tax_amount = row[32]
        #         tax_code = row[33]
        #         second_cost_center_number = row[34]
        #         san_count = row[35]
        #         monthly_charge = row[36]
        #         month_count = row[37]
        #         current_month = row[38]
        #         rows_dicts = {
        #             # 'account':account_number,
        #             'account_number':account_number,
        #             # 'cost_center':cost_center.name,
        #             'cost_center_number':cost_center_number,
        #             # 'cost_center':cost_center.name,
        #             'currency':currency,
        #             'debit_in_account_currency' : float(0),
        #             'credit_in_account_currency' : abs(float(credit)),
        #             'remark':remark,
        #             'group':group,
        #             'year': year,
        #             'posting_date':posting_date,
        #             'tax_amount':tax_amount,
        #             'tax_code':tax_code,
        #             'second_cost_center_number':second_cost_center_number,
        #             'san_count':san_count,
        #             'monthly_charge':monthly_charge,
        #             'month_count':month_count,
        #             'current_month':current_month,
        #             'revenue_account':revenue_account
        #         }
        #         # rows_dict.update(rows_dicts)
        #         cur_list.append(rows_dicts)

        # # append to list A
        # for row in cur_list:
        #     dje_list.append(row)       

        # print('djelist: ',dje_list)
        # # minus and calculate dr, put into list B
        # updatelist = doLogicDeferred(dje_list)
        # print('update list-------------------')
        # print(updatelist)
        
        # # create new drje
        # drje = frappe.new_doc('Deferred Revenue Journal Entry')
        # print('-----update listtt')
        # print(updatelist)

        # # put list B into it
        # for row in updatelist:
        #     drje.append('accounts',row)
        
        # print('drje--------------------------: ',tag_id_str)
        # drje.posting_date = tag_id_str
        # drje.tag_id = tag_id_str
        # drje.doc_name = tag_id_str
        # drje.save()
        # drje.submit()
        # drje_name =drje.name

        # domains = domain + '/app/deferred-revenue-journal-entry/'+ drje_name
        # error_link = "<a href='"+domains+"' target='_blank'>Deferred Revenue Journal Entry "+tag_id_str+"</a>"
        # msg = 'A deferred revenue journal entry has been made for Billing Report '+tag_id_str+'. Please see here '+error_link
        # title = 'ERPNext: Deferred Revenue Journal Entry '+tag_id_str
        # sendEmail(msg,title,drje.doctype,drje.name)





        # get last drje data, put into list A
        # get current drje data, append to list A
        # minus and calculate dr, put into list B
        # create new drje, put list B into it
        # create 2 new rows based on list B, put into current je


        # ---------------------------end of logic
        

        # doc.save()
        # doc.submit()

def doImportBillingReport():
    errors=[]
    getFileData = {"name": "pfile"}
    headers = {
        "Content-Type": "application/json",
    }
    # prod internal
    getFileReqUrl = 'http://172.18.96.101:8080/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    returnReqUrl = 'http://172.18.96.101:8080/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
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
                cr_dict,cr = getCr_pass_file(zip_file,file,0)
                fileDate = file[-14:-4]
                dateSplit = fileDate.split('-')
                print("dateSplit  ",dateSplit)
                year=dateSplit[0]
                month=dateSplit[1]
                day=dateSplit[2]
                new_date = date(year=int(year),month=int(month),day=int(day))
                batch_id = getBatchID(file,day)
                print('--------------filenamessss: ',file)
                error_list = doImportBillingReportSingle(file,cr_dict,cr,batch_id,new_date)
                errors.append(error_list)
    if errors !=[]:
        flattened_data = [item for sublist in errors for item in sublist]
        returnData =  {"name": "Pfile", "errorFileSummary":flattened_data}
    else:
        returnData =  {"name": "Pfile", "errorFileSummary":[]}
    print('errors: ',returnData)
    response = requests.request("POST", returnReqUrl,headers=headers,json=returnData, verify=False)
    if response.status_code == 200:
        print("Request was successful (Status Code 200).")
    
    # doUAT()
    # scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing Report'})
    # if scheduler.control == 'Stop':
    #     print('-----------------Billing Report Scheduler: Stopped')
    #     return
    # else:
    # # if True:
    #     print('-----------------Billing Report Scheduler: Playing')

    # ---------------------------------real one call api--------------------------


    #----------------------------------for uat purpose----------------------------

    
    # if isUnorganized == 1:
    #     new_date = date(day=31,month=1,year=2023)
    #     filename = '131_string(13) with rebate.csv'
    #     batch_id = getBatchID(filename)
    #     cr_dict,cr = getCr(filename)
    #     print('isUnorganized')
    # else:
        # doc_name, new_date,cr,cr_dict, batch_id = checkFile()
    # doc_name, new_date,cr,cr_dict, batch_id = checkFile()
    # today = datetime.now().date()
        # doc.append('journal_entry',{
        #     'journal_entry':je_name,
        # })
        
# def checkExist(tag_id):
#     try:
#         print('tag_id: ',tag_id)
#         je = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':tag_id})
#         # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
#         # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
#         domains = domain + '/app/journal-entry/'+ je.name
#         journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+tag_id+"</a>"
#         print('exist: true')
#         return True, je.name
#     except:
#         print('exist: false')
#         return False, ''

# def createcsv(start_date, end_date):
#     start_date = datetime.strptime(start_date,'%Y-%m-%d')
#     end_date = datetime.strptime(end_date,'%Y-%m-%d')
#     dates = {'start_date':start_date,'end_date':end_date}
#     start_date, end_date, year = getIsoDate(dates)
#     start_end_year = {'start_date':start_date,'end_date':end_date,'year':year}
#     existcr = {}
#     ready,cr = getCR(start_end_year,existcr)
#     # print('CR: ',cr)
#     if not len(cr):
#         print('cr start end year: ',start_end_year)
#         print('CR is empty')
#         raise Exception('Pfile is empty!')
#         # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
#         # email_args = {
#         # 	'recipients':user1.email,
#         # 	'message':'msg',
#         # 	'subject':'title',
#         # 	# 'reference_doctype':errorlog.doctype,
#         # 	# 'reference_name':errorlog.name
#         # }
#         # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)
#         # return False,'',''

#     if ready:
#         path = 'pfile_report'
#         date_name = getDateOnly(start_date)
#         # print('DATE NAME -------------------: ',date_name)
#         year = str(date_name.year)[-2:]
#         month = str(date_name.month)
#         if len(month) < 2:
#             month = '0'+month

#         pathtofile = path+'/PFILE_'+ str(month)+str(year)
#         filename = 'PFILE_' + str(month)+str(year)+'.csv'
#         # print('FILENAME: ',filename)

#         if os.path.exists(path):
#             with open(pathtofile,'w',newline='') as file:
#                 writer = csv.writer(file)
#                 for row in cr:
#                     # print('row: ',row)
#                     writer.writerow(row)
#         else:
#             os.makedirs(path)
#             with open(pathtofile,'w',newline='') as file:
#                 writer = csv.writer(file)
#                 for row in cr:
#                     # print('row: ',row)
#                     writer.writerow(row)

#         with open(pathtofile,'rb') as file:
#             print('return file',' path: ',pathtofile)
#             return file, filename, pathtofile

# def getDateOnly(start_date):
# 	date_only = start_date[:10]
# 	new_date = datetime.strptime(date_only,'%Y-%m-%d')
# 	year = new_date.year
# 	day = new_date.day
# 	month = new_date.month
# 	new_date = date(year,month,day)
# 	print('new_date: ',new_date)
# 	return new_date

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
#         print('-------LENGTH CM: ',length)

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

# latest
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

def checkDominant(f1,errors,error_list):
    val_list = []
    for o in f1:
        if not len(val_list):
            val = {'val':o['val'],'count':1}
            val_list.append(val)
        else:
            exist = False
            for v in val_list:
                if v['val'] == o['val']:
                    v['count']+=1
                    exist = True
            if not exist:
                val = {'val':o['val'],'count':1}
                val_list.append(val)

    if len(val_list) > 1:
        dominant = 0
        dominant_val = ''
        for v in val_list:
            if dominant == 0:
                dominant = v['count']
                dominant_val = v['val']
            else:
                if v['count'] > dominant:
                    dominant = v['count']
                    dominant_val = v['val']
        
        for o in f1:
            if dominant_val != o['val']:
                errors['error'] = True
                error = {
                        'row':o['row'],
                        'field':o['field'],
                        'val':o['val'],
                        'desc':'Wrong Data'
                    }
                # if '_' in o['field']:
                #     split = o['field'].split('_')
                #     if len(split) > 1:
                #         field = ''
                #         for i in range(len(split)):
                #             if field == '':
                #                 field = split[i]
                #             else:
                #                 field += ' '+split[i]
                #     error['desc'] = 'Wrong '+field
                # else:
                #     error['desc'] = 'Wrong '+o['field']

                error_list.append(error)

# def getError(row_list,row,error_list,errors,balance):
#     year = row_list['year']
#     account_number = row_list['account_number']
#     cost_center_number = row_list['cost_center_number']
#     currency = row_list['currency']
#     tax_amount = row_list['tax_amount']
#     second_cost_center_number = row_list['second_cost_center_number']
#     san_count = row_list['san_count']
#     monthly_charge = row_list['monthly_charge']
#     month_count = row_list['month_count']
#     current_month = row_list['current_month']
#     revenue_account = row_list['revenue_account']
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
#     user_remark = row_list['user_remark']
#     posting_date = row_list['posting_date']
#     group = row_list['group']

    
#     objYear = {'field':'year','value':year}
#     objAccount = {'field':'account_number','value':account_number,'doctype':'Account'}
#     objCost = {'field':'cost_center_number','value':cost_center_number,'doctype':'Cost Center'}
#     objCurrency = {'field':'currency','value':currency}
#     objPostingDate = {'field':'posting_date', 'value':posting_date}
#     objGroup = {'field':'group','value':group}
#     objTaxAmount = {'field':'tax_amount', 'value':tax_amount}
#     objSecondCostCenterNumber = {'field':'second_cost_center_number','value':second_cost_center_number}
#     objSanCount = {'field':'san_count','value':san_count}
#     objMonthlyCharge = {'field':'monthly_charge','value':monthly_charge}
#     objMonthCount = {'field':'month_count','value':month_count}
#     objCurrentMonth = {'field':'current_month','value':current_month}
#     objRevenueAccount = {'field':'revenue_account','value':revenue_account}
#     # objRevenueAccount = {'field':'revenue_account','value':revenue_account,'doctype':'Account'}
#     objUserRemark = {'field':'user_remark','value':user_remark}
    
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
#         balance = checkError(f1,'','',row,errors,error_list,'') # get value
#     # credit
#     elif amt_type == 'credit':
#         f1 = {'field':'credit_in_account_currency','value':abs(float(debit_credit))}
#         checkError(f1,2,'float',row,errors,error_list,'') # check float type
#         checkEmpty(f1,row,errors,error_list)
#         checkError(f1,'','',row,errors,error_list,balance)  # check balance
#     # tax amount
#     checkEmpty(objTaxAmount,row,errors,error_list)
#     checkError(objTaxAmount,2,'number',row,errors,error_list,'') # check number type
#     # tax code
#     # second_cost_center_number
#     checkEmpty(objSecondCostCenterNumber,row,errors,error_list)
#     # san_count
#     checkEmpty(objSanCount,row,errors,error_list)
#     checkError(objSanCount,2,'number',row,errors,error_list,'') # check number type
#     # monthly charge
#     checkEmpty(objMonthlyCharge,row,errors,error_list)
#     checkError(objMonthlyCharge,2,'number',row,errors,error_list,'') # check number type
#     # month count
#     checkEmpty(objMonthCount,row,errors,error_list)
#     checkError(objMonthCount,2,'number',row,errors,error_list,'') # check number type
#     # current month
#     checkError(objCurrentMonth,7,'',row,errors,error_list,'')      
#     checkEmpty(objCurrentMonth,row,errors,error_list)
#     checkError(objCurrentMonth,2,'number',row,errors,error_list,'') # check number type
#     # revenue account
#     # checkEmpty(objRevenueAccount,row,errors,error_list)
#     # checkError(objRevenueAccount,1,'',row,errors,error_list,'')    # check exist
#     # # user remark
#     checkEmpty(objUserRemark,row,errors,error_list)
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

# latest
# def getError(row_list,row,error_list,errors,balance):
#     year = row_list['year']
#     account_number = row_list['account_number']
#     cost_center_number = row_list['cost_center_number']
#     currency = row_list['currency']
#     tax_amount = row_list['tax_amount']
#     profit_or_cost_center_number = row_list['profit_or_cost_center_number']
#     san_count = row_list['san_count']
#     monthly_charge = row_list['monthly_charge']
#     month_count = row_list['month_count']
#     current_month = row_list['current_month']
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
#     objTaxAmount = {'field':'tax_amount', 'value':tax_amount}
#     objProfitOrCostCenterNumber = {'field':'profit_or_cost_center_number','value':profit_or_cost_center_number}
#     objSanCount = {'field':'san_count','value':san_count}
#     objMonthlyCharge = {'field':'monthly_charge','value':monthly_charge}
#     objMonthCount = {'field':'month_count','value':month_count}
#     objCurrentMonth = {'field':'current_month','value':current_month}
#     try:
#         revenue_account = row_list['revenue_account']
#         objRevenueAccount = {'field':'revenue_account','value':revenue_account}
#     except:
#         pass
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
#     # tax amount
#     checkEmpty(objTaxAmount,row,errors,error_list)
#     checkError(objTaxAmount,2,'number',row,errors,error_list,'') # check number type
#     # tax code
#     # second_cost_center_number
#     checkEmpty(objProfitOrCostCenterNumber,row,errors,error_list)
#     # san_count
#     checkEmpty(objSanCount,row,errors,error_list)
#     checkError(objSanCount,2,'number',row,errors,error_list,'') # check number type
#     # monthly charge
#     checkEmpty(objMonthlyCharge,row,errors,error_list)
#     checkError(objMonthlyCharge,2,'number',row,errors,error_list,'') # check number type
#     # month count
#     checkEmpty(objMonthCount,row,errors,error_list)
#     checkError(objMonthCount,2,'number',row,errors,error_list,'') # check number type
#     # current month
#     checkError(objCurrentMonth,7,'',row,errors,error_list,'')      
#     checkEmpty(objCurrentMonth,row,errors,error_list)
#     checkError(objCurrentMonth,2,'number',row,errors,error_list,'') # check number type
#     # revenue account
#     # checkEmpty(objRevenueAccount,row,errors,error_list)
#     # checkError(objRevenueAccount,1,'',row,errors,error_list,'')    # check exist
#     # # user remark
#     checkEmpty(objUserRemark,row,errors,error_list)
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
#                 'group':row[31],
#                 'tax_amount':row[32],
#                 'tax_code':row[33],
#                 'second_cost_center_number':row[34],
#                 'san_count':row[35],
#                 'monthly_charge':row[36],
#                 'month_count':row[37],
#                 'current_month':row[38]
#             }
#             try:
#                 row_list['revenue_account'] = row[39]
#             except:
#                 row_list['revenue_account'] = 0

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
#                 'group':row[31],
#                 'tax_amount':row[32],
#                 'tax_code':row[33],
#                 'second_cost_center_number':row[34],
#                 'san_count':row[35],
#                 'monthly_charge':row[36],
#                 'month_count':row[37],
#                 'current_month':row[38]
#             }
#             try:
#                 row_list['revenue_account'] = row[39]
#             except:
#                 row_list['revenue_account'] = 0
#             # other = {'row':row_count,'posting_date':posting_date,'group':group}
#             # others.append(other)
#             posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
#             posting_date_list.append(posting_dates)
#             groups = {'row':row_count,'field':'group','val':group}
#             group_list.append(groups)
#             getError(row_list,row_count,error_list,errors,balance)


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
#         # for p in error_list:
#         #     print(p)
#         return True,error_list

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

# def getDatetime(dates):
#     if isinstance(dates, str):
#         dates = datetime.strptime(dates, '%Y-%m-%d')
#         dates = dates.date()
#         # print('datessss datetime: ',dates)

#     return dates

# def getDate(start_date,end_date):
# 	# start_date = getDatetime(start_date)
#     # end_date = getDatetime(end_date)
# 	start_date = getDatetimeDate(start_date)
# 	end_date = getDatetimeDate(end_date)
# 	year = start_date.year
# 	times = time(0,0,0)
# 	start_date = datetime.combine(start_date,times)
# 	end_date = datetime.combine(end_date,times)
# 	start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
# 	start_date = start_date.isoformat()+"Z"
# 	print('++++++++++++++STARTDATE')
# 	print(start_date)
# 	end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
# 	end_date = end_date.isoformat()+"Z"

# 	return start_date, end_date, year

# def getMonth(dates):
#     if isinstance(dates, str):
#         dates = datetime.strptime(dates, '%Y-%m-%d')
#         dates = dates.date()
    
#     month = dates.strftime('%B')
#     print('month: ',month)
#     return month
                
# def getCR(start_end_year,existcr):
# 	start_date = start_end_year['start_date']
# 	end_date = start_end_year['end_date']
# 	year = start_end_year['year']
# 	reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextPFileMthEndJob'})
# 	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
# 	reqUrl = reportcr.url +reportcr.api_key
# 	print('reqURL: ',reqUrl)

# 	payload = json.dumps({
# 	"startDate": start_date,
# 	"endDate": end_date,
# 	"name": "string",
# 	"year": year
# 	}, default=str)

# 	print('payload: ',payload)

# 	headersList = {
# 	"Accept": "*/*",
# 	"Content-Type": "application/json" 
# 	}

# 	response = requests.request("POST", reqUrl, data=payload, headers=headersList)

# 	headers = response.headers
# 	# print(headers)
# 	msg = headers.get('return-message')
# 	textt = response.content.decode('utf-8')
# 	cr = csv.reader(textt.splitlines(), delimiter=',')
# 	cr = list(cr)
# 	print('===========CR==============')
# 	# print(cr)
# 	# return True,cr
# 	if 'filename=string.csv.tmp' in msg:
# 		existcr['exist'] = False
# 		return False,''
# 		# raise Exception('The file you are trying to get is not in CSV format. Please try again later.')
# 	else:
# 		textt = response.content.decode('utf-8')
# 		cr = csv.reader(textt.splitlines(), delimiter=',')
# 		cr = list(cr)
# 		# print('++++++++CR LENGTH: ',len(cr))
# 		if not len(cr):
# 			return False, cr
# 		# print('========cr=========:',cr)
# 		return True,cr  

# def checkReadyCR(start_date,end_date):
#     # startdate,enddate,year = getDate(start_date,end_date)
#     startdate = getISODate(start_date)
#     enddate = getISODate(end_date)
#     year = start_date.year
#     start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#     existcr = {}
#     ready,cr = getCR(start_end_year,existcr)

#     if not len(existcr):
#         return True,cr
#     else:
#         return False,cr

#     # dates_list = []
#     # start_end_year = {}

#     # if much:
#     #     diff = end_date - start_date
#     #     diff_day = diff.days + 1
# 	# 	# print('startdaate: ',start_date)
#     #     counter = 0

#     #     for i in range(diff_day):
#     #         if i == 0:
#     #             startdate = enddate = start_date
#     #             # date_dic = {'start_date':startdate,'end_date':enddate}
#     #             startdate,enddate,year = getDate(startdate,enddate)
#     #             start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#     #             # date_dic = {'start_date':startdate,'end_date':enddate}
#     #             dates_list.append(start_end_year)
#     #             counter += 1
#     #         else:
#     #             next_date = start_date + timedelta(days=counter)
#     #             counter += 1
#     #             startdate = enddate = next_date
#     #             date_dic = {'start_date':startdate,'end_date':enddate}
#     #             startdate,enddate,year = getDate(startdate,enddate)
#     #             start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
#     #             dates_list.append(start_end_year)

#     #     # print('---------DATE LIST')
#     #     # print(dates_list)
#     # else:
#     #     # date_dic = {'start_date':start_date,'end_date':end_date}
#     #     startdate,enddate,year = getDate(start_date,end_date)
#     #     start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}

#     # existcr = {}
#     # cr_ready = []
#     # cr_notready = []
#     # if much:
#     #     for d in dates_list:
#     #         ready,cr = getCR(d,existcr)
#     #         if cr == '':
#     #             print('KOSONGGGG')
#     #         else:
#     #             print('TAK KOSONGGGG')
#     #         if ready:
#     #             cr_start = {'cr':cr,'date':d['start_date']}
#     #             cr_ready.append(cr_start)
#     #         else:
#     #             cr_notready.append(d['start_date'])
#     #     if not len(existcr):
#     #         return True,cr_ready,cr_notready
#     #     else:
#     #         return False,cr_ready,cr_notready
#     # else:
#     #     # print('====date_dic====')
#     #     # print(date_dic)
#     #     ready,cr = getCR(start_end_year,existcr)
#     #     # if len(cr) == 0:
#     #     #     print('KOSONGSSS')
#     #     # else:
#     #     #     print('TAK KOSONGSSS')
#     #     #     print(cr)
#     #     # print('CR IN CHECKREADY: ',cr)
#     #     cr_start = {'cr':cr,'date':start_end_year['start_date']}
#     #     cr_ready.append(cr_start)
#     #     # print('CR-DATE')
#     #     # print(cr_date)
#     #     if ready:
#     #         return True,cr_ready,''
#     #     else:
#     #         return False,cr_ready,''

# def sendEmail(msg,subject,doctype,name):
#     userlist = []
#     users = frappe.get_all('User')
#     for user in users:
#         u = frappe.get_last_doc('User',filters={'name':user.name})
#         rolelist = u.roles
#         if rolelist:
#             for r in rolelist:
#                 if r.role == 'Accounts Manager':
#                     userlist.append(u.email)
#                     break  
#     email_args = {
#         'recipients':userlist,
#         'message':msg,
#         'subject':subject,
#         'reference_doctype':doctype,
#         'reference_name':name
#     }
#     frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)

def createErrorLog(file,much,error_list,errordate):
    errordate = errordate[:10]
    errordate = datetime.strptime(errordate,'%Y-%m-%d')
    errordate = errordate.date()
    errorlog = frappe.new_doc('Billing Journal Entry Error Log')
    errorlog.date = datetime.now().date()
    errorlog.collection_report_date = errordate
    errorlog.start_date = errordate
    errordate_str = errordate.strftime('%Y-%m-%d')
    for e in error_list:
        errorlog.append('error_list',{
            'file':file,
            'row':e['row'],
            'field':e['field'],
            'value':e['value'],
            'description':e['description']
        })
    errorlog.save()
    print('name:: ',errorlog.name)
    # domain = 'http://175.136.236.153:8003' + '/app/billing-journal-entry-error-log/'+ errorlog.name
    # domain = 'http://127.0.0.1:8000' + '/app/billing-journal-entry-error-log/'+ errorlog.name
    domains = domain + '/app/billing-journal-entry-error-log/'+ errorlog.name
    error_link = "<a href='"+domains+"' target='_blank'>Error Log "+str(errordate_str)+"</a>"
    msg = 'A billing journal entry error log has been made for Billing Report '+str(errordate)+'. Please see here '+error_link
    title = 'ERPNext: Billing Journal Entry Error Log '+str(errordate)
    sendEmail(msg,title,errorlog.doctype,errorlog.name,'IWK User')
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
    # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)
    if not much:
        # frappe.msgprint('There is error(s) when trying to import the Collection Report. You can see the list here ' +error_link)
        return error_link,errorlog.name
    else:
        return error_link,errorlog.name

# def importfrombs(start_date, end_date,cr):
def importfrombs(file,cr_dict):
    # ready,cr = checkReadyCR(start_date,end_date)
    # if ready:
    #     # print('CR: ',cr)
    #     print('start_date: ',start_date,' end_date: ',end_date)
    #     print('CR IS READY!')

	# if start_date != end_date:
	# 	much = True
	# 	ready,cr_ready,cr_notready = checkReadyCR(much,start_date,end_date)
	# else:
	# 	much = False
	# 	ready,cr_ready,cr_notready = checkReadyCR(much,start_date,'')
	# 	print('CR ABLE: ',cr_ready)
                
	# much,exist,cr_able,cr_unable = checkReadyCR(start_date,end_date)
    cr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    error_log_name_list = []
    journal_entry_name_list = []
	# journal_entry_link = []
    print('cr-dict: -------------------')
    print(cr_dict)

    error_result, error_list = handleError(file,cr_dict)
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

# def getCurrentMonthStr():
#     today = datetime.now().date()
#     month = today.strftime('%m')
#     year = today.strftime('%y')
#     currentmonth = month+year
#     return currentmonth

# def createAccountingEntries(journal,cr,new_date):
#     # latest_posting = date(day=1,month=1,year=1900)
#     posting_date = ''

#     if not len(cr):
#         now = datetime.now().strftime('%Y-%m-%d')
#         # new_date = datetime.strptime(now, '%Y-%m-%d').date() + timedelta(days=1)
#         # journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         # tag_id = getDateOnly(dates)
#         # tag_id_str = tag_id.strftime('%Y-%m-%d')
#         # journal.tag_id = tag_id
#         journal.save()
#         journal.submit()
#         je_name = journal.name
#         return je_name,''
#     else:
#         counter = 1
#         total_debit = 0
#         total_credit = 0

#         first_date = cr[0][30]
        
#         for row in cr:
#             # debit
#             # print('ROW')
#             # print(row)
#             row_list = []
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
#                 tax_amount = row[32]
#                 tax_code = row[33]
#                 second_cost_center_number = row[34]
#                 san_count = row[35]
#                 monthly_charge = row[36]
#                 month_count = row[37]
#                 current_month = row[38]
#                 try:
#                     revenue_account = row[39]
#                 except:
#                     revenue_account = 0

#                 # print('debit: ',debit)
#                 total_debit += float(debit)
#                 # print('total_debit: ',total_debit)

#                 rows_dict = {
#                     # 'account':account_number,
#                     'account_number':account_number,
#                     # 'cost_center':cost_center.name,
#                     'cost_center_number':cost_center_number,
#                     # 'cost_center':cost_center.name,
#                     'currency':currency,
#                     'debit_in_account_currency' : float(debit),
#                     'credit_in_account_currency' : float(0),
#                     'remark':remark,
#                     'group':group,
#                     'year': year,
#                     'posting_date':posting_date,
#                     'tax_amount':tax_amount,
#                     'tax_code':tax_code,
#                     'second_cost_center_number':second_cost_center_number,
#                     'san_count':san_count,
#                     'monthly_charge':monthly_charge,
#                     'month_count':month_count,
#                     'current_month':current_month,
#                     'revenue_account':revenue_account
#                 }

#                 row_list.append(rows_dict)
                
#                 debit_acc = frappe.get_last_doc("Account", filters={"account_number":account_number})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":cost_center_number})
#                 journal.append('accounts',{
#                     'account':debit_acc.name,
#                     'account_number':debit_acc.account_number,
#                     'cost_center':cost_center.name,
#                     'cost_center_number':cost_center_number,
#                     # 'cost_center':cost_center.name,
#                     'currency':currency,
#                     'debit_in_account_currency' : float(debit),
#                     'credit_in_account_currency' : float(0),
#                     'remark':remark,
#                     'group':group,
#                     'year': year,
#                     'posting_date':posting_date,
#                     'tax_amount':tax_amount,
#                     'tax_code':tax_code,
#                     'second_cost_center_number':second_cost_center_number,
#                     'san_count':san_count,
#                     'monthly_charge':monthly_charge,
#                     'month_count':month_count,
#                     'current_month':current_month,
#                     'revenue_account':revenue_account
#                 })

#                 # posting_date = getDatetime(posting_date)
#                 # if latest_posting < posting_date:
#                 #     latest_posting = posting_date

                

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
#                 tax_amount = row[32]
#                 tax_code = row[33]
#                 second_cost_center_number = row[34]
#                 san_count = row[35]
#                 monthly_charge = row[36]
#                 month_count = row[37]
#                 current_month = row[38]
#                 try:
#                     revenue_account = row[39]
#                 except:
#                     revenue_account = 0

#                 rows_dict = {
#                     # 'account':account_number,
#                     'account_number':account_number,
#                     # 'cost_center':cost_center.name,
#                     'cost_center_number':cost_center_number,
#                     # 'cost_center':cost_center.name,
#                     'currency':currency,
#                     'debit_in_account_currency' : float(0),
#                     'credit_in_account_currency' : float(credit),
#                     'remark':remark,
#                     'group':group,
#                     'year': year,
#                     'posting_date':posting_date,
#                     'tax_amount':tax_amount,
#                     'tax_code':tax_code,
#                     'second_cost_center_number':second_cost_center_number,
#                     'san_count':san_count,
#                     'monthly_charge':monthly_charge,
#                     'month_count':month_count,
#                     'current_month':current_month,
#                     'revenue_account':revenue_account
#                 }

#                 row_list.append(rows_dict)

#                 credit_acc = frappe.get_last_doc("Account", filters={"account_number":account_number})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":cost_center_number})
#                 total_credit += float(credit)
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
#                     'posting_date':posting_date,
#                     'tax_amount':tax_amount,
#                     'tax_code':tax_code,
#                     'second_cost_center_number':second_cost_center_number,
#                     'san_count':san_count,
#                     'monthly_charge':monthly_charge,
#                     'month_count':month_count,
#                     'current_month':current_month,
#                     'revenue_account':revenue_account
#                 })

#                 # posting_date = getDatetime(posting_date)
#                 # if latest_posting < posting_date:
#                 #     latest_posting = posting_date
        
#         # --------------------------------------logic for deferred and revenue----------------

#         # now = datetime.now().date()
#         # journal.entry_type = "Journal Entry"
#         # month_num = getMonthNumber(month_glb)
        
#         # if latest_posting.month != month_num:
#         #     if month_num % 2 == 0:
#         #         if month_num < 8:
#         #             day = 30
#         #         else:
#         #             day = 31
#         #     else:
#         #         if month_num < 8:
#         #             day = 31
#         #         else:
#         #             day = 30
#         #     print('month: ',month_num,' day: ',day)
#         #     latest_posting = date(day=day, month=month_num, year=latest_posting.year)
#         # journal.posting_date = latest_posting
#         # journal.tag_id = latest_posting
#         # print('--------------POSTING DATE: ',posting_date)
#         # month = getMonth(posting_date)
#         # year = latest_posting.year
#         # tag_id = getDatetime(posting_date)
#         # sch = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing Report'})
#         # sch = frappe.get_last_doc('random')
#         # if sch.value == 0:
#         #     try:
#         #         val = sch.value
#         #         val += 1
#         #         sch.value = val
#         #     except:
#         #         val = 1
#         #         sch.value = val
#         #     sch.save()
#         #     sch.submit()
#         #     month = tag_id.month + val
#         #     # tag_id = tag_id.replace(month=tag_id.month+val)
#         #     if month > 12:
#         #         year+=1
#         #         month=1
#         #     days = calendar.monthrange(tag_id.year,month)
#         #     tag_id = date(day=days[1],month=month,year=year)

        

#         # tag_id_str = tag_id.strftime('%Y-%m-%d')
#         # journal.tag_id = tag_id
#         # journal.save()
#         # journal.submit()
#         # company = frappe.get_last_doc('Company',filters={'company_name':journal.company})
#         # journal.title = journal.report_type + ' - '+month+' '+str(year)
#         # journal.title = doc_name
#         # journal.save()
#         # journal.submit()
#         # je_name = journal.name
#         # print('je_name: ',je_name)

#         # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je_name
#         # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
#         # domains = domain + '/app/journal-entry/'+ je_name
#         # journal_link = "<a href='"+domains+"' target='_blank'>Billing - "+tag_id_str+"</a>"
#         # # frappe.msgprint('One Journal Entry has been created, See Here ')
#         # msg = 'A journal entry has been made for Billing Report '+str(posting_date)+'. Please see here '+journal_link
#         # title = 'ERPNext: Journal Entry '+str(posting_date)
#         # sendEmail(msg,title,journal.doctype,journal.name)
#         # return journal, tag_id_str
#         # dr_list = getDr(new_date)
#         return journal

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
        je_name = 'Billing - '+str(end_date)
        journal.title = je_name
        journal.noaccount = 'No Current Month Import Data For This Month'
        journal.save()
        domains = domain + '/app/journal-entry/'+ journal.name
        journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+str(end_date)+"</a>"
        # frappe.msgprint('One Journal Entry has been created, See Here ')
        msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
        title = 'ERPNext: Journal Entry '+str(posting_date)
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
        journal.title = 'Billing - '+str(posting_date)
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

def doCalculate(row,f1):
    # print('--row--: ',row)
    # print('LENGTH: ',len(row))
    # print('---row: ',row['month_count'])
    # print('---type: ',type(row['month_count']))
    # print('month count 1: ',row['month_count'])
    # month_count = 1
    if f1 == 1:
        month_count = int(row['month_count']) - 1
    else:
        month_count = 1
    row['month_count']  = month_count
    # print('=month count: ',month_count)
    # print('=row ',row['month_count'])
    # print('month count 2: ',row['month_count'])
    deferred_revenue = month_count*row['monthly_charge']*row['san_count']
    # print('month count: ',month_count)
    return deferred_revenue, row

# def doLogicDeferred(dje_list):
#     new_list = [] # accounting entries that needed to be added to JE last month
#     update_list = []
#     counter = 1
#     revenue_counter = 0
#     row_1 = {}
#     row_2 = {}

#     i = -1

#     for row in dje_list:
#         i += 1
#         if revenue_counter == 0:
#             if counter == 1:
#                 counter += 1
#                 deferred_revenue, row = doCalculate(row,1)
#                 row['debit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row1 = row.copy()
#                 deferred_revenue2, row_1 = doCalculate(row1,2)
#                 row_1['debit_in_account_currency'] = deferred_revenue2
#                 row_1['credit_in_account_currency'] = 0
#             elif counter == 2:
#                 counter = 1
#                 revenue_counter += 1
#                 deferred_revenue, row = doCalculate(row,1)
#                 row['credit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row2 = row.copy()
#                 deferred_revenue2, row_2 = doCalculate(row2,2)
#                 row_2['credit_in_account_currency'] = deferred_revenue2
#                 row_2['debit_in_account_currency'] = 0
#         if revenue_counter == 1:
#             revenue_counter = 0
#             row_1['account_number'] = row_2['account_number']
#             row_1['account'] = row_2['account']
#             row_1['cost_center_number'] = row_2['cost_center_number']
#             row_1['cost_center'] = row_2['cost_center']
#             row_2['revenue_account'] = None
#             row_2['account_number'] = row_1['revenue_account']
#             acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#             row_2['account'] = acc.name
#             row_1['month_count'] = 1
#             row_2['month_count'] = 1

#             new_list.append(row_1)
#             new_list.append(row_2)
#     return new_list

def doLogicDeferred(dje_list):
    print('------------pop')
    for d in dje_list:
        print(d)
        print('\n\n')
    new_list = [] # accounting entries that needed to be added to JE last month
    update_list = []
    counter = 1
    revenue_counter = 0
    row_1 = {}
    row_2 = {}
    isBegin = True
    seq = 0
    isDebitFirst = False

    i = -1

    for row in dje_list:
        i += 1
        if isBegin:
            counter = 2
            isDebitFirst = False
            if row['credit_in_account_currency'] == 0.0:
                counter = 1
                isDebitFirst = True
                print('debit: ',row['debit_in_account_currency'],' credit: ',row['credit_in_account_currency'])
                print('type: ',type(row['credit_in_account_currency']))
            isBegin = False
            revenue_counter = 0
            seq = 1

        if revenue_counter == 0:
            if seq == 2:
                revenue_counter = 1

            if counter == 1:
                if seq == 1:
                    seq = 2
                    counter = 2

                deferred_revenue, row = doCalculate(row,1)
                row['debit_in_account_currency'] = deferred_revenue
                update_list.append(row)
                row1 = row.copy()
                deferred_revenue2, row_1 = doCalculate(row1,2)
                row_1['debit_in_account_currency'] = deferred_revenue2
                row_1['credit_in_account_currency'] = 0

            elif counter == 2:
                if seq == 1:
                    seq = 2
                    counter = 1

                deferred_revenue, row = doCalculate(row,1)
                row['credit_in_account_currency'] = deferred_revenue
                update_list.append(row)
                row2 = row.copy()
                deferred_revenue2, row_2 = doCalculate(row2,2)
                row_2['credit_in_account_currency'] = deferred_revenue2
                row_2['debit_in_account_currency'] = 0
            
            

        # if revenue_counter == 1:
        #     revenue_counter = 0
        #     isBegin = True
        #     seq = 0
        #     if isDebitFirst:
        #         row_1['account_number'] = row_2['account_number']
        #         row_1['account'] = row_2['account']
        #     row_1['cost_center_number'] = row_2['cost_center_number']
        #     row_1['cost_center'] = row_2['cost_center']
        #     row_2['revenue_account'] = None
        #     row_2['account_number'] = row_1['revenue_account']
        #     acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
        #     row_2['account'] = acc.name
        #     row_1['month_count'] = 1
        #     row_2['month_count'] = 1

        #     new_list.append(row_1)
        #     new_list.append(row_2)

        if revenue_counter == 1:
            revenue_counter = 0
            isBegin = True
            seq = 0

            if isDebitFirst:
                row_1['account_number'] = row_2['account_number']
                row_1['account'] = row_2['account']

                cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
                row_1['cost_center_number'] = row_2['cost_center_number']
                # row_1['cost_center'] = row_2['cost_center']
                # change
                row_1['cost_center'] = cost_center.name
                row_2['cost_center'] = cost_center.name

                row_2['revenue_account'] = None
                row_2['account_number'] = row_1['revenue_account']
                acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
                row_2['account'] = acc.name
                row_1['month_count'] = 1
                row_2['month_count'] = 1

                new_list.append(row_1)
                new_list.append(row_2)
                print('isdebitfirst true')
            else:
                row_2['account_number'] = row_1['account_number']
                row_2['account'] = row_1['account']
                # change
                cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
                row_1['cost_center'] = cost_center.name
                row_2['cost_center'] = cost_center.name

                row_2['cost_center_number'] = row_1['cost_center_number']
                # row_2['cost_center'] = row_1['cost_center']
                row_1['revenue_account'] = None
                row_1['account_number'] = row_2['revenue_account']
                acc = frappe.get_last_doc('Account',filters={'account_number':row_1['account_number']})
                row_1['account'] = acc.name
                row_2['month_count'] = 1
                row_1['month_count'] = 1
            # row_1['cost_center_number'] = row_2['cost_center_number']
            # row_1['cost_center'] = row_2['cost_center']
            # row_2['revenue_account'] = None
            # row_2['account_number'] = row_1['revenue_account']
            # acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
            # row_2['account'] = acc.name
            # row_1['month_count'] = 1
            # row_2['month_count'] = 1

                new_list.append(row_2)
                new_list.append(row_1)
                print('isdebitfirst false')
    return new_list

# def getRM(price):
#     if not isinstance(price, str):
#         price = str(price)
#     if '.' in price:
#         split = price.split('.')
#         if len(split[1]) < 2:
#             split[1] = '00'
#             price = 'RM '+split[0]+'.'+split[1]
#         else:
#             price = 'RM '+price
#     else:
#         price = 'RM '+price+'.00'
#     print('price: ',price)
#     return price

# def createDeferredAccountingEntries(journal,new_date):
#     # --------------------find the DR using previous date----------------------------------
#     # prev_date = getPreviousDate(new_date)
#     # print('-------prev_date: ',prev_date,' type: ',type(prev_date))
#     # deferreds = frappe.get_list('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
    
#     #--------------------find DR using last DR created-------------------------------------
#     deferreds = getDocList('Deferred Revenue Journal Entry','',True)
#     if not deferreds:
#         # print('No Deferred Found for ',getDateString(prev_date))
#         print('No Previous Deferred Revenue Found!')
#         return
#     else:
#         # deferred = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
#         deferred = getDoc('Deferred Revenue Journal Entry','')
#     acc = deferred.accounts
#     counter = 1
#     dr = []
#     isBegin = True
#     complete = False
#     seq = 0
#     for row in acc:
#         # print('-----debit: ',row.debit_in_account_currency,' ---credit: ',row.credit_in_account_currency)
#         # print('acccc debit: ',row.debit_in_account_currency,' credit: ',row.credit_in_account_currency)
        
#         if isBegin:
#             counter = 2
#             if row.debit_in_account_currency != 0.0:
#                 counter = 1
#             isBegin = False
#             seq = 1
#             complete = False

#         if not complete:
#             if seq == 2:
#                 complete = True
#                 isBegin = True
#             if counter == 1:
#                 print('debit')
#                 if seq == 1:
#                     counter = 2
#                     seq += 1
#                 rows_dict = {
#                     'account':row.account,
#                     'account_number':row.account_number,
#                     'cost_center':row.cost_center,
#                     'cost_center_number':row.cost_center_number,
#                     # 'cost_center':cost_center.name,
#                     'currency':row.currency,
#                     'debit_in_account_currency' : float(row.debit_in_account_currency),
#                     'credit_in_account_currency' : float(0),
#                     'remark':row.remark,
#                     'group':row.group,
#                     'year': row.year,
#                     'posting_date':row.posting_date,
#                     'tax_amount':row.tax_amount,
#                     'tax_code':row.tax_code,
#                     'profit_or_cost_center_number':row.profit_or_cost_center_number,
#                     'san_count':row.san_count,
#                     'monthly_charge':row.monthly_charge,
#                     'month_count':row.month_count,
#                     'current_month':row.current_month,
#                     'revenue_account':row.revenue_account,
#                     'journal_entry':row.journal_entry
#                 }
#                 dr.append(rows_dict)
#             elif counter == 2:
#                 print('credit')
#                 if seq == 1:
#                     counter = 1
#                     seq += 1
#                 rows_dict = {
#                     'account':row.account,
#                     'account_number':row.account_number,
#                     'cost_center':row.cost_center,
#                     'cost_center_number':row.cost_center_number,
#                     # 'cost_center':cost_center.name,
#                     'currency':row.currency,
#                     'debit_in_account_currency' : float(0),
#                     'credit_in_account_currency' : float(row.credit_in_account_currency),
#                     'remark':row.remark,
#                     'group':row.group,
#                     'year': row.year,
#                     'posting_date':row.posting_date,
#                     'tax_amount':row.tax_amount,
#                     'tax_code':row.tax_code,
#                     'profit_or_cost_center_number':row.profit_or_cost_center_number,
#                     'san_count':row.san_count,
#                     'monthly_charge':row.monthly_charge,
#                     'month_count':row.month_count,
#                     'current_month':row.current_month,
#                     'revenue_account':row.revenue_account,
#                     'journal_entry':row.journal_entry
#                 }
#                 dr.append(rows_dict)
        
#     for i in dr:
#         print(i)
#         print('\n\n')

#     new_list = doLogicDeferred(dr)
#     counter = 1
#     total_debit = 0
#     total_credit = 0
#     for row in new_list:
#         if counter == 1:
#             counter +=1
#             total_debit += row['debit_in_account_currency']
#         elif counter == 2:
#             counter = 1
#             total_credit += row['credit_in_account_currency']
#         journal.append('deferred_accounts',row)
#     # print('dr: ')  
#     # for i in dr:
#     #     print(i) 
#     #     print('\n\n')
#     journal.total_deferred_debit = getRM(total_debit)
#     journal.total_deferred_credit = getRM(total_credit)
#     print('Done Create ')
  
# def createJE(cr,new_date):
#     journal = frappe.new_doc("Journal Entry")
#     journal.report_type = 'Billing'
#     journal.posting_date = new_date
#     journal.tag_id = new_date
#     posting_date = ''
#     # print('CRRRR')
#     # print(cr)
#     print('LENGTH: ',len(cr))
#     # latest_posting = date(day=1,month=1,year=1900)
#     createAccountingEntries(journal,cr,new_date)
#     print('test')
#     createDeferredAccountingEntries(journal,new_date)
    
#     # createBillingAccountingEntries(journal)

#     # je_name = journal.name
#     # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je_name
#     # # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
#     # journal_link = "<a href='"+domain+"' target='_blank'>Journal Entry "+tag_id_str+"</a>"
#     # # frappe.msgprint('One Journal Entry has been created, See Here ')
#     # msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
#     # title = 'ERPNext: Journal Entry '+str(posting_date)

#     return journal

def createJE(cr,end_date,batch_id):
    print('=================================================cr======')
    print(cr)
    journal = frappe.new_doc("Journal Entry")
    journal.report_type = 'Billing'
    posting_date = ''
    # print('CRRRR')
    # print(cr)
    print('LENGTH: ',len(cr))
    latest_posting = date(day=1,month=1,year=1900)
    # je_name, journal_link = createAccountingEntries(journal,cr,end_date)
    createAccountingEntries(journal,cr,end_date)
    # print('journal_link: ',journal_link)
    # createDeferredAccountingEntries(journal,end_date)
    # journal.save()
    # print('batchid je: ',batch_id)
    journal.tag_id = batch_id
    journal.save()
    journal.submit()
    frappe.db.commit()

    # print('batchid after save: ',journal.tag_id)
    # createDeferredAccountingEntries(journal,date(year=2023,month=2,day=28))
    # createBillingAccountingEntries(journal)
    # dates = cr[0][30]

    # je_name = journal.name
    # domains = domain + '/app/journal-entry/'+ je_name
    # journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+dates+"</a>"
    # msg = 'A journal entry has been created for Billing Report '+str(posting_date)+'. Please see here '+journal_link
    # title = 'ERPNext: Billing Journal Entry '+str(posting_date)
    # sendEmail(msg,title,journal.doctype,journal.name)

    # return je_name,journal_link

@frappe.whitelist(allow_guest=True)
def importBillingReport():
    doImportBillingReport()
    print('API: Successfully import billing report')
