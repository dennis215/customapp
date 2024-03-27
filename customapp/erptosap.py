import frappe
from datetime import datetime, date, time, timedelta
import json, requests, csv, os, calendar
from frappe.utils.csvutils import UnicodeWriter
from frappe.utils import cstr
from ftplib import FTP
import io

def getRow(accounts,row_list,tag_id,isCollection):
    current_datetime=getDateTimeString()
    tag = True
    counter = 1
    for a in accounts:
        # split_remark = a.remark.split('/')
        # first_half_remark = split_remark[0].strip()
        # remarks = first_half_remark + "/ "+current_datetime
        if(a.debit_in_account_currency==0):
            counter=2
        else:
            counter=1
        print('account: ',a.name)
        if counter == 1:
            if isCollection:
                row = {
                    'year':a.year,
                    'account_number':a.account_number,
                    'cost_center_number':a.cost_center_number,
                    'currency':a.currency,
                    'debit':a.debit_in_account_currency,
                    'remark':a.remark,
                    'group':a.group,
                    'posting_date':a.posting_date,
                    'is_jb':a.is_jb,
                    'profit_or_cost_center_number':a.profit_or_cost_center_number,
                }
            else:
                row = {
                    'year':a.year,
                    'account_number':a.account_number,
                    'cost_center_number':a.cost_center_number,
                    'currency':a.currency,
                    'debit':a.debit_in_account_currency,
                    'remark':a.remark,
                    'group':a.group,
                    'posting_date':a.posting_date,
                    'tax_amount':a.tax_amount,
                    'tax_code':a.tax_code,
                    'profit_or_cost_center_number':a.profit_or_cost_center_number,
                    'san_count':a.san_count,
                    'monthly_charge':a.monthly_charge,
                    'month_count':a.month_count,
                    'current_month':a.current_month,
                    'is_jb':a.is_jb,
                }
            if tag:
                row['tag_id'] = tag_id
            print('----------debit-----------------')
            print(row)
            # print('row 1: ',row)
            row_list.append(row)
        
        elif counter == 2:
            if isCollection:
                row = {
                    'year':a.year,
                    'account_number':a.account_number,
                    'cost_center_number':a.cost_center_number,
                    'currency':a.currency,
                    'credit':a.credit_in_account_currency,
                    'remark':a.remark,
                    'group':a.group,
                    'posting_date':a.posting_date,
                    'is_jb':a.is_jb,
                    'profit_or_cost_center_number':a.profit_or_cost_center_number,
                }
            else:
                row = {
                    'year':a.year,
                    'account_number':a.account_number,
                    'cost_center_number':a.cost_center_number,
                    'currency':a.currency,
                    'credit':a.credit_in_account_currency,
                    'remark':a.remark,
                    'group':a.group,
                    'posting_date':a.posting_date,
                    'tax_amount':a.tax_amount,  
                    'tax_code':a.tax_code,
                    'profit_or_cost_center_number':a.profit_or_cost_center_number,
                    'san_count':a.san_count,
                    'monthly_charge':a.monthly_charge,
                    'month_count':a.month_count,
                    'current_month':a.current_month,
                    'is_jb':a.is_jb,
                }
            if tag:
                row['tag_id'] = tag_id
            # print('row 2: ',row)
            print('----------credit-----------------')
            print(row)
            row_list.append(row)

def getDate(dates):
    dates = datetime.strptime(dates, '%Y-%m-%d')
    dates = dates.date()
    return dates

def getDateString(dates):
    dates = dates.strftime('%Y-%m-%d')
    return dates

def getDateTimeString():
    current_datetime = datetime.now()
    year = current_datetime.strftime("%y")
    month = current_datetime.strftime("%m")
    day = current_datetime.strftime("%d")
    hour = current_datetime.strftime("%H")
    minute = current_datetime.strftime("%M")
    formatted_datetime = year + month + day + hour + minute
    print(formatted_datetime)
    return formatted_datetime

def getAmount(amt):
    try:
        amt_str = str(amt)
    except:
        amt_str = amt
    
    if '.' in amt_str:
        split = amt_str.split('.')
        length = len(split[1])
        if length < 2:
            split[1] = split[1] + '0'
            amt_str = split[0]+'.'+split[1]
    else:
        amt_str +='.00'
    
    # print('amt_str: ',amt_str)
    return amt_str

def getVal(row,counter):
    if counter == 1:
        val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',round((row['debit']), 2),'','',round((row['debit']), 2),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],'','',row['profit_or_cost_center_number'])
        # print('val 1: ',val)
    else:
        val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+str(round((row['credit']), 2)),'','','-'+str(round((row['credit']), 2)),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],'','',row['profit_or_cost_center_number'])
    
    # tag = True
    # if tag:
    #     if counter == 1:
    #         val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',getAmount(row['debit']),'','',getAmount(row['debit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])
    #         # print('val 1: ',val)
    #     else:
    #         val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+getAmount(row['credit']),'','','-'+getAmount(row['credit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])
    
    return val

def getValDeferred(row,isDebit):
    try:
        if isDebit:
            val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',round((row['debit']), 2),'','',round((row['debit']), 2),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],str(row['tax_amount']),str(row['tax_code']),row['profit_or_cost_center_number'])
            # print('val 1: ',val)
        else:
            val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+str(round((row['credit']), 2)),'','','-'+str(round((row['credit']), 2)),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],str(row['tax_amount']),str(row['tax_code']),row['profit_or_cost_center_number'])
        return val
    except Exception as e:
        print('errors: ',e)
    # tag = True
    # if tag:
    #     if counter == 1:
    #         val = ('',str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',getAmount(row['debit']),'','',getAmount(row['debit']),'','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])
    #         # print('val 1: ',val)
    #     else:
    #         val = ('',str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+getAmount(row['credit']),'','','-'+getAmount(row['credit']),'','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])

@frappe.whitelist(allow_guest=True)
def exportCR():
    if frappe.request.method == 'POST':
        data = frappe.request.get_json()
        # print('DATA: ',data)
        start_date = data['start_date']
        end_date = data['end_date']
        # print('start: ',start_date)
        # print('end: ',end_date)

        start_date = getDate(start_date)
        end_date = getDate(end_date)

        if end_date < start_date:
            raise Exception('End date cannot be Earlier than Start Date')

        much = False
        if start_date == end_date:
            journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
            tag_id = journal.tag_id
            accounts = journal.accounts
            # print('accounts: ',accounts)
            row_list = []
            getRow(accounts,row_list,tag_id,1)

            writer = UnicodeWriter()
            counter = 1
            for row in row_list:
                if counter == 1:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter+=1
                elif counter == 2:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter = 1
            
            frappe.response['result'] = writer.getvalue()
            frappe.response['type'] = 'csv'
            frappe.response['doctype'] = 'Journal Entry_'+str(start_date)
        else:
            diff = end_date - start_date
            days = diff.days
            row_list = []

            # the first date
            journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
            accounts = journal.accounts
            tag_id = journal.tag_id
            # print('accounts: ',accounts)
            getRow(accounts,row_list,tag_id,1)

            # rest of the date
            for i in range(days):
                start_date += timedelta(days=1)
                journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
                tag_id = journal.tag_id
                accounts = journal.accounts
                # print('accounts: ',accounts)
                getRow(accounts,row_list,tag_id,1)
            
            # print('ROW LIST: ',row_list)
            print('length: ',len(row_list))
            writer = UnicodeWriter()
            counter = 1
            for row in row_list:
                if counter == 1:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter+=1
                elif counter == 2:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter = 1
            
            frappe.response['result'] = writer.getvalue()
            print('result:')
            print(writer.getvalue())
            frappe.response['type'] = 'csv'
            frappe.response['doctype'] = 'Journal Entry_'+str(start_date)+'--'+str(end_date)

        # print('ROW LIST: ',row_list)
            
@frappe.whitelist(allow_guest=True)
def exportgetCR():
    if frappe.request.method == 'GET':
        # data = frappe.request.get_data()
        start_date = frappe.local.request.args.get('start_date')
        end_date = frappe.local.request.args.get('end_date')
        print('PRINT START DATE: ',start_date)
        print('PRINT END DATE: ',end_date)

        start_date = getDate(start_date)
        end_date = getDate(end_date)

        if end_date < start_date:
            raise Exception('End date cannot be Earlier than Start Date')

        much = False
        if start_date == end_date:
            journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
            accounts = journal.accounts
            tag_id = journal.tag_id
            # print('accounts: ',accounts)
            row_list = []
            getRow(accounts,row_list,tag_id,1)

            writer = UnicodeWriter()
            counter = 1
            for row in row_list:
                if counter == 1:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter+=1
                elif counter == 2:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter = 1
            
            frappe.response['result'] = writer.getvalue()
            frappe.response['type'] = 'csv'
            frappe.response['doctype'] = 'Journal Entry_'+str(start_date)
            print('test')
        else:
            diff = end_date - start_date
            days = diff.days
            row_list = []

            # the first date
            journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
            accounts = journal.accounts
            tag_id = journal.tag_id
            # print('accounts: ',accounts)
            getRow(accounts,row_list,tag_id,1)

            # rest of the date
            for i in range(days):
                start_date += timedelta(days=1)
                journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
                accounts = journal.accounts
                tag_id = journal.tag_id
                # print('accounts: ',accounts)
                getRow(accounts,row_list,tag_id,1)
            
            # print('ROW LIST: ',row_list)
            print('length: ',len(row_list))
            writer = UnicodeWriter()
            counter = 1
            for row in row_list:
                if counter == 1:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter+=1
                elif counter == 2:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter = 1
            
            frappe.response['result'] = writer.getvalue()
            print('result:')
            print(writer.getvalue())
            frappe.response['type'] = 'csv'
            frappe.response['doctype'] = 'Journal Entry_'+str(start_date)+'--'+str(end_date)

        # print('ROW LIST: ',row_list)


# ------------------------------------------export deferred---------------------------------------------         

def getDeferredList(names):
    # journals = frappe.get_list('Journal Entry',filters={'report_type':'Billing','posting_date':dates})
    try:
        # journal = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','posting_date':dates})
        deferred_lists = []
        for name in names:
            journal = frappe.get_last_doc('Journal Entry',filters={'name':name})

            # deferred = journal.deferred_accounts
            deferred = journal.accounts
            # print('je: ',journal.name)
            # print('acc: ',deferred)
            deferred_list = []
            for row in deferred:
                deff = {}
                deff['account_number'] = row.account_number
                deff['cost_center_number'] = row.cost_center_number
                deff['currency'] = row.currency
                deff['debit'] = row.debit_in_account_currency
                deff['credit'] = row.credit_in_account_currency
                deff['remark'] = row.remark
                deff['group'] = row.group
                deff['year'] = row.year
                deff['posting_date'] = row.posting_date
                deff['tax_amount'] = row.tax_amount
                deff['tax_code'] = row.tax_code
                deff['profit_or_cost_center_number'] = row.profit_or_cost_center_number
                deferred_list.append(deff)
            deferred_lists.append(deferred_list)
        return deferred_lists
    except Exception as e:
        print('error: ',e)
        return ''

def getLastDate(dates):
    month = dates.month
    year = dates.year
    days = calendar.monthrange(year,month)
    new_date = date(day=days[1],month=month,year=year)

    return new_date

def getStrp(dates):
    if isinstance(dates, str):
        dates = datetime.strptime(dates, '%Y-%m-%d').date()
    return dates

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
        'reference_doctype':users[0].doctype,
        'reference_name':users[0].name
    }
    frappe.enqueue(method=frappe.sendmail, queue='short',timeout='300',**email_args)


@frappe.whitelist(allow_guest=True)
def exportDeferredRevenue():
    if frappe.request.method == 'POST':
        data = frappe.request.get_json()
        # print('DATA: ',data)
        start_date = data['start_date']
        end_date = data['end_date']


        start_date = getStrp(start_date)
        end_date = getStrp(end_date)
        if start_date.month != end_date.month:
            # return response error
            return 
        
        new_date = getLastDate(start_date)
        # print('new_date: ',new_date)
        account_list = getDeferredList(new_date)
        if account_list == '':
            # raise Exception('Deferred Revenue Does Not Exist Yet')
            print('Deferred Revenue Does Not Exist Yet')
            return
        # else:
        #     print('return')
        # print('list: ',account_list)

        writer = UnicodeWriter()
        counter = 1
        i = 0
        isDebit = False
        for row in account_list:
            i +=1
            isDebit = False
            if row['debit'] != 0:
                isDebit = True
            # if counter == 1:
            if isDebit:
                val = getValDeferred(row,isDebit)
                print('val1: ',val)
                writer.writerow(val)
                counter+=1
            else:
                val = getValDeferred(row,isDebit)
                print('val2: ',val)
                writer.writerow(val)
                counter = 1
        print()
        
        frappe.response['result'] = writer.getvalue()
        frappe.response['type'] = 'csv'
        frappe.response['doctype'] = 'Journal Entry_'+getDateString(start_date)
        print('test: ',getDateString(start_date))
        msg = 'A Deferred Revenue for '+getDateString(start_date)+' has been exported to SAP'
        title = 'ERPNext: Deferred Revenue Export'
        sendEmail(msg,title,'','')

@frappe.whitelist(allow_guest=True)
def exportDeferredRevenueGet():
    if frappe.request.method == 'GET':
        start_date = frappe.local.request.args.get('start_date')
        end_date = frappe.local.request.args.get('end_date')
        print('start_Date: ',start_date)
        
        start_date = getStrp(start_date)
        end_date = getStrp(end_date)
        if start_date.month != end_date.month:
            # return response error
            return 
        
        new_date = getLastDate(start_date)
        account_list = getDeferredList(new_date)
        if account_list == '':
            # raise Exception('Deferred Revenue Does Not Exist Yet')
            print('Deferred Revenue Does Not Exist Yet')
            return
        # else:
        #     print('list: ',account_list )

        writer = UnicodeWriter()
        # counter = 1
        isDebit = False
        for row in account_list:
            isDebit = False
            if row['debit'] != 0.0:
                isDebit = True
            # if counter == 1:
            if isDebit:
                val = getValDeferred(row,isDebit)
                print('val1: ',val)
                writer.writerow(val)
            else:
                val = getValDeferred(row,isDebit)
                print('val2: ',val)
                writer.writerow(val)
                counter = 1
        
        frappe.response['result'] = writer.getvalue()
        frappe.response['type'] = 'csv'
        frappe.response['doctype'] = 'Journal Entry_'+getDateString(start_date)
        print('test: ',getDateString(start_date))
    else:
        print('Wrong Method')

def createcsv2(rows):
    pass

def createcsv(rows):
    alist = []
    print('rows: ',rows)
    print('------stop')
    for row in rows:
        val = ''
        vals = ','+row['account_number']+','+row['cost_center_number']+','
        val = val + vals
        print('val: ',val)
        vals = ',,,,,,,,'+row['currency']+',,,'+row['debitcredit']+',,,'+row['debitcredit']+','
        val = val + vals
        print('val: ',val)
        vals = ',,,,,'+row['user_remark']+',,,,,,,'+row['posting_date']+','+row['group']+','+row['tax_amount']+','+row['tax_code']+','+row['second_cost_center_number']+','
        val = val + vals
        print('val: ',val)
        vals = row['san_count']+','+row['monthly_charge']+','+row['month_count']+','+row['current_month']
        val = val + vals
        print('val: ',val)
        print('-----------')

        alist.append(val)
    
    return alist

def IsJBExported(journal_list):
    for j in journal_list:
        print("all the j")
        print(j)
        try:
            journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
            journal.is_jb_exported = '1'
            journal.save()
            frappe.db.commit()
        except Exception as e:
            print('error: ',e)

def IsExported(journal_list):
    for j in journal_list:
        try:
            journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
            journal.is_exported = '1'
            journal.save()
            frappe.db.commit()
        except Exception as e:
            print('error: ',e)

def uploadToFtpServer(csv_string,filename,server_path):
    try:
        csv_file = io.BytesIO(csv_string.encode('utf-8'))

        hostname = '210.19.60.131'
        username = 'bs'
        password = 'Bs@_IWK2023'
        # filename = 'testCR.csv'
        # if report == 2:
        #     filename = 'testDR.csv'
        # server_path = '/home/bs/dev/'

        ftp = FTP(hostname)
        ftp.set_debuglevel(2)
        ftp.set_pasv(True)
        ftp.login(username, password)
        ftp.cwd(server_path)

        ftp.storlines("STOR "+filename, csv_file)
        
        ftp.quit()
        print('File ',filename,' upload sucessfully!')
    except Exception as e:
        print('Error: ',filename,' Cannot be Uploaded!')

def createCSVExport(value,filename,path):
    csv_string = value.replace('"', '')
    print('------------------csv_string')
    print(csv_string)
    uploadToFtpServer(csv_string,filename,path)

def getFilenameDateString():
    now = frappe.utils.now_datetime()
    year = str(now.year)
    month = str(now.month)
    if len(month) < 2:
        month = '0'+month
    day = str(now.day)
    if len(day) < 2:
        day = '0'+day
    hour = str(now.hour)
    minute = str(now.minute)
    dateString=  year+month+day+hour+minute
    return dateString

    
def getExportFilename(report):
    filename = ''
    if report == 1:
        filename += 'BSCOLL'
    elif report == 2:
        filename += 'BSDEF'
    elif report == 3:
        filename += 'BSBILL'

    # now = datetime.now()
    filename +=getFilenameDateString()
    print('filename: ',filename)

    return filename


def exportCRReportToSAP():
    print('------------------Export CR Report To SAP')
    # if scheduler == 'Collection Report (Export)':
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Collection Report (Export)'})
        if scheduler.report_name == '' or scheduler.report_name is None:
            print('generate file name: ')
            filename = getExportFilename(1)
        else:
            filename = scheduler.report_name
            filename += getFilenameDateString()
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_exported':'0','docstatus':'1'})
                journal_list.append(journal)
            except:
                print('No Collection Report is available to be exported!')
                return
        elif periodic == 'Month End':
            #enable in Staging [1]
            # now = datetime.now()
            # month = now.month
            # months = str(month)
            # if len(str(month)) < 2:
                # months = '0'+str(month)
            # month_filter = '%-'+months+'-%'
            #end of enable [1]

            #disable in Staging [2]
            last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_exported':'0','docstatus':'1'})
            month = last_journal.posting_date.month
            year = last_journal.posting_date.year
            last = calendar.monthrange(year,month)[1]
            str_date = str(year) + '-' + str(month) + '-'
            first_day = str_date + '01'
            last_day = str_date + str(last)
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Collection','is_exported':'0','posting_date':['between',[first_day,last_day]],'docstatus':'1'})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    print('----------journal_list-----------------')
                    print(journal_list)
            else:
                print('No Collection Report is available to be exported!')
                return
        row_lists = []
        for j in journal_list:
            tag_id = j.tag_id
            accounts = j.accounts
            row_list = []
            getRow(accounts,row_list,tag_id,1)
            row_lists.append(row_list)
        
        if len(journal_list) <= 0:
            print('No Journal Entry Found!')
            return
        # Removing entries with 'is_jb': 1
        row_lists = [
            [entry for entry in sublist if entry.get('is_jb', 0) != 1]
            for sublist in row_lists
        ]
        writer = UnicodeWriter()
        combined_array = []
        for rows in row_lists:
            for item in rows:
                combined_array.append(item)
        # Sum up credit and debit
        cumulative_sums = {}
        for entry in combined_array:
            key = (entry['account_number'], entry['cost_center_number'], entry['remark'], entry['group'],entry['profit_or_cost_center_number'])
            if key not in cumulative_sums:
                cumulative_sums[key] = {'year': entry['year'], 'account_number': entry['account_number'], 'cost_center_number': entry['cost_center_number'], 'currency': entry['currency'], 'credit': 0.0, 'debit': 0.0, 'remark': entry['remark'], 'group': entry['group'], 'posting_date': entry['posting_date'], 'tag_id': entry['tag_id'],'profit_or_cost_center_number':entry['profit_or_cost_center_number']}
            cumulative_sums[key]['credit'] += entry.get('credit', 0)
            cumulative_sums[key]['debit'] += entry.get('debit', 0)
            # Balance the credit and debit
            for key, values in cumulative_sums.items():
                credit = values['credit']
                debit = values['debit']
                if credit > debit:
                    values['credit'] = credit - debit
                    values['debit'] = 0.0
                else:
                    values['credit'] = 0.0
                    values['debit'] = debit - credit


        # Convert the dictionary values to a list
        result = list(cumulative_sums.values())
        for entry in result:
            print('----------entry inresult-----------------')
            print(entry)
        # writer = UnicodeWriter()
        for row in result:
            if(row['debit'] != 0):
                counter = 1
            else:
                counter = 2
            if counter == 1:
                val = getVal(row,counter)
                writer.writerow(val)
            elif counter == 2:
                val = getVal(row,counter)
                writer.writerow(val)
        print('----------writer-----------------')
        print(writer)
        print('----------done unicodeWriter-----------------')
        createCSVExport(writer.getvalue(),filename,server_path)
        print('-----------done everything------------------')
        IsExported(journal_list)
    except Exception as e:
        print('error: ',e)
       
@frappe.whitelist(allow_guest=True)
def exportDRReportToSAP():
    print('--export Deferred Revenue----')
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Deferred Revenue (Export)'})
        if scheduler.report_name == '' or scheduler.report_name is None:
            filename = getExportFilename(2)
        else:
            filename = scheduler.report_name
            filename += getFilenameDateString()
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic
        names = []

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0','docstatus':'1'})
                journal_list.append(journal)
                names.append(journal.name)
            except:
                print('No Deferred Revenue is available to be exported!')
                return
            
        elif periodic == 'Month End':
            #enable in Staging [1]
            # now = datetime.now()
            # month = now.month
            # year = now.year
            # last = calendar.monthrange(year,month)[1]
            # str_date = str(year) + '-' + str(month) + '-'
            # first_day = str_date + '01'
            # last_day = str_date + str(last)
            #end of enable [1]

            #disable in Staging [2]
            try:
                last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0','docstatus':'1'})
                month = last_journal.posting_date.month
                year = last_journal.posting_date.year
                last = calendar.monthrange(year,month)[1]
                str_date = str(year) + '-' + str(month) + '-'
                first_day = str_date + '01'
                last_day = str_date + str(last)
            except:
                print('Deferred Revenue Not Found!')
                return
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0','posting_date':['between',[first_day,last_day]],'docstatus':'1'})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    names.append(journal.name)
            else:
                print('No Collection Report is available to be exported!')
                return
            
        # print('len journals: ',len(names))
        # print(names)
        if len(journal_list) == 0:
            print('No Deferred Revenue Found!')
            return

        # print('new_date: ',new_date)
        account_list = getDeferredList(names)
        if account_list == '':
            # raise Exception('Deferred Revenue Does Not Exist Yet')
            print('Deferred Revenue Does Not Exist Yet')
            return
        # else:
        #     print('return')
        # print('list: ',account_list)

        writer = UnicodeWriter()
        counter = 1
        i = 0
        isDebit = False
        for rows in account_list:
            for row in rows:
                i +=1
                isDebit = False
                if row['debit'] != 0:
                    isDebit = True
                # if counter == 1:
                if isDebit:
                    val = getValDeferred(row,isDebit)
                    print('val1: ',val)
                    writer.writerow(val)   
                    counter+=1
                else:
                    val = getValDeferred(row,isDebit)
                    print('val2: ',val)
                    writer.writerow(val)
                    counter = 1
        
        print('----------done unicodeWriter-----------------')
        createCSVExport(writer.getvalue(),filename,server_path)
        print('-----------done everything------------------')
        IsExported(journal_list)

        # msg = 'A Deferred Revenue for '+getDateString(start_date)+' has been exported to SAP'
        # title = 'ERPNext: Deferred Revenue Export'
        # sendEmail(msg,title,'','')
    except Exception as e:
        print('error: ',e)


def exportBRReportToSAP():
    print('--export Billing Report----')
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing Report (Export)'})
        print('report_name:',scheduler.report_name,'#')
        if scheduler.report_name == '' or scheduler.report_name is None:
            filename = getExportFilename(3)
        else:
            filename = scheduler.report_name
            filename += getFilenameDateString()
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic
        names = []

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_exported':'0','docstatus':'1'})
                journal_list.append(journal)
                names.append(journal.name)
            except:
                print('No Billing Journal Entry available to be exported!')
                return
        elif periodic == 'Month End':
            #enable in Staging [1]
            # now = datetime.now()
            # month = now.month
            # year = now.year
            # last = calendar.monthrange(year,month)[1]
            # str_date = str(year) + '-' + str(month) + '-'
            # first_day = str_date + '01'
            # last_day = str_date + str(last)
            #end of enable [1]

            #disable in Staging [2]
            last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_exported':'0','docstatus':'1'})
            month = last_journal.posting_date.month
            year = last_journal.posting_date.year
            last = calendar.monthrange(year,month)[1]
            str_date = str(year) + '-' + str(month) + '-'
            first_day = str_date + '01'
            last_day = str_date + str(last)
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Billing','is_exported':'0','posting_date':['between',[first_day,last_day]],'docstatus':'1'})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    names.append(journal.name)
            else:
                print('No Billing Report is available to be exported!')
                return
        row_lists = []
        for j in journal_list:
            tag_id = j.tag_id
            accounts = j.accounts
            row_list = []
            getRow(accounts,row_list,tag_id,0)
            row_lists.append(row_list)  
        # print('len journals: ',len(names))
        # print(names)
        if len(journal_list) <= 0:
            print('No Billing Found!')
            return

        # print('new_date: ',new_date)
        account_list = getDeferredList(names)
        if account_list == '':
            # raise Exception('Deferred Revenue Does Not Exist Yet')
            print('Billing Report Does Not Exist Yet')
            return
        # else:
        #     print('return')
        # print('list: ',account_list)
        writer = UnicodeWriter()
        # Removing entries with 'is_jb': 1
        row_lists = [
            [entry for entry in sublist if entry.get('is_jb', 0) != 1]
            for sublist in row_lists
        ]
        combined_array = []
        for rows in row_lists:
            for item in rows:
                combined_array.append(item)
        # Sum up credit and debit
        cumulative_sums = {}
        for entry in combined_array:
            key = (entry['account_number'], entry['cost_center_number'], entry['remark'], entry['group'],entry['profit_or_cost_center_number'])
            if key not in cumulative_sums:
                cumulative_sums[key] = {'year': entry['year'], 'account_number': entry['account_number'], 'cost_center_number': entry['cost_center_number'], 'currency': entry['currency'], 'credit': 0.0, 'debit': 0.0, 'remark': entry['remark'], 'group': entry['group'], 'posting_date': entry['posting_date'],'tax_amount': entry['tax_amount'],'tax_code': entry['tax_code'],'profit_or_cost_center_number': entry['profit_or_cost_center_number'],'san_count': entry['san_count'],'monthly_charge': entry['monthly_charge'],'month_count': entry['month_count'],'current_month': entry['current_month'], 'tag_id': entry['tag_id']}
            cumulative_sums[key]['credit'] += entry.get('credit', 0)
            cumulative_sums[key]['debit'] += entry.get('debit', 0)
            # Balance the credit and debit
            for key, values in cumulative_sums.items():
                credit = values['credit']
                debit = values['debit']
                if credit > debit:
                    values['credit'] = credit - debit
                    values['debit'] = 0.0
                else:
                    values['credit'] = 0.0
                    values['debit'] = debit - credit
        # Convert the dictionary values to a list
        result = list(cumulative_sums.values())
        for entry in result:
            print('----------entry inresult-----------------')
            print(entry)

        for row in result:
            if(row['debit'] != 0):
                counter = 1
            else:
                counter = 2
            if counter == 1:
                val = getValDeferred(row,1)
                writer.writerow(val)
            elif counter == 2:
                val = getValDeferred(row,0)
                writer.writerow(val)
        print('----------writer-----------------')
        print(writer)

        print('----------done unicodeWriter-----------------')
        createCSVExport(writer.getvalue(),filename,server_path)
        print('-----------done everything------------------')
        IsExported(journal_list)

        # msg = 'A Deferred Revenue for '+getDateString(start_date)+' has been exported to SAP'
        # title = 'ERPNext: Deferred Revenue Export'
        # sendEmail(msg,title,'','')
    except Exception as e:
        print('error: ',e)


def exportJBCRReportToSAP():
    print('------------------Export CR JB Report To SAP')
    # if scheduler == 'Collection Report (Export)':
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Collection JB Report (Export)'})
        if scheduler.report_name == '' or scheduler.report_name is None:
            print('generate file name: ')
            filename = getExportFilename(1)
        else:
            filename = scheduler.report_name
            filename += getFilenameDateString()
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_jb_exported':'0','docstatus':'1'})
                journal_list.append(journal)
            except:
                print('No Collection Report JB is available to be exported!')
                return
        elif periodic == 'Month End':
            #enable in Staging [1]
            # now = datetime.now()
            # month = now.month
            # months = str(month)
            # if len(str(month)) < 2:
                # months = '0'+str(month)
            # month_filter = '%-'+months+'-%'
            #end of enable [1]

            #disable in Staging [2]
            last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_jb_exported':'0','docstatus':'1'})
            month = last_journal.posting_date.month
            year = last_journal.posting_date.year
            last = calendar.monthrange(year,month)[1]
            str_date = str(year) + '-' + str(month) + '-'
            first_day = str_date + '01'
            last_day = str_date + str(last)
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Collection','is_jb_exported':'0','posting_date':['between',[first_day,last_day]],'docstatus':'1'})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    print('----------journal_list-----------------')
                    print(journal_list)
            else:
                print('No Collection Report JB is available to be exported!')
                return
        row_lists = []
        for j in journal_list:
            tag_id = j.tag_id
            accounts = j.accounts
            row_list = []
            getRow(accounts,row_list,tag_id,1)
            row_lists.append(row_list)
        
        if len(journal_list) <= 0:
            print('No Journal Entry Found!')
            return
        # Removing entries with 'is_jb': 0
        row_lists = [
            [entry for entry in sublist if entry.get('is_jb', 1) != 0]
            for sublist in row_lists
        ]
        writer = UnicodeWriter()
        combined_array = []
        for rows in row_lists:
            for item in rows:
                combined_array.append(item)
        # Sum up credit and debit
        cumulative_sums = {}
        for entry in combined_array:
            key = (entry['account_number'], entry['cost_center_number'], entry['remark'], entry['group'],entry['profit_or_cost_center_number'])
            if key not in cumulative_sums:
                cumulative_sums[key] = {'year': entry['year'], 'account_number': entry['account_number'], 'cost_center_number': entry['cost_center_number'], 'currency': entry['currency'], 'credit': 0.0, 'debit': 0.0, 'remark': entry['remark'], 'group': entry['group'], 'posting_date': entry['posting_date'], 'tag_id': entry['tag_id'],'profit_or_cost_center_number':entry['profit_or_cost_center_number']}
            cumulative_sums[key]['credit'] += entry.get('credit', 0)
            cumulative_sums[key]['debit'] += entry.get('debit', 0)
            # Balance the credit and debit
            for key, values in cumulative_sums.items():
                credit = values['credit']
                debit = values['debit']
                if credit > debit:
                    values['credit'] = credit - debit
                    values['debit'] = 0.0
                else:
                    values['credit'] = 0.0
                    values['debit'] = debit - credit


        # Convert the dictionary values to a list
        result = list(cumulative_sums.values())
        for entry in result:
            print('----------entry inresult-----------------')
            print(entry)
        # writer = UnicodeWriter()
        for row in result:
            if(row['debit'] != 0):
                counter = 1
            else:
                counter = 2
            if counter == 1:
                val = getVal(row,counter)
                writer.writerow(val)
            elif counter == 2:
                val = getVal(row,counter)
                writer.writerow(val)
        print('----------writer-----------------')
        print(writer)
        print('----------done unicodeWriter-----------------')
        createCSVExport(writer.getvalue(),filename,server_path)
        print('-----------done everything------------------')
        IsJBExported(journal_list)
    except Exception as e:
        print('error: ',e)

def exportJBBRReportToSAP():
    print('--export Billing JB Report----')
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Billing JB Report (Export)'})
        print('report_name:',scheduler.report_name,'#')
        if scheduler.report_name == '' or scheduler.report_name is None:
            filename = getExportFilename(3)
        else:
            filename = scheduler.report_name
            filename += getFilenameDateString()
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic
        names = []

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_jb_exported':'0','docstatus':'1'})
                journal_list.append(journal)
                names.append(journal.name)
            except:
                print('No Billing Journal JB Entry available to be exported!')
                return
        elif periodic == 'Month End':
            #enable in Staging [1]
            # now = datetime.now()
            # month = now.month
            # year = now.year
            # last = calendar.monthrange(year,month)[1]
            # str_date = str(year) + '-' + str(month) + '-'
            # first_day = str_date + '01'
            # last_day = str_date + str(last)
            #end of enable [1]

            #disable in Staging [2]
            last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_jb_exported':'0','docstatus':'1'})
            month = last_journal.posting_date.month
            year = last_journal.posting_date.year
            last = calendar.monthrange(year,month)[1]
            str_date = str(year) + '-' + str(month) + '-'
            first_day = str_date + '01'
            last_day = str_date + str(last)
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Billing','is_jb_exported':'0','posting_date':['between',[first_day,last_day]],'docstatus':'1'})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    names.append(journal.name)
            else:
                print('No Billing Report is available to be exported!')
                return
        row_lists = []
        for j in journal_list:
            tag_id = j.tag_id
            accounts = j.accounts
            row_list = []
            getRow(accounts,row_list,tag_id,0)
            row_lists.append(row_list)  
        # print('len journals: ',len(names))
        # print(names)
        if len(journal_list) <= 0:
            print('No Billing Found!')
            return

        # print('new_date: ',new_date)
        account_list = getDeferredList(names)
        if account_list == '':
            # raise Exception('Deferred Revenue Does Not Exist Yet')
            print('Billing Report Does Not Exist Yet')
            return
        # else:
        #     print('return')
        # print('list: ',account_list)
        writer = UnicodeWriter()
        # Removing entries with 'is_jb': 0
        row_lists = [
            [entry for entry in sublist if entry.get('is_jb', 1) != 0]
            for sublist in row_lists
        ]
        combined_array = []
        for rows in row_lists:
            for item in rows:
                combined_array.append(item)
        # Sum up credit and debit
        cumulative_sums = {}
        for entry in combined_array:
            key = (entry['account_number'], entry['cost_center_number'], entry['remark'], entry['group'],entry['profit_or_cost_center_number'])
            if key not in cumulative_sums:
                cumulative_sums[key] = {'year': entry['year'], 'account_number': entry['account_number'], 'cost_center_number': entry['cost_center_number'], 'currency': entry['currency'], 'credit': 0.0, 'debit': 0.0, 'remark': entry['remark'], 'group': entry['group'], 'posting_date': entry['posting_date'],'tax_amount': entry['tax_amount'],'tax_code': entry['tax_code'],'profit_or_cost_center_number': entry['profit_or_cost_center_number'],'san_count': entry['san_count'],'monthly_charge': entry['monthly_charge'],'month_count': entry['month_count'],'current_month': entry['current_month'], 'tag_id': entry['tag_id']}
            cumulative_sums[key]['credit'] += entry.get('credit', 0)
            cumulative_sums[key]['debit'] += entry.get('debit', 0)
            # Balance the credit and debit
            for key, values in cumulative_sums.items():
                credit = values['credit']
                debit = values['debit']
                if credit > debit:
                    values['credit'] = credit - debit
                    values['debit'] = 0.0
                else:
                    values['credit'] = 0.0
                    values['debit'] = debit - credit
        # Convert the dictionary values to a list
        result = list(cumulative_sums.values())
        for entry in result:
            print('----------entry inresult-----------------')
            print(entry)

        for row in result:
            if(row['debit'] != 0):
                counter = 1
            else:
                counter = 2
            if counter == 1:
                val = getValDeferred(row,1)
                writer.writerow(val)
            elif counter == 2:
                val = getValDeferred(row,0)
                writer.writerow(val)
        print('----------writer-----------------')
        print(writer)

        print('----------done unicodeWriter-----------------')
        createCSVExport(writer.getvalue(),filename,server_path)
        print('-----------done everything------------------')
        IsJBExported(journal_list)

        # msg = 'A Deferred Revenue for '+getDateString(start_date)+' has been exported to SAP'
        # title = 'ERPNext: Deferred Revenue Export'
        # sendEmail(msg,title,'','')
    except Exception as e:
        print('error: ',e)
     