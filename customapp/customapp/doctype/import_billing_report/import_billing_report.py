# Copyright (c) 2023, mysite and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, date, time, timedelta
import requests, json, os, csv, calendar
from frappe.model.document import Document
from customapp.general_function import *

class ImportBillingReport(Document):
    def before_insert(self):
        global domain 
        domain = getDomain()
        print('csv-------------------------')
        start_date = self.start_date
        end_date = self.end_date
        # isChecked = self.random_seq

        start_date = datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start_date.month == end_date.month:
            month = start_date.month
            year = start_date.year
            days = calendar.monthrange(year=year, month=month)
            last_day = days[1]
            tag_id = date(day=last_day,month=month,year=year)
        else:
            raise Exception('Both Dates Must Be Within Same Month')
        
        # for uat
        cr, batch_id = findFile(start_date,end_date)
        # cr, batch_id = findFile(start_date,end_date,isChecked)
        
        month_name = calendar.month_name[month]

        # while True:
        #     scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing Report'})
        #     if scheduler.field1 == '0':
        #         if scheduler.field2 == '1':
        #             file = frappe.get_last_doc('File',filters={'file_name':'string(13).csv'})
        #             scheduler.field2 = '1'
        #     elif scheduler.field1 == '1':
        #         if scheduler.field2 == '2':
        #             file = frappe.get_last_doc('File',filters={'file_name':'string(14).csv'})
                
                    
        #         file = frappe.get_last_doc('File',filters={'file_name':'string(12).csv'})
                
        #     if scheduler.field1 == 'string(12)':
        #         file = frappe.get_last_doc('File',filters={'file_name':'string(12).csv'})
        #     print('----found')
        #     attach_csv = self.collection_report_csv
        #     attach_csv = file.file_url
        #     # if attach_csv == '':
        #     #     start_date = getDatetime(self.start_date)
        #     #     end_date = getDatetime(self.end_date)
            
        #     #     today = datetime.now().date()
        #     #     if start_date >= today or end_date >= today:
        #     #         raise Exception('Date Cannot be Today or onward!')
            
        #     print('----------------------csv')
        #     # print('domain ',frappe.utils.get_url())
        #     print(attach_csv)
        #     site = frappe.utils.get_site_path()
        #     split = site.split('/')
        #     site = split[1]
        #     attach_csv = site+attach_csv
        #     cr = []
        #     with open(attach_csv,'r') as file:
        #         reader = csv.reader(file)
        #         # print('reader')
        #         # print(reader)
        #         for r in reader:
        #             # print('row: ',r)
        #             cr.append(r)

        #     today = datetime.now().date()

        exist, name,journal_link = checkExist(batch_id,end_date)
        print('--------------EXIST: ',exist)
        if exist:
            raise Exception('Journal Entry of Billing for '+month_name+' is already created. You can see here '+journal_link)


        # importfrombs(start_date, end_date)
        error = False
        error_log_name_list = []
        if len(cr) > 1:
            error,error_log_name_list,error_link = importfrombs(cr)
        if error:
            for log in error_log_name_list:
                self.append('journal_entry_error_log',{
                    'journal_entry_error_log':log,
                })
            frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
        else:
            je_name,journal_links = createJE(cr,end_date,batch_id)
            self.append('journal_entry',{
                'journal_entry':je_name,
            })
            frappe.msgprint('Journal Entries has been created, See Here '+journal_links)


    # def after_insert(self):
    #     start_date = self.start_date
    #     if not isinstance(start_date, str):
    #         start_date = start_date.strftime('%Y-%m-%d')
    #     end_date = self.end_date
    #     if not isinstance(end_date, str):
    #         end_date = end_date.strftime('%Y-%m-%d')

    #     file,filename,path = createcsv(start_date,end_date)

    #     if file == False:
    #         return True
    #     # print('FILENAME1: ',filename)

    #     # file_name = save_file(fname=filename, content=file.read(), dt="attachcsv", dn=self.name)
    #     file_doc = frappe.get_doc({
    #         "doctype": "File",
    #         # "file_url": "/files/"+filename,
    #         "file_name": filename,
    #         # "attached_to_doctype": self.doctype,
    #         # "attached_to_name": self.name,
    #         "content": frappe.read_file(path)
    #     })
    #     # file_doc.insert(ignore_permissions=True)
    #     # file_doc.file_url = "/files/"+filename
    #     file_doc.save()
    #     # print('file url: ',file_doc.file_url)
    #     self.collection_report_csv = file_doc.file_url
    #     return True
    #     pass

def getBatchID(filename):
    split = filename.split('_')
    batchid = split[0]
    return batchid

def makeDict(row,counter):
    # print('counter: ',counter,' val: ',row[15])
    dicts = {
        # 'account':acc,
        'year': row[1],
        'account_number':row[2],
        # 'cost_center': cost,
        'cost_center_number': row[3],
        'currency': row[12],
        'remark': row[23],
        'posting_date': row[30],
        'group': row[31],
        'tax_amount': row[32],
        'tax_code': row[33],
        'profit_or_cost_center_number': row[34],
        'san_count': row[35],
        'monthly_charge': row[36],
        'month_count': row[37],
        'current_month': row[38],
        'is_jb': 1 if row[41] else 0,
    }
    try:
        dicts['revenue_account'] = row[39]
    except:
        # dicts['revenue_account'] = 0
        pass
    # debit
    if counter == 1:
        # acc = frappe.get_last_doc('Account',filters={'account_number'}:row[1])
        # cost = frappe.get_last_doc('Cost Center', filters={'cost_Center_number':row[3]})
        dicts['debit'] = abs(float(row[15]))
    elif counter == 2:
        dicts['credit'] = abs(float(row[15]))
    
    return dicts

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

def findFile(start_date,end_date):
    month = start_date.month

    # if isChecked == 1:
    #     filename = '131_string(13) with rebate.csv'
    #     # file = frappe.get_last_doc('File',filters={'file_name':filename})
    #     cr = getCr(filename)
    if start_date >= date(year=2022,month=12,day=1) and end_date <= date(year=2022,month=12,day=31):
        filename = '12_string(12).csv'
        # file = frappe.get_last_doc('File',filters={'file_name':filename})
        cr = getCr(filename)
        # return
    elif start_date >= date(year=2022,month=11,day=1) and end_date <= date(year=2022,month=11,day=30):
        filename = '100_string(100).csv'
        # file = frappe.get_last_doc('File',filters={'file_name':filename})
        cr = getCr(filename)
        print('lenngth: ',len(cr))
    else:
        # if start_date >= date(year=2023,month=1,day=1) and end_date <= date(year=2023,month=1,day=31):
        cur_month = datetime.now().month
        if month > cur_month:
            raise Exception('Can not Import Billing Report for Next Month!')
        if month == 1:
            filename = '13_string(13) perfect data.csv'
            # file = frappe.get_last_doc('File',filters={'file_name':filename})
            cr = getCr(filename)
        # elif start_date >= date(year=2023,month=2,day=1) and end_date <= date(year=2023,month=2,day=28):
        elif month == 2:
            # template = False
            filename = '14_string(14) perfect data.csv'
            # file = frappe.get_last_doc('File',filters={'file_name':filename})
            # getCrString15(template,'')
            cr = getCr(filename)
        elif month == 3:
            # template = True
            filename = '15_string(15) perfect data.csv'
            # file = frappe.get_last_doc('File',filters={'file_name':filename})
            # template = True
            # cr = getCrString15(template,end_date)
            cr = getCr(filename)
        elif month == 4:
            # template = True
            filename = '16_string(16) perfect data.csv'
            # file = frappe.get_last_doc('File',filters={'file_name':filename})
            # template = True
            # cr = getCrString15(template,end_date)
            cr = getCr(filename)
        else:
            raise Exception('No Report available for the Date!')
    print('----cr------')
    print(cr)
    dict_list = getDict(cr)
    print('---dic list ----')
    print(dict_list)
    batchid = getBatchID(filename)
    return dict_list, batchid

def changeTemplate(cr,new_date):
    site = getSite()
    path = site+'/private/files/'
    filename = 'string(15) perfect data.csv'
    # date_name = getDateOnly(start_date)
    # print('DATE NAME -------------------: ',date_name)
    pathtofile = path+filename

    for row in cr:
        row[30] = new_date

    if os.path.exists(path):
        with open(pathtofile,'w',newline='') as file:
            writer = csv.writer(file)
            for row in cr:
                # print('row: ',row)
                writer.writerow(row)
            print('done1')
    else:
        os.makedirs(path)
        with open(pathtofile,'w',newline='') as file:
            writer = csv.writer(file)
            for row in cr:
                # print('row: ',row)
                writer.writerow(row)
            print('done2')

def getCr(filename):
    print('filename in getcr: ',filename)
    file = frappe.get_last_doc('File', filters={'file_name':filename})
    file_url = file.file_url

    # print(file_url)
    site = frappe.utils.get_site_path()
    split = site.split('/')
    site = split[1]
    file_path = site+file_url
    cr = []
    with open(file_path,'r') as file:
        reader = csv.reader(file)
        # print('reader')
        # print(reader)
        for r in reader:
            # print('row: ',r)
            cr.append(r)

    return cr

def getCrString15(template,new_date):
    str_date = getDateString(new_date)
    if not template:
        new_date = '2023-03-31'
    file_name = 'string(15) perfect data.csv'
    cr = getCr(file_name)
    changeTemplate(cr,str_date)
    return cr

def getDateString(dates):
    if not isinstance(dates, str):
        dates = dates.strftime('%Y-%m-%d')
    return dates

def getSite():
    site = frappe.utils.get_site_path()
    split = site.split('/')
    site = split[1]
    return site


def checkExist(tag_id,end_date):
    try:
        je = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':tag_id})
        # tag_str = tag_id.strftime('%Y-%m-%d')
        # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
        # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
        domains = domain + '/app/journal-entry/'+ je.name
        journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+getDateString(end_date)+"</a>"
        return True, je.name,journal_link
    except Exception as e:
        print('Exception: ',str(e))
        return False, '',''

def createcsv(start_date, end_date):
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.strptime(end_date,'%Y-%m-%d')
    dates = {'start_date':start_date,'end_date':end_date}
    start_date, end_date, year = getIsoDate(dates)
    start_end_year = {'start_date':start_date,'end_date':end_date,'year':year}
    existcr = {}
    ready,cr = getCR(start_end_year,existcr)
    # print('CR: ',cr)
    if not len(cr):
        print('cr start end year: ',start_end_year)
        print('CR is empty')
        raise Exception('Pfile is empty!')
        # user1 = frappe.get_last_doc('User',filters={'username':'csyafiq2iss'})
        # email_args = {
        # 	'recipients':user1.email,
        # 	'message':'msg',
        # 	'subject':'title',
        # 	# 'reference_doctype':errorlog.doctype,
        # 	# 'reference_name':errorlog.name
        # }
        # frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)
        # return False,'',''

    if ready:
        path = 'pfile_report'
        date_name = getDateOnly(start_date)
        # print('DATE NAME -------------------: ',date_name)
        year = str(date_name.year)[-2:]
        month = str(date_name.month)
        if len(month) < 2:
            month = '0'+month

        pathtofile = path+'/PFILE_'+ str(month)+str(year)
        filename = 'PFILE_' + str(month)+str(year)+'.csv'
        # print('FILENAME: ',filename)

        if os.path.exists(path):
            with open(pathtofile,'w',newline='') as file:
                writer = csv.writer(file)
                for row in cr:
                    # print('row: ',row)
                    writer.writerow(row)
        else:
            os.makedirs(path)
            with open(pathtofile,'w',newline='') as file:
                writer = csv.writer(file)
                for row in cr:
                    # print('row: ',row)
                    writer.writerow(row)

        with open(pathtofile,'rb') as file:
            print('return file',' path: ',pathtofile)
            return file, filename, pathtofile

def getDateOnly(start_date):
	date_only = start_date[:10]
	new_date = datetime.strptime(date_only,'%Y-%m-%d')
	year = new_date.year
	day = new_date.day
	month = new_date.month
	new_date = date(year,month,day)
	print('new_date: ',new_date)
	return new_date

def getIsoDate(crdate):
	start_date = crdate['start_date']
	end_date = crdate['end_date']
	year = start_date.year
	times = time(0,0,0)
	start_date = datetime.combine(start_date,times)
	end_date = datetime.combine(end_date,times)
	# print('------type: ',type(start_date))
	start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
	start_date = start_date.isoformat()+"Z"
	# print('++++++++++++++STARTDATE')
	# print(start_date)
	end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
	end_date = end_date.isoformat()+"Z"

	return start_date, end_date, year

def checkError(f1,f2,f3,row,errors,error_list,balance):
    # f1(data), f2(error type), f3(number/string, length), f4(),balance
    # checkExist('Account','account_number',row_list['account_number'],row,error_list,errors)
    field = f1['field']
    val = f1['value']
    error = {
        'row':row,
        'field':field,
        'val':val
    }

    if f2 == 1: # check record existence and ..
        doctype = f1['doctype']
        if f3 == '':
            try:
                obj = frappe.get_last_doc(doctype,filters={field:val})
            except:
                errors['error'] = True
                error['desc'] = 'Invalid Data'
                error_list.append(error)
                # print('error: ',error_list)
        else:
            field2 = f3['field2']
            val2 = f3['val2']
            objs = frappe.get_all(doctype,filters={field2:val2})
            filter_count = 0
            for o in objs:
                if val in o.name:
                    filter_count+=1

            if filter_count < 1:
                errors['error'] = True
                error['desc'] = doctype + ' Not Exist'
                error_list.append(error)
                # print(error_list)

    elif f2 == 2: # check format
        if f3 == 'string':  # only string
            if not val.isdigit():
                return True
            else:
                errors['error'] = True
                error['desc'] = 'Invalid Format'
                error_list.append(error)
                return False
                # print(error_list)
        
        elif f3 == 'number': # only number
            try: 
                val_int = int(val)
                return True
            except:
                # print('type: ',type(val))
                errors['error'] = True
                error['desc'] = 'Invalid Format'
                error_list.append(error)
                return False
                # print(error_list)
            # if f4 != '': # year
            #     year = datetime.now().year
            #     if int(val) != year:
            #         error['desc'] 
            #         error_list.append(error)
        elif f3 == 'float':
            # if not isinstance(val, float):
            try:
                float(val)
                if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
                    # print(val)
                    if val <= 0.0:
                        errors['error'] = True
                        error['desc'] = 'Invalid Value'
                        error_list.append(error)
                        return False
                    return True
                return True
            except:
                errors['error'] = True
                error['desc'] = 'Invalid Format'
                error_list.append(error)
                return False
                # print(error_list)
            # else:
            #     return True


    elif f2 == 3:   # check if follow format eg, length
        if f3 != '':
            valstr = str(val)
            length = len(valstr)
            if length != f3:
                errors['error'] = True
                error['desc'] = 'Invalid Length'
                error_list.append(error)
                # print(error_list)
            else:
                if field == 'current month':
                    month = str(val)[0:2]
                    year = str(val)[2:]
                    if int(month) > 12 or int(month) < 0:
                        errors['error'] = True
                        error['desc'] = 'Invalid Month Value'
                        error_list.append(error)
                        # print(error_list)
                    if int(year) < 0:
                        errors['error'] = True
                        error['desc'] = 'Invalid Year Value'
                        error_list.append(error)
                        # print(error_list)
    
    elif f2 == 4: # check exact value
        # if f3 == 'MYR':
        #     if val != 'MYR':
        #         errors['error'] = True
        #         error['desc'] = 'Invalid Currency'
        #         error_list.append(error)
        if val != f3:
            errors['error'] = True
            if field == 'currency':
                error['desc'] = 'Invalid Currency'
            elif field == 'year':
                error['desc'] = 'Invalid Year'
            error_list.append(error)
            # print(error_list)

    elif f2 == 5: # date for user remark
        current_date = datetime.now().date()
        current_date = current_date.strftime('%y%m%d')
        
        user_date = val[:6]
        # if current_date != user_date:
        #     print('user_date: ',user_date)
        #     print('ccurent_date: ',current_date)
        #     errors['error'] = True
        #     error['desc'] = 'Wrong Date'
        #     error_list.append(error)
            # print(error_list)
        user_year = int(user_date[:2])
        user_month = int(user_date[2:4])
        user_day = int(user_date[4:6])
        if user_month < 0 or user_month > 12:
            errors['error'] = True
            error['desc'] = 'Invalid Date'
            error_list.append(error)
        else:
            first_day, lastday = calendar.monthrange(user_year,user_month)
            if user_day < 0 or user_day > lastday:
                errors['error'] = True
                error['desc'] = 'Invalid Date'
                error_list.append(error)

        # print('year: ',str(int(user_year)),' '+str(int(user_month))+' '+str(int(user_day)))

        user_time = val[-4:]
        hour = int(user_time[:2])
        minute = int(user_time[2:])
        if hour > 23 or hour < 0 or minute > 59 or minute < 0:
            errors['error'] = True
            error['desc'] = 'Invalid Time'
            error_list.append(error)
            # print(error_list)

    elif f2 == 6: # compare to current date
        current_date = datetime.now().date()
        current_date = current_date.strftime('%Y-%m-%d')
        if current_date != val:
            errors['error'] = True
            error['desc'] = 'Wrong Date'
            error_list.append(error)
            # print(error_list)

    elif f2 == 7: # check current_month length
        val_str = str(val)
        length = len(val_str)

        month = 0
        if length == 3:
            month = val_str[:1]
        elif length == 4:
            month = val_str[:2]
        else:
            errors['error'] = True
            error['desc'] = 'Invalid Length'
            error_list.append(error)
            # print(error_list)

        if int(month) <= 0 or int(month) > 12:
            errors['error'] = True
            error['desc'] = 'Invalid Month'
            error_list.append(error)
            # print(error_list)

        year = val_str[-2:]
        if int(year) <= 0:
            errors['error'] = True
            error['desc'] = 'Invalid Year'
            error_list.append(error)
            # print(error_list)

    if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
        # if balance['counter'] == 1:
        #     balance['val'] = abs(val)
        # elif balance['counter'] == 2:
        if balance['counter'] == 2:
            # print('val1: ', balance['val'],' val2: ',val)
            if balance['val'] != val:
                errors['error'] = True
                error['row'] = row
                error['val'] = balance['val']
                if field == 'debit_in_account_currency':
                    error['desc'] = 'Not Balanced With Credit Row '+str(row-1)
                elif field == 'credit_in_account_currency':
                    error['desc'] = 'Not Balanced With Debit Row '+str(row-1)
                print('error1: ',error,' val: ',val,' another: ',balance['val'])
                error_list.append(error)

        # balance = val
        # print('balance: ',balance,' val: ',val)
    #     return balance
    # elif field == 'credit_in_account_currency':
    #     if balance != val:
    #         # print('error row: ',error['row'])
    #         errors['error'] = True
    #         error['row'] = row-1
    #         error['val'] = balance
    #         error['desc'] = 'Not Balanced With Credit Row '+str(row)
    #         error_list.append(error)
    #         err_credit = {'row':row,'field':field,'val':val,'desc':'Not Balanced With Debit Row '+str(row-1)}
    #         # error['row'] = error['row']-1
    #         # error['val'] = val
    #         # error['desc'] = 'Credit Is Not Balanced With Debit Row '+str(row)
    #         error_list.append(err_credit)
            # print(error_list)

def checkEmpty(f1,row,errors,error_list):
    field = f1['field']
    val = f1['value']
    error = {
        'row':row,
        'field':field,
        'val':val
    }

    if val == '':
        errors['error'] = True
        error['desc'] = 'Missing Value'
        error_list.append(error)

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
#     profit_or_cost_center_number = row_list['profit_or_cost_center_number']
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
#     objRevenueAccount = {'field':'revenue_account','value':revenue_account}
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

def getError(row_list,row,error_list,errors,balance):
    year = row_list['year']
    account_number = row_list['account_number']
    cost_center_number = row_list['cost_center_number']
    currency = row_list['currency']
    tax_amount = row_list['tax_amount']
    profit_or_cost_center_number = row_list['profit_or_cost_center_number']
    san_count = row_list['san_count']
    monthly_charge = row_list['monthly_charge']
    month_count = row_list['month_count']
    current_month = row_list['current_month']
    # print('debit credit type: ',type(row_list['debit']))
    # print('debit credit: ',row_list['debit'])
    # print('year: ',year)

    amt_type = ''
    try:
        debit_credit = row_list['debit']
        amt_type = 'debit'
    except:
        debit_credit = row_list['credit']
        amt_type = 'credit'
    remark = row_list['remark']
    posting_date = row_list['posting_date']
    group = row_list['group']

    
    objYear = {'field':'year','value':year}
    objAccount = {'field':'account_number','value':account_number,'doctype':'Account'}
    objCost = {'field':'cost_center_number','value':cost_center_number,'doctype':'Cost Center'}
    objCurrency = {'field':'currency','value':currency}
    objPostingDate = {'field':'posting_date', 'value':posting_date}
    objGroup = {'field':'group','value':group}
    objTaxAmount = {'field':'tax_amount', 'value':tax_amount}
    objProfitOrCostCenterNumber = {'field':'profit_or_cost_center_number','value':profit_or_cost_center_number}
    objSanCount = {'field':'san_count','value':san_count}
    objMonthlyCharge = {'field':'monthly_charge','value':monthly_charge}
    objMonthCount = {'field':'month_count','value':month_count}
    objCurrentMonth = {'field':'current_month','value':current_month}
    try:
        revenue_account = row_list['revenue_account']
        objRevenueAccount = {'field':'revenue_account','value':revenue_account}
    except:
        pass
    # objRevenueAccount = {'field':'revenue_account','value':revenue_account,'doctype':'Account'}
    objUserRemark = {'field':'user_remark','value':remark}
    
    # year
    result = True
    checkEmpty(objYear,row,errors,error_list)
    result = checkError(objYear,2,'number',row,errors,error_list,'')  # check number type
    if result:
        current_year = datetime.now().date().year
        checkError(objYear,4,str(current_year),row,errors,error_list,'')  # check current year
    # account
    checkEmpty(objAccount,row,errors,error_list)
    checkError(objAccount,2,'number',row,errors,error_list,'')  # check number type
    checkError(objAccount,1,'',row,errors,error_list,'')    # check exist
    # # cost center
    checkEmpty(objCost,row,errors,error_list)
    checkError(objCost,1,'',row,errors,error_list,'') # check exist
    # #currency
    # checkError(objCurrency,2,'string',row,errors,error_list,'') # check string type
    checkEmpty(objCurrency,row,errors,error_list)
    checkError(objCurrency,4,'MYR',row,errors,error_list,'') # check value MYR
    # # debit
    if amt_type == 'debit':
        f1 = {'field':'debit_in_account_currency','value':float(debit_credit)}
        checkError(f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(f1,row,errors,error_list)
        # balance = checkError(f1,'','',row,errors,error_list,'') # get value
        checkError(f1,'','',row,errors,error_list,balance) # get value
    # credit
    elif amt_type == 'credit':
        f1 = {'field':'credit_in_account_currency','value':abs(float(debit_credit))}
        checkError(f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(f1,row,errors,error_list)
        checkError(f1,'','',row,errors,error_list,balance)  # check balance
    # tax amount
    checkEmpty(objTaxAmount,row,errors,error_list)
    checkError(objTaxAmount,2,'number',row,errors,error_list,'') # check number type
    # tax code
    # second_cost_center_number
    checkEmpty(objProfitOrCostCenterNumber,row,errors,error_list)
    # san_count
    checkEmpty(objSanCount,row,errors,error_list)
    checkError(objSanCount,2,'number',row,errors,error_list,'') # check number type
    # monthly charge
    checkEmpty(objMonthlyCharge,row,errors,error_list)
    checkError(objMonthlyCharge,2,'number',row,errors,error_list,'') # check number type
    # month count
    checkEmpty(objMonthCount,row,errors,error_list)
    checkError(objMonthCount,2,'number',row,errors,error_list,'') # check number type
    # current month
    checkError(objCurrentMonth,7,'',row,errors,error_list,'')      
    checkEmpty(objCurrentMonth,row,errors,error_list)
    checkError(objCurrentMonth,2,'number',row,errors,error_list,'') # check number type
    # revenue account
    # checkEmpty(objRevenueAccount,row,errors,error_list)
    # checkError(objRevenueAccount,1,'',row,errors,error_list,'')    # check exist
    # # user remark
    checkEmpty(objUserRemark,row,errors,error_list)
    # split = user_remark.split(' / ')
    # print('------------user remark: ',user_remark)
    # bank_account = split[0]
    # user_date = split[1]
    # objURaccount = {'field':'account_name','value':bank_account,'doctype':'Account'}
    # checkEmpty(objURaccount,row,errors,error_list)
    # objParentAccount = {'field2':'parent_account','val2':'Bank - I'}
    # checkError(objURaccount,1,objParentAccount,row,errors,error_list,'') # check bank account exist
    # objURdate = {'field':'user_remark','value':user_date}
    # checkError(objURdate,5,'',row,errors,error_list,'')
    # # posting date
    # checkError(objPostingDate,6,'',row,errors,error_list,'')

    return balance  


def handleError(cr):
    # print('CR:')
    # print(cr)
    error_list = []
    counter = 1
    row_count = 0
    errors = {}
    posting_date_list = []
    group_list = []
    # rows = cr['cr']
    balance_counter = 1
    balance = {'val':0,'counter':balance_counter}
    for row in cr:
        # debit
        # try:
        #     row['debit']
        #     counter = 1
        # except:
        #     counter = 2

        row_count += 1
        posting_date = row['posting_date']
        group = row['group']

        posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
        posting_date_list.append(posting_dates)
        groups = {'row':row_count,'field':'group','val':group}
        group_list.append(groups)
            
        # if counter == 1:
        balance['counter'] = balance_counter
        getError(row,row_count,error_list,errors,balance)

        if balance_counter == 1:
            try:
                balance['val'] = row['debit']
            except:
                balance['val'] = row['credit']
            balance_counter = 2

        elif balance_counter == 2:
            # balance['counter'] = balance_counter
            getError(row,row_count,error_list,errors,balance)
            balance_counter = 1
            


    # check posting date dominant error
    # checkDominant(posting_date_list,errors,error_list)
    # check group dominant error
    checkDominant(group_list,errors,error_list)
    
    if not len(errors):
        # print('no error')
        # print('error_list: ',error_list)
        return False,error_list
    else:
        # print('errors: ',errors)
        print('errors')
        for p in error_list:
            print(p)
        return True,error_list

def getDatetime(dates):
    if isinstance(dates, str):
        # print('------dates: ',dates)
        dates = datetime.strptime(dates, '%Y-%m-%d')
        dates = dates.date()

    return dates

def getDate(start_date,end_date):
	start_date = getDatetime(start_date)
	end_date = getDatetime(end_date)
	year = start_date.year
	times = time(0,0,0)
	start_date = datetime.combine(start_date,times)
	end_date = datetime.combine(end_date,times)
	start_date = start_date + timedelta(hours=0,minutes=0,seconds=0)
	start_date = start_date.isoformat()+"Z"
	print('++++++++++++++STARTDATE')
	print(start_date)
	end_date = end_date + timedelta(hours=23,minutes=59,seconds=59)
	end_date = end_date.isoformat()+"Z"

	return start_date, end_date, year

def getMonth(dates):
    if isinstance(dates, str):
        dates = datetime.strptime(dates, '%Y-%m-%d')
        dates = dates.date()
    
    month = dates.strftime('%B')
    print('month: ',month)
    return month
                
def getCR(start_end_year,existcr):
	start_date = start_end_year['start_date']
	end_date = start_end_year['end_date']
	year = start_end_year['year']
	reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextPFileMthEndJob'})
	# reqUrl = "http://175.136.236.153:8106/api/RptCashReceiptSummary"
	reqUrl = reportcr.url +reportcr.api_key
	print('reqURL: ',reqUrl)

	payload = json.dumps({
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
	# print(cr)
	# return True,cr
	if 'filename=string.csv.tmp' in msg:
		existcr['exist'] = False
		return False,''
		# raise Exception('The file you are trying to get is not in CSV format. Please try again later.')
	else:
		textt = response.content.decode('utf-8')
		cr = csv.reader(textt.splitlines(), delimiter=',')
		cr = list(cr)
		# print('++++++++CR LENGTH: ',len(cr))
		if not len(cr):
			return False, cr
		# print('========cr=========:',cr)
		return True,cr  

def checkReadyCR(start_date,end_date):
    startdate,enddate,year = getDate(start_date,end_date)
    start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
    existcr = {}
    ready,cr = getCR(start_end_year,existcr)

    if not len(existcr):
        return True,cr
    else:
        return False,cr

    # dates_list = []
    # start_end_year = {}

    # if much:
    #     diff = end_date - start_date
    #     diff_day = diff.days + 1
	# 	# print('startdaate: ',start_date)
    #     counter = 0

    #     for i in range(diff_day):
    #         if i == 0:
    #             startdate = enddate = start_date
    #             # date_dic = {'start_date':startdate,'end_date':enddate}
    #             startdate,enddate,year = getDate(startdate,enddate)
    #             start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
    #             # date_dic = {'start_date':startdate,'end_date':enddate}
    #             dates_list.append(start_end_year)
    #             counter += 1
    #         else:
    #             next_date = start_date + timedelta(days=counter)
    #             counter += 1
    #             startdate = enddate = next_date
    #             date_dic = {'start_date':startdate,'end_date':enddate}
    #             startdate,enddate,year = getDate(startdate,enddate)
    #             start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}
    #             dates_list.append(start_end_year)

    #     # print('---------DATE LIST')
    #     # print(dates_list)
    # else:
    #     # date_dic = {'start_date':start_date,'end_date':end_date}
    #     startdate,enddate,year = getDate(start_date,end_date)
    #     start_end_year = {'start_date':startdate,'end_date':enddate,'year':year}

    # existcr = {}
    # cr_ready = []
    # cr_notready = []
    # if much:
    #     for d in dates_list:
    #         ready,cr = getCR(d,existcr)
    #         if cr == '':
    #             print('KOSONGGGG')
    #         else:
    #             print('TAK KOSONGGGG')
    #         if ready:
    #             cr_start = {'cr':cr,'date':d['start_date']}
    #             cr_ready.append(cr_start)
    #         else:
    #             cr_notready.append(d['start_date'])
    #     if not len(existcr):
    #         return True,cr_ready,cr_notready
    #     else:
    #         return False,cr_ready,cr_notready
    # else:
    #     # print('====date_dic====')
    #     # print(date_dic)
    #     ready,cr = getCR(start_end_year,existcr)
    #     # if len(cr) == 0:
    #     #     print('KOSONGSSS')
    #     # else:
    #     #     print('TAK KOSONGSSS')
    #     #     print(cr)
    #     # print('CR IN CHECKREADY: ',cr)
    #     cr_start = {'cr':cr,'date':start_end_year['start_date']}
    #     cr_ready.append(cr_start)
    #     # print('CR-DATE')
    #     # print(cr_date)
    #     if ready:
    #         return True,cr_ready,''
    #     else:
    #         return False,cr_ready,''

def createErrorLog(much,error_list,errordate):
    if not isinstance(errordate,str):
        errordate = errordate.strftime('%Y-%m-%d')
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
            'row':e['row'],
            'field':e['field'],
            'value':e['val'],
            'description':e['desc']
        })
    errorlog.save()
    # print('name:: ',errorlog.name)

    domains = domain + '/app/billing-journal-entry-error-log/'+ errorlog.name
    error_link = "<a href='"+domains+"' target='_blank'>Error Log "+str(errordate_str)+"</a>"
    msg = 'A billing journal entry error log has been made for Billing Report '+str(errordate)+'. Please see here '+error_link
    title = 'ERPNext: Billing Journal Entry Error Log '+str(errordate)
    sendEmail(msg,title,errorlog.doctype,errorlog.name)
    
    if not much:
        # frappe.msgprint('There is error(s) when trying to import the Collection Report. You can see the list here ' +error_link)
        return error_link,errorlog.name
    else:
        return error_link,errorlog.name

# def importfrombs(start_date, end_date,cr):
def importfrombs(cr):
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
    cr_date = cr[0]['posting_date']
    cr_date = datetime.strptime(cr_date, '%Y-%m-%d').date()
        
    # cr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    error_log_name_list = []
    journal_entry_name_list = []
	# journal_entry_link = []
    print('test1111')
    error_result, error_list = handleError(cr)
    print('ERROR RESULT: ',error_result)
    # print('ERROR LIST: ', error_list)
    # print('LENGTH CR: ',len(cr))
    # print('----------------------CR: ',cr)
    # cr_date = cr[0][30]
    # print('CRRRR DATEEEE: ',cr_date)

    if error_result == True:
        error_link,error_name = createErrorLog(False,error_list,cr_date)
        error_log_name_list.append(error_name)
        # frappe.msgprint('There is error when trying to import the Collection Report. You can see the error here ' +error_link)
        return error_result,error_log_name_list,error_link
    return error_result,'',''

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

def getCurrentMonthStr():
    today = datetime.now().date()
    month = today.strftime('%m')
    year = today.strftime('%y')
    currentmonth = month+year
    return currentmonth

# def createTagID():
#     today = datetime.now().date()
#     month = today.strftime('%B')
#     tagid = month +' - '+'Billing 001'
#     return tagid

# def updateTagID(tag):
#     split = tag.split(' ')
#     num = split[2]
#     num_int = int(num)
#     num_str = str(num_int)
#     if len(num_str) < 2:
#         num_str = '00'+num_str
#     elif len(num_str) < 3:
#         num_str = '0'+num_str

#     tag = split[0] +' '+ split[1] +' '+ num_str

#     return tag

# def createAccountingEntries(journal,cr,end_date):
#     latest_posting = date(day=1,month=1,year=1900)
#     posting_date = ''

#     if len(cr) < 2:
#         # now = datetime.now().strftime('%Y-%m-%d')
#         # new_date = datetime.strptime(now, '%Y-%m-%d').date() + timedelta(days=1)
#         # journal.posting_date = new_date         # erpnext set date to one day before posting_date, so need to add 1 day to get present date
#         # tag_id = getDateOnly(dates)
#         # tag_id_str = tag_id.strftime('%Y-%m-%d')
#         journal.tag_id = end_date
#         journal.posting_date = end_date
#         je_name = 'Billing - '+str(end_date)
#         journal.title = je_name
#         journal.noaccount = 'No Current Month Import Data For This Month'
#         journal.save()
#         domains = domain + '/app/journal-entry/'+ journal.name
#         journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+str(end_date)+"</a>"
#         # frappe.msgprint('One Journal Entry has been created, See Here ')
#         msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
#         title = 'ERPNext: Journal Entry '+str(posting_date)
#         return je_name,journal_link
#     else:
#         counter = 1
#         total_debit = 0
#         total_credit = 0
        
#         for row in cr:
#             # debit
#             # print('ROW')
#             # print(row)
#             # row_list = []
#             try:
#                 row['debit']
#                 counter = 1
#             except:
#                 counter = 2

#             posting_date = getDatetime(row['posting_date'])
#             if latest_posting < posting_date:
#                 latest_posting = posting_date

#             if counter == 1:
                
#                 debit_acc = frappe.get_last_doc("Account", filters={"account_number":row['account_number']})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['cost_center_number']})
#                 row['account'] = debit_acc.name
#                 row['cost_center'] = cost_center.name
#                 total_debit += float(row['debit'])
#                 # print('total_debit: ',total_debit)
#                 # print('----debit: ',row['debit'])
#                 row['debit_in_account_currency'] = row['debit']
                
#             # credit
#             elif counter == 2:
#                 counter = 1
                

#                 credit_acc = frappe.get_last_doc("Account", filters={"account_number":row['account_number']})
#                 cost_center = frappe.get_last_doc("Cost Center", filters={"cost_center_number":row['cost_center_number']})
#                 total_credit += float(row['credit'])
#                 row['account'] = credit_acc.name
#                 row['cost_center'] = cost_center.name
#                 # print('----credit: ',row['credit'])
#                 row['credit_in_account_currency'] = row['credit']
                


#         # --------------------------------------logic for deferred and revenue----------------
#             # for l in last_acc_list:
#             #     if row_list[0].account_number == l[0].account_number:
#             #         if row_list[1].account_number == l[1].account_number:
#             #             # update first row of last
#             #             updateLastRow(journal,l[0],1,1)
#             #             # update second row of last
#             #             updateLastRow(journal,l[1],1,-1)
#             #             # update third row of last
#             #             updateLastRow(journal,l[2],2,1)
#             #             # update fourth row of last
#             #             updateLastRow(journal,l[3],2,-1)

#             #             # create first new row
#             #             createNewRow(journal,row_list[0])
#             #             # create first new row
#             #             createNewRow(journal,row_list[1])
        
#         # --------------------------------------logic for deferred and revenue----------------
#             journal.append('accounts',row)

#         now = datetime.now().date()
#         journal.total_debit = total_debit
#         journal.total_credit = total_credit
#         journal.entry_type = "Journal Entry"
        
#         journal.posting_date = latest_posting
#         # print('--------------POSTING DATE: ',posting_date)
#         month = getMonth(posting_date)
#         year = latest_posting.year
#         tag_id = getDatetime(posting_date)

#         tag_id_str = tag_id.strftime('%Y-%m-%d')
#         journal.tag_id = tag_id
#         journal.save()
#         # journal.submit()
#         company = frappe.get_last_doc('Company',filters={'company_name':journal.company})
#         # journal.title = journal.report_type + ' - '+month+' '+str(year)
#         journal.title = 'Billing - '+str(posting_date)
#         # journal.save()
#         # journal.submit()
#         je_name = journal.name
#         # print('je_name: ',je_name)

#         domains = domain + '/app/journal-entry/'+ je_name
#         journal_link = "<a href='"+domains+"' target='_blank'>Billing Journal Entry "+tag_id_str+"</a>"
#         # frappe.msgprint('One Journal Entry has been created, See Here ')
#         msg = 'A journal entry has been made for Collection Report '+str(posting_date)+'. Please see here '+journal_link
#         title = 'ERPNext: Journal Entry '+str(posting_date)
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

# def doLogicDeferred(dje_list):
#     new_list = [] # accounting entries that needed to be added to JE last month
#     update_list = []
#     counter = 1
#     revenue_counter = 0
#     row_1 = {}
#     row_2 = {}
#     isBegin = True
#     seq = 0
#     isDebitFirst = False

#     i = -1

#     for row in dje_list:
#         i += 1
#         if isBegin:
#             counter = 2
#             isDebitFirst = False
#             if row['debit_in_account_currency'] == 0:
#                 counter = 1
#                 isDebitFirst = True
#             isBegin = False
#             revenue_counter = 0
#             seq = 1

#         if revenue_counter == 0:
#             if seq == 2:
#                 revenue_counter = 1

#             if counter == 1:
#                 if seq == 1:
#                     seq = 2
#                     counter = 2

#                 deferred_revenue, row = doCalculate(row,1)
#                 row['debit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row1 = row.copy()
#                 deferred_revenue2, row_1 = doCalculate(row1,2)
#                 row_1['debit_in_account_currency'] = deferred_revenue2
#                 row_1['credit_in_account_currency'] = 0

#             elif counter == 2:
#                 if seq == 1:
#                     seq = 2
#                     counter = 1

#                 deferred_revenue, row = doCalculate(row,1)
#                 row['credit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row2 = row.copy()
#                 deferred_revenue2, row_2 = doCalculate(row2,2)
#                 row_2['credit_in_account_currency'] = deferred_revenue2
#                 row_2['debit_in_account_currency'] = 0
            
            

#         # if revenue_counter == 1:
#         #     revenue_counter = 0
#         #     isBegin = True
#         #     seq = 0
#         #     if isDebitFirst:
#         #         row_1['account_number'] = row_2['account_number']
#         #         row_1['account'] = row_2['account']
#         #     row_1['cost_center_number'] = row_2['cost_center_number']
#         #     row_1['cost_center'] = row_2['cost_center']
#         #     row_2['revenue_account'] = None
#         #     row_2['account_number'] = row_1['revenue_account']
#         #     acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#         #     row_2['account'] = acc.name
#         #     row_1['month_count'] = 1
#         #     row_2['month_count'] = 1

#         #     new_list.append(row_1)
#         #     new_list.append(row_2)

#         if revenue_counter == 1:
#             revenue_counter = 0
#             isBegin = True
#             seq = 0

#             if isDebitFirst:
#                 row_1['account_number'] = row_2['account_number']
#                 row_1['account'] = row_2['account']

#                 cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
#                 row_1['cost_center_number'] = row_2['cost_center_number']
#                 # row_1['cost_center'] = row_2['cost_center']
#                 # change
#                 row_1['cost_center'] = cost_center.name
#                 row_2['cost_center'] = cost_center.name

#                 row_2['revenue_account'] = None
#                 row_2['account_number'] = row_1['revenue_account']
#                 acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#                 row_2['account'] = acc.name
#                 row_1['month_count'] = 1
#                 row_2['month_count'] = 1
#             else:
#                 row_2['account_number'] = row_1['account_number']
#                 row_2['account'] = row_1['account']
#                 # change
#                 cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
#                 row_1['cost_center'] = cost_center.name
#                 row_2['cost_center'] = cost_center.name

#                 row_2['cost_center_number'] = row_1['cost_center_number']
#                 row_2['cost_center'] = row_1['cost_center']
#                 row_1['revenue_account'] = None
#                 row_1['account_number'] = row_2['revenue_account']
#                 acc = frappe.get_last_doc('Account',filters={'account_number':row_1['account_number']})
#                 row_1['account'] = acc.name
#                 row_2['month_count'] = 1
#                 row_1['month_count'] = 1
#             # row_1['cost_center_number'] = row_2['cost_center_number']
#             # row_1['cost_center'] = row_2['cost_center']
#             # row_2['revenue_account'] = None
#             # row_2['account_number'] = row_1['revenue_account']
#             # acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#             # row_2['account'] = acc.name
#             # row_1['month_count'] = 1
#             # row_2['month_count'] = 1

#             new_list.append(row_1)
#             new_list.append(row_2)
#     return new_list

# def doLogicDeferred(dje_list):
#     print('------------pop')
#     for d in dje_list:
#         print(d)
#         print('\n\n')
#     new_list = [] # accounting entries that needed to be added to JE last month
#     update_list = []
#     counter = 1
#     revenue_counter = 0
#     row_1 = {}
#     row_2 = {}
#     isBegin = True
#     seq = 0
#     isDebitFirst = False

#     i = -1

#     for row in dje_list:
#         i += 1
#         if isBegin:
#             counter = 2
#             isDebitFirst = False
#             if row['credit_in_account_currency'] == 0.0:
#                 counter = 1
#                 isDebitFirst = True
#                 print('debit: ',row['debit_in_account_currency'],' credit: ',row['credit_in_account_currency'])
#                 print('type: ',type(row['credit_in_account_currency']))
#             isBegin = False
#             revenue_counter = 0
#             seq = 1

#         if revenue_counter == 0:
#             if seq == 2:
#                 revenue_counter = 1

#             if counter == 1:
#                 if seq == 1:
#                     seq = 2
#                     counter = 2

#                 deferred_revenue, row = doCalculate(row,1)
#                 row['debit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row1 = row.copy()
#                 deferred_revenue2, row_1 = doCalculate(row1,2)
#                 row_1['debit_in_account_currency'] = deferred_revenue2
#                 row_1['credit_in_account_currency'] = 0

#             elif counter == 2:
#                 if seq == 1:
#                     seq = 2
#                     counter = 1

#                 deferred_revenue, row = doCalculate(row,1)
#                 row['credit_in_account_currency'] = deferred_revenue
#                 update_list.append(row)
#                 row2 = row.copy()
#                 deferred_revenue2, row_2 = doCalculate(row2,2)
#                 row_2['credit_in_account_currency'] = deferred_revenue2
#                 row_2['debit_in_account_currency'] = 0
            
            

#         # if revenue_counter == 1:
#         #     revenue_counter = 0
#         #     isBegin = True
#         #     seq = 0
#         #     if isDebitFirst:
#         #         row_1['account_number'] = row_2['account_number']
#         #         row_1['account'] = row_2['account']
#         #     row_1['cost_center_number'] = row_2['cost_center_number']
#         #     row_1['cost_center'] = row_2['cost_center']
#         #     row_2['revenue_account'] = None
#         #     row_2['account_number'] = row_1['revenue_account']
#         #     acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#         #     row_2['account'] = acc.name
#         #     row_1['month_count'] = 1
#         #     row_2['month_count'] = 1

#         #     new_list.append(row_1)
#         #     new_list.append(row_2)

#         if revenue_counter == 1:
#             revenue_counter = 0
#             isBegin = True
#             seq = 0

#             if isDebitFirst:
#                 row_1['account_number'] = row_2['account_number']
#                 row_1['account'] = row_2['account']

#                 cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
#                 row_1['cost_center_number'] = row_2['cost_center_number']
#                 # row_1['cost_center'] = row_2['cost_center']
#                 # change
#                 row_1['cost_center'] = cost_center.name
#                 row_2['cost_center'] = cost_center.name

#                 row_2['revenue_account'] = None
#                 row_2['account_number'] = row_1['revenue_account']
#                 acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#                 row_2['account'] = acc.name
#                 row_1['month_count'] = 1
#                 row_2['month_count'] = 1

#                 new_list.append(row_1)
#                 new_list.append(row_2)
#                 print('isdebitfirst true')
#             else:
#                 row_2['account_number'] = row_1['account_number']
#                 row_2['account'] = row_1['account']
#                 # change
#                 cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
#                 row_1['cost_center'] = cost_center.name
#                 row_2['cost_center'] = cost_center.name

#                 row_2['cost_center_number'] = row_1['cost_center_number']
#                 # row_2['cost_center'] = row_1['cost_center']
#                 row_1['revenue_account'] = None
#                 row_1['account_number'] = row_2['revenue_account']
#                 acc = frappe.get_last_doc('Account',filters={'account_number':row_1['account_number']})
#                 row_1['account'] = acc.name
#                 row_2['month_count'] = 1
#                 row_1['month_count'] = 1
#             # row_1['cost_center_number'] = row_2['cost_center_number']
#             # row_1['cost_center'] = row_2['cost_center']
#             # row_2['revenue_account'] = None
#             # row_2['account_number'] = row_1['revenue_account']
#             # acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
#             # row_2['account'] = acc.name
#             # row_1['month_count'] = 1
#             # row_2['month_count'] = 1

#                 new_list.append(row_2)
#                 new_list.append(row_1)
#                 print('isdebitfirst false')
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
                # print('-=-=-=-=-= row1 new_cc: ',row1['new_cost_center'])
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
                print('---lalalala---- ',row_1['new_cost_center'])
                # cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
                cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['new_cost_center']})
                print('-----lalala2222-----')
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
                # cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['profit_or_cost_center_number']})
                cost_center = frappe.get_last_doc('Cost Center',filters={'cost_center_number':row_1['new_cost_center']})
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


def getRM(price):
    if not isinstance(price, str):
        price = str(price)
    if '.' in price:
        split = price.split('.')
        if len(split[1]) < 2:
            split[1] = '00'
            price = 'RM '+split[0]+'.'+split[1]
        else:
            price = 'RM '+price
    else:
        price = 'RM '+price+'.00'
    print('price: ',price)
    return price

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

def getPreviousDate(dates):
    if isinstance(dates, str):
        dates = datetime.strptime(dates,'%Y-%m-%d')
    
    month = dates.month
    year = dates.year
    month-=1
    if month <= 0:
        month = 12
        year -=1
    days = calendar.monthrange(year,month)
    prev_date = date(day=days[1],month=month,year=year)
    return prev_date

# def createDeferredAccountingEntries(journal,new_date):
#     prev_date = getPreviousDate(new_date)
#     print('-------prev_date: ',prev_date)
#     deferreds = frappe.get_list('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
#     if not deferreds:
#         print('No Deferred Found for ',getDateString(prev_date))
#         return
#     else:
#         deferred = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
#     acc = deferred.accounts
#     counter = 1
#     dr = []
#     for row in acc:
#         if counter == 1:
#             counter +=1
#             rows_dict = {
#                 'account':row.account,
#                 'account_number':row.account_number,
#                 'cost_center':row.cost_center,
#                 'cost_center_number':row.cost_center_number,
#                 # 'cost_center':cost_center.name,
#                 'currency':row.currency,
#                 'debit_in_account_currency' : float(row.debit),
#                 'credit_in_account_currency' : float(0),
#                 'remark':row.remark,
#                 'group':row.group,
#                 'year': row.year,
#                 'posting_date':row.posting_date,
#                 'tax_amount':row.tax_amount,
#                 'tax_code':row.tax_code,
#                 'profit_or_cost_center_number':row.profit_or_cost_center_number,
#                 'san_count':row.san_count,
#                 'monthly_charge':row.monthly_charge,
#                 'month_count':row.month_count,
#                 'current_month':row.current_month,
#                 'revenue_account':row.revenue_account,
#                 'journal_entry':row.journal_entry
#             }
#             dr.append(rows_dict)
#         elif counter == 2:
#             counter = 1
#             rows_dict = {
#                 'account':row.account,
#                 'account_number':row.account_number,
#                 'cost_center':row.cost_center,
#                 'cost_center_number':row.cost_center_number,
#                 # 'cost_center':cost_center.name,
#                 'currency':row.currency,
#                 'debit_in_account_currency' : float(0),
#                 'credit_in_account_currency' : float(row.credit),
#                 'remark':row.remark,
#                 'group':row.group,
#                 'year': row.year,
#                 'posting_date':row.posting_date,
#                 'tax_amount':row.tax_amount,
#                 'tax_code':row.tax_code,
#                 'profit_or_cost_center_number':row.profit_or_cost_center_number,
#                 'san_count':row.san_count,
#                 'monthly_charge':row.monthly_charge,
#                 'month_count':row.month_count,
#                 'current_month':row.current_month,
#                 'revenue_account':row.revenue_account,
#                 'journal_entry':row.journal_entry
#             }
#             dr.append(rows_dict)
    
#     new_list = doLogicDeferred(dr)
#     counter = 1
#     total_debit = 0
#     total_credit = 0
#     print('new list: ')
#     print(new_list)
#     for row in new_list:
#         if counter == 1:
#             counter +=1
#             total_debit += row['debit_in_account_currency']
#         elif counter == 2:
#             counter = 1
#             total_credit += row['credit_in_account_currency']
#         journal.append('deferred_accounts',row)
#     # print('dr: ',dr)   

#     if len(new_list):
#         journal.total_deferred_debit = getRM(total_debit)
#         journal.total_deferred_credit = getRM(total_credit)
#     print('Done Create ')
  
# def createDeferredAccountingEntries(journal,new_date):
#     prev_date = getPreviousDate(new_date)
#     print('-------prev_date: ',prev_date,' type: ',type(prev_date))
#     deferreds = frappe.get_list('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
#     if not deferreds:
#         print('No Deferred Found for ',getDateString(prev_date))
#         return
#     else:
#         deferred = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'tag_id':prev_date})
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
        
#     print('------popppppppppoooooopppppppppppp')
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
#                     'journal_entry':row.journal_entry,
#                     'new_cost_center':row.new_cost_center
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
#                     'journal_entry':row.journal_entry,
#                     'new_cost_center':row.new_cost_center
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

  
# def createJE(cr,end_date,batch_id):
#     journal = frappe.new_doc("Journal Entry")
#     journal.report_type = 'Billing'
#     posting_date = ''
#     # print('CRRRR')
#     # print(cr)
#     print('LENGTH: ',len(cr))
#     latest_posting = date(day=1,month=1,year=1900)
#     je_name, journal_link = createAccountingEntries(journal,cr,end_date)
#     # print('journal_link: ',journal_link)
#     createDeferredAccountingEntries(journal,end_date)
#     journal.save()
#     journal.tag_id = batch_id
#     journal.submit()
#     frappe.db.commit()
#     # createDeferredAccountingEntries(journal,date(year=2023,month=2,day=28))
#     # createBillingAccountingEntries(journal)
#     # dates = cr[0][30]

#     # je_name = journal.name
#     # domains = domain + '/app/journal-entry/'+ je_name
#     # journal_link = "<a href='"+domains+"' target='_blank'>Journal Entry "+dates+"</a>"
#     # msg = 'A journal entry has been created for Billing Report '+str(posting_date)+'. Please see here '+journal_link
#     # title = 'ERPNext: Billing Journal Entry '+str(posting_date)
#     # sendEmail(msg,title,journal.doctype,journal.name)

#     return je_name,journal_link

def createJE(cr,end_date,batch_id):
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
    # msg = 'A journal entry has been created for Billing Report '+str(posting_date)+'. Please see here '+journal_link
    # title = 'ERPNext: Billing Journal Entry '+str(posting_date)
    # sendEmail(msg,title,journal.doctype,journal.name)

    return je_name,journal_link
