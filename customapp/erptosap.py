import frappe
from datetime import datetime, date, time, timedelta
import json, requests, csv, os, calendar
from frappe.utils.csvutils import UnicodeWriter
from frappe.utils import cstr
from ftplib import FTP
import io

def getRow(accounts,row_list,tag_id):
    tag = True
    counter = 1
    for a in accounts:
        # print('account: ',a.name)
        if counter == 1:
            counter+=1

            row = {
                'year':a.year,
                'account_number':a.account_number,
                'cost_center_number':a.cost_center_number,
                'currency':a.currency,
                'debit':a.debit_in_account_currency,
                'remark':a.remark,
                'group':a.group,
                'posting_date':a.posting_date,
            }
            if tag:
                row['tag_id'] = tag_id

            # print('row 1: ',row)
            row_list.append(row)
        
        elif counter == 2:
            counter = 1
            row = {
                'year':a.year,
                'account_number':a.account_number,
                'cost_center_number':a.cost_center_number,
                'currency':a.currency,
                'credit':a.credit_in_account_currency,
                'remark':a.remark,
                'group':a.group,
                'posting_date':a.posting_date
            }
            if tag:
                row['tag_id'] = tag_id
            # print('row 2: ',row)
            row_list.append(row)

def getDate(dates):
    dates = datetime.strptime(dates, '%Y-%m-%d')
    dates = dates.date()
    return dates

def getDateString(dates):
    dates = dates.strftime('%Y-%m-%d')
    return dates

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
        val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',getAmount(row['debit']),'','',getAmount(row['debit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'])
        # print('val 1: ',val)
    else:
        val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+getAmount(row['credit']),'','','-'+getAmount(row['credit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'])
    
    tag = True
    if tag:
        if counter == 1:
            val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',getAmount(row['debit']),'','',getAmount(row['debit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])
            # print('val 1: ',val)
        else:
            val = (str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+getAmount(row['credit']),'','','-'+getAmount(row['credit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],row['tag_id'])
    
    return val

def getValDeferred(row,isDebit):
    try:
        if isDebit:
            val = ('',str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','',getAmount(row['debit']),'','',getAmount(row['debit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],str(row['tax_amount']),row['tax_code'],row['profit_or_cost_center_number'])
            # print('val 1: ',val)
        else:
            val = ('',str(row['year']),str(row['account_number']),str(row['cost_center_number']),'','','','','','','','',str(row['currency']),'','','-'+getAmount(row['credit']),'','','-'+getAmount(row['credit']),'','','','',row['remark'],'','','','','','',row['posting_date'],row['group'],str(row['tax_amount']),row['tax_code'],row['profit_or_cost_center_number'])
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
            getRow(accounts,row_list,tag_id)

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
            getRow(accounts,row_list,tag_id)

            # rest of the date
            for i in range(days):
                start_date += timedelta(days=1)
                journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
                tag_id = journal.tag_id
                accounts = journal.accounts
                # print('accounts: ',accounts)
                getRow(accounts,row_list,tag_id)
            
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
            getRow(accounts,row_list,tag_id)

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
            getRow(accounts,row_list,tag_id)

            # rest of the date
            for i in range(days):
                start_date += timedelta(days=1)
                journal = frappe.get_last_doc('Journal Entry',filters={'tag_id':start_date})
                accounts = journal.accounts
                tag_id = journal.tag_id
                # print('accounts: ',accounts)
                getRow(accounts,row_list,tag_id)
            
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
    csv_string = value
    uploadToFtpServer(csv_string,filename,path)

def getExportFilename(report):
    filename = ''
    if report == 1:
        filename += 'BRAINSCOLL'
    elif report == 2:
        filename += 'BRAINSDEF'
    elif report == 3:
        filename += 'BRAINSBILL'

    # now = datetime.now()
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

    filename += year+month+day+hour+minute
    print('hour: ',hour)
    print('minute: ',minute)
    print('now: ',now)


    return filename


def exportCRReportToSAP():
    print('------------------Export CR Report To SAP')
    # if scheduler == 'Collection Report (Export)':
    try:
        scheduler = frappe.get_last_doc('Scheduler Manager',filters={'scheduler':'Collection Report (Export)'})
        if scheduler.report_name == '' or scheduler.report_name is None:
            filename = getExportFilename(1)
        else:
            filename = scheduler.report_name
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_exported':'0'})
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
            last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Collection','is_exported':'0'})
            month = last_journal.posting_date.month
            year = last_journal.posting_date.year
            last = calendar.monthrange(year,month)[1]
            str_date = str(year) + '-' + str(month) + '-'
            first_day = str_date + '01'
            last_day = str_date + str(last)
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Collection','is_exported':'0','posting_date':['between',[first_day,last_day]]})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
            else:
                print('No Collection Report is available to be exported!')
                return
        row_lists = []
        for j in journal_list:
            tag_id = j.tag_id
            accounts = j.accounts
            row_list = []
            getRow(accounts,row_list,tag_id)
            row_lists.append(row_list)
        
        if len(journal_list) <= 0:
            print('No Journal Entry Found!')
            return
        
        writer = UnicodeWriter()
        for rows in row_lists:
            # writer = UnicodeWriter()
            counter = 1
            for row in rows:
                if counter == 1:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter+=1
                elif counter == 2:
                    val = getVal(row,counter)
                    writer.writerow(val)
                    counter = 1
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
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic
        names = []

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0'})
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
                last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0'})
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

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Deferred Revenue','is_exported':'0','posting_date':['between',[first_day,last_day]]})
            
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
        server_path = scheduler.path
        journal_list = []
        periodic = scheduler.periodic
        names = []

        if periodic == 'Daily':
            try:
                journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_exported':'0'})
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
            try:
                last_journal = frappe.get_last_doc('Journal Entry', filters={'report_type':'Billing','is_exported':'0'})
                month = last_journal.posting_date.month
                year = last_journal.posting_date.year
                last = calendar.monthrange(year,month)[1]
                str_date = str(year) + '-' + str(month) + '-'
                first_day = str_date + '01'
                last_day = str_date + str(last)
            except:
                print('Billing Report Not Found!')
                return
            #end of disable [2]

            journals = frappe.get_all('Journal Entry', filters={'report_type':'Billing','is_exported':'0','posting_date':['between',[first_day,last_day]]})
            
            if journals:
                for j in journals:
                    journal = frappe.get_last_doc('Journal Entry',filters={'name':j.name})
                    journal_list.append(journal)
                    names.append(journal.name)
            else:
                print('No Billing Report is available to be exported!')
                return
            
        # print('len journals: ',len(names))
        # print(names)
        if len(journal_list) == 0:
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
                    # print('val1: ',val)
                    writer.writerow(val)
                    counter+=1
                else:
                    val = getValDeferred(row,isDebit)
                    # print('val2: ',val)
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
