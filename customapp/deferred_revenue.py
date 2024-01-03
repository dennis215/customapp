import frappe
from datetime import datetime, time, date
import os, csv, requests, calendar, json, random, string, socket, re, time
from customapp.general_function import *

def printing(data):
    i = 0
    for row in data:
        i += 1
        print('i, length: ',len(row))
        print('i, data: ',row.keys())

def checkExist(dates):
    try:
        doc = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'tag_id':dates})
        return True
    except:
        return False

def deferredRevenue():
    print('----------------------------deferred revenue')
    # now = datetime.now()
    # ts = int(now.timestamp())
    # sch = frappe.get_last_doc('Scheduled Job Type',filters={'method':'customapp.deferred_revenue.deferredRevenue'})
    # sch.time2 = ts
    # sch.save()
    # doc = frappe.new_doc('testdoctype2')
    # doc.save()
    # frappe.db.commit()
    # return
    global domain, site
    # domain = 'http://127.0.0.1:8000'
    # domain = 'http://175.136.236.153:8003'
    domain = getDomain()
    sites = frappe.utils.get_site_path()
    split = sites.split('/')
    site = split[1]
    # print('--Site: ',site,' domain: ',domain)
    scheduler = frappe.get_last_doc('Scheduler Manager',filters={'name':'Deferred Revenue (Import)'})
    control = scheduler.control
    # if control == 'Stop':
    #     print('--------------------Deferred Revenue Scheduler is STOPPED')
    # elif control == 'Play':
    if True:
    #     print('--------------------Deferred Revenue Scheduler is PLAYING')
    #     while True:
    #         sch = frappe.get_last_doc('Scheduled Job Type',filters={'method':'customapp.deferred_revenue.deferredRevenue'})
    #         now = datetime.now()
    #         ts = int(now.timestamp())
    #         diff = ts - sch.time1
    #         if diff >= 60:
    #             print('diff: ',diff,' break')
    #             sch.time1 = ts
    #             sch.save()
    #             frappe.db.commit()
    #             break
    #         else:
    #             time.sleep(1)
    #             print('diff: ',diff)

        # bill_je = frappe.get_list('Journal Entry',filters={'report_type':'Billing'})
        # if bill_je:
        #     if len(bill_je) > 1:
        #         exist,date_take,date_put = checkDo()
        #         print('date_take: ',date_take)
        #         print('date_put: ',date_put)
        #         if not exist:
        #             print('not exist')
        #             return
        #     else:
        #         print('There is only one Billing Journal Entry Found!')
        #         return
        # else:
        #     print('No Billing Journal Entry Found!')
        #     return
        docCheck = getLastMonthName(3)
        doc = frappe.get_last_doc('Deferred Revenue Journal Entry')
        print('docCheck docCheck docCheck: ',docCheck)
        if(doc.name==docCheck):
            raise Exception('Deferred entry created for '+docCheck)
        print(docCheck+'not created yet')

        # 1) create new dje                                                     done!
        deferred = frappe.new_doc('Deferred Revenue Journal Entry')
        # deferred.tag_id = date_take
        # for real
        # doc_name = getCurrentMonthName()
        # deferred.doc_name = doc_name
        deferred.created = datetime.now().date()
        # for testing
        # deferred.doc_name = ''.join(random.choices(string.digits, k=4))
        print('1) Done create new dje')

        dje_list = []
        update_list = []
        new_list = []
        print('dje list length: ',len(dje_list))
        # 2) take jea from last month dje                                       done!
        # 3) select 2 that month count is not 0
        dr_exist, last_djea, last_posting_date = getJEALastDR(docCheck)
        # dr_exist= got previous deferred, last_djea = deferred JE, posting= this month last day
        print('--------------lastdjea :')
        print('last djea: ',last_djea)
        
        for l in last_djea:
            print('--------------')
            print(l)

        print('last djea length: ',len(last_djea))
        print('2) done select 2 that month count is not 0')
        
        # print('lengtht: ',len(last_deferred_list))
        # for l in last_deferred_list:
        #     # print(l)
        #     print(l['account_number'])

        # 4) put 3 into dje list
        if not dr_exist:
            # last_posting_date = date(year=2023,month=1,day=31)
            # next_date = getNextDate(last_posting_date)
            next_date = getNextDate(last_posting_date)
            # deferred.tag_id = next_date
            default = True
        else:
            # last_dr = frappe.get_last_doc('Deferred Revenue')
            # last_posting_date = last_dr.posting_date
            next_date = getNextDate(last_posting_date)
            # deferred.posting_date = next_date
            # deferred.tag_id = next_date
            deferred.doc_name = next_date
            default = False

            for row in last_djea:
                dje_list.append(row)
        
        # if checkExist(next_date):
        #     print('Deferred Revenue Journal Entry for ',str(next_date),' already exist!')
        #     return
            
        # # print('dje list length: ',len(dje_list))
        # # print('----dje lists',dje_list)
        #     print('3) done put 3 into dje list')

        # 5) take jea from last month je which have deferred revenue            done!
        # if dr_exist:
        je_exist,row_JE_list, tag_id = getRowLastJE(next_date)
    # print('last je length: ',len(row_JE_list))
        print('4) done take jea from last month je')
        for l in row_JE_list:
            print('-----')
            print(l)


        # 6) put 6 into dje list
        if not je_exist and default:
            print('No Journal Entry!')
            return
        elif je_exist:
            for row in row_JE_list:
                dje_list.append(row)
        # dje_list.append(row_JE_list)
            print('dje list length: ',len(dje_list))
            # print(dje_list)
            print('5) done put 6 into dje list')
        # for l in dje_list:
        #     print('---------------')
        #     print(l['debit_in_account_currency'],' ',l['credit_in_account_currency'])

        # 7) -month_count and calculate value each jea from dje list
        # 8) create 2 new rows from 7
        # print('--dje_list: ',dje_list)
        # print('999999999999999999999999 ',dje_list)
        
        # elif je_exist:
        # new_list, update_list = doLogicDeferred(dje_list)
        update_list = doLogicDeferred(dje_list)
        print('6) done create 2 new rows')
        # print('update')
        # for p in update_list:
        #     print('--------------- ',p['month_count'])
            # print('6) done create 2 new rows')
        # for l in update_list:
        #     print(l['debit_in_account_currency'],' ',l['credit_in_account_currency'],' ',l['month_count'])

        # 10) put updated dje from 7 to 1
        # doAddtoNewDJE(deferred,dje_list)
        # print('-----update list-----')
        # print(update_list)
        doAddtoNewDJE(deferred,update_list)
        
        # print('update')
        # for p in update_list:
        #     print('--------------- ',p)
        print('7) done put updated dje')

        # 11) put created new jea to last je
        # if dr_exist or je_exist:
        #     # print('------...----',doc.name)
        #     doCreateJEAonLastMonthJE(date_put,new_list)
        #     print('8) done put new created to last month je')
        createDeferredAccountingEntries(deferred,tag_id)

def getNextDate(dates):
    if isinstance(dates, str):
        dates = datetime.strptime(dates, '%Y-%m-%d')
    month = dates.month
    year = dates.year
    month += 1
    if month == 13:
        month = 1
        year += 1
    days = calendar.monthrange(year, month)
    next_date = date(day=days[1],month=month,year=year)
    return next_date

def checkDo():
    # je_list = frappe.get_list('Journal Entry',filters={'report_type':'Billing'})
    # if je_list:
    #     je = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing'})
    #     posting_date = je.posting_date

    # check is any deferred
    dr_list = frappe.get_list('Deferred Revenue Journal Entry')
    if dr_list:
        deferred = frappe.get_last_doc('Deferred Revenue Journal Entry')
        tag_id = deferred.tag_id
        # month = tag_id.month
        # month += 1
        # days = calendar.monthrange(tag_id.year, month)
        # date_take = date(day=days[1],month=month,year=tag_id.year)
        date_take = getNextDate(tag_id)
        date_put = getNextDate(date_take)

        je_take_list = frappe.get_list('Journal Entry',filters={'report_type':'Billing','tag_id':date_take})
        je_put_list = frappe.get_list('Journal Entry',filters={'report_type':'Billing','tag_id':date_put})
        if je_take_list and je_put_list:
            # je = je_list[0]
            # return True, posting_date
            # print('tagid: ',tag_id,' postingdate: ',posting_date,' sasa')
            return True, date_take,date_put
        else:
            print('Next Billing Journal Entry Has Not Been Created Yet!')
            print('take: ',date_take,' put: ',date_put)
            take = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':date_take})
            put = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':date_put})
            return False,'',''
    else:
        # create 
        date_take = date(day=31,month=1,year=2023)
        date_put = getNextDate(date_take)
        # month = date_take.month
        # month += 1
        # days = calendar.monthrange(date_take.year, month)
        # date_put = date(day=days[1],month=month,year=date_take.year)

        je_list = frappe.get_list('Journal Entry',filters={'report_type':'Billing','tag_id':date_put})
        if je_list:
            je = je_list[0]
            # posting_date = posting_date.replace(month=posting_date.month-1)
            # print('ppopopting date: ',posting_date)
            return True, date_take,date_put
        else:
            print('Next Billing Journal Entry Has Not Been Created Yet!')
            return False,'',''

    # else:
    #     dates = calendar.monthrange(2023,1)
    #     dates = date(day=dates[1],month=1,year=2023)
    #     try:
    #         je = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':dates})
    #     except:
    #         return

# def getMonthDate(posting_date):
#     if isinstance(posting_date, str):
#         posting_date = datetime.strptime(posting_date,'%Y-%m-%d')
#     month = posting_date.month
#     month_name = posting_date

def getPastPostingDate(dates):
    pass

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

def getLastMonthName(f1):
    now = datetime.now()
    year = now.year
    if now.month == 1:
        month = 12
        year =year-1
    else:
        month = now.month - 1   # last month
    date1 = date(day=1, month=month, year=year)
    last_month = ''
    if f1 == 1:
        last_month = date1.strftime('%B')+' - '+'Billing'
    elif f1 == 2:
        last_month = date1.strftime('%B')+' '+now.strftime('%Y')
        return last_month
    elif f1==3:
        last_month = str(year)+" - "+date1.strftime('%B')
        return last_month
    # print('name: ',last_month)
    title = ["like", f"%{last_month}%"]
    return title

def getCurrentMonthName():
    now = datetime.now()
    name = now.strftime('%B') + ' ' + now.strftime('%Y')
    
    return name

def get_first_day(posting_date):
    # Assuming posting_date is a string in the format 'YYYY-MM-DD'
    posting_date = datetime.strptime(str(posting_date), '%Y-%m-%d')
    
    # Get the first day of the month
    first_day = posting_date.replace(day=1)
    
    # Format the result as a string if needed
    first_day_str = first_day.strftime('%Y-%m-%d')
    
    return first_day_str
def getRowLastJE(posting_date):
    # print('last_month: ',last_month)
    # title = getLastMonthName(1)

    # doc = frappe.get_last_doc('Deferred Revenue Journal Entry', filters={'name':filter})
    # print('title: ',title)
    # doc = frappe.get_last_doc('Journal Entry', filters={'title':title,'report_type':'Billing'})
    je_exist = False
    firstDay = get_first_day(posting_date)   
    doclist = frappe.get_all('Journal Entry',
    filters={'report_type': 'Billing',"docstatus":1, 'posting_date': ['between', [firstDay, posting_date]]},fields=['*'])
    # doclist = frappe.get_list('Journal Entry', filters={'report_type':'Billing',"docstatus":1,'posting_date':['>=', firstDay, '<=', posting_date]})
    if doclist:
        je_exist = True
    else: 
        return je_exist,'',''
    
    account_entries_list =[]
    for doc in doclist:
        journal_entry = frappe.get_doc('Journal Entry', doc.name)
        account_entries_list.append(journal_entry.accounts)
    flat_account_entries_list = [entry for sublist in account_entries_list for entry in sublist]
    # print('doc name: ',doc.name)
    # print('row list:')
    # print(row_list)
    # print('length row: ',len(row_list))

    data_entries_list = []
    for row in flat_account_entries_list:
    # row = account_entries_list[0]
        if row.month_count <=1:
            pass
        else:
            data = {
                'account':row.account,
                'account_number':row.account_number,
                'cost_center':row.cost_center,
                'cost_center_number':row.cost_center_number,
                'currency':row.currency,
                'debit_in_account_currency' : float(row.debit_in_account_currency),
                'credit_in_account_currency' : float(row.credit_in_account_currency),
                'remark':row.remark,
                'group':row.group,
                'year': row.year,
                'posting_date':row.posting_date,
                'tax_amount':row.tax_amount,
                'tax_code':row.tax_code,
                'profit_or_cost_center_number':row.profit_or_cost_center_number,
                'san_count':row.san_count,
                'monthly_charge':row.monthly_charge,
                'month_count':row.month_count,
                'current_month':row.current_month,
                'revenue_account':row.revenue_account,
                'new_cost_center':row.new_cost_center,
                'journal_entry':doc.name
            }
            data_entries_list.append(data)
    # print('data')
    # print(data)
    # for row in data_entries_list:
    #     print(row['month_count'])
    return je_exist,data_entries_list, doc.tag_id

def doCreateJEAonLastMonthJE(date_put, new_list):
    doc = frappe.get_last_doc('Journal Entry',filters={'report_type':'Billing','tag_id':date_put})
    je = frappe.new_doc('Journal Entry')
    je.title = doc.title
    je.tag_id = doc.tag_id
    je.report_type = doc.report_type
    je.naming_series = doc.naming_series
    je.posting_date = doc.posting_date
    je.accounts = doc.accounts
    
    total_debit = 0
    total_credit = 0
    counter = 1
    for row in new_list:
        je.append('deferred_accounts',row)
        if counter == 1:
            counter += 1
            total_debit += row['debit_in_account_currency']
        elif counter == 2:
            counter = 1
            total_credit += row['credit_in_account_currency']
    # total_debit, total_credit = getDeferredTotal(total_debit)
    je.total_deferred_debit = 'RM '+str(total_debit)
    je.total_deferred_credit = 'RM '+str(total_credit)

    doc.cancel()
    doc.delete()
    je.save()
    je.submit()

def getDeferredTotal(val):
    vals = str(val)
    if '.' in vals:
        split = vals.split('.')
        vals = split[0]
        if len(vals) > 4:
            val1 = vals[:3]

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

def doLogicDeferred(dje_list):
    new_list = [] # accounting entries that needed to be added to JE last month
    update_list = []
    revenue_counter = 0
    isBegin = True
    seq = 0
    row_1 = {}
    row_2 = {}
    counter = 0

    for row in dje_list:
        if isBegin:
            counter = 2
            if row['debit_in_account_currency'] != 0:
                counter = 1
            seq = 1
            isBegin = False
        if revenue_counter == 0:
            if seq == 2:
                revenue_counter += 1
                isBegin = True

            if counter == 1:
                deferred_revenue, row = doCalculate(row,1)
                row['debit_in_account_currency'] = deferred_revenue
                update_list.append(row)
                row1 = row.copy()
                deferred_revenue2, row_1 = doCalculate(row1,2)
                row_1['debit_in_account_currency'] = deferred_revenue2
                row_1['credit_in_account_currency'] = 0

                if seq == 1:
                    counter = 2
                    seq += 1
            elif counter == 2:
                deferred_revenue, row = doCalculate(row,1)
                row['credit_in_account_currency'] = deferred_revenue
                update_list.append(row)
                row2 = row.copy()
                deferred_revenue2, row_2 = doCalculate(row2,2)
                row_2['credit_in_account_currency'] = deferred_revenue2
                row_2['debit_in_account_currency'] = 0

                if seq == 1:
                    counter = 1
                    seq += 1
            
            
        if revenue_counter == 1:
            revenue_counter = 0
            row_1['account_number'] = row_2['account_number']
            row_1['account'] = row_2['account']
            row_1['cost_center_number'] = row_2['cost_center_number']
            row_1['cost_center'] = row_2['cost_center']
            row_2['revenue_account'] = None
            row_2['account_number'] = row_1['revenue_account']
            acc = frappe.get_last_doc('Account',filters={'account_number':row_2['account_number']})
            row_2['account'] = acc.name
            row_1['month_count'] = 1
            row_2['month_count'] = 1

            new_list.append(row_1)
            new_list.append(row_2)
    
    # print('update')
    return update_list

def doLogicDeferred2(dje_list):
    # for d in dje_list:
    #     print(d)
    #     print('\n\n')
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
        if row['month_count'] >1:
            i += 1
            if isBegin:
                counter = 2
                isDebitFirst = False
                if row['credit_in_account_currency'] == 0.0:
                    counter = 1
                    isDebitFirst = True
                    # print('debit: ',row['debit_in_account_currency'],' credit: ',row['credit_in_account_currency'])
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
                    # print('isdebitfirst true')
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
    return new_list


def doAddtoNewDJE(deferred,dje_list):
    # print('updated list')
    # try:
    # print('dje list: ',dje_list)
    now = datetime.now().date()
    posting_date = dje_list[0]['posting_date']
    for row in dje_list:
        deferred.append('accounts',row)

    # title = getDRTitle(now)
    title = getDRTitle(posting_date)
    deferred.doc_name = title
    deferred.save()
    deferred.submit()

    domains = domain + '/app/deferred-revenue-journal-entry/'+ deferred.name
    # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
    deferred_link = "<a href='"+domains+"' target='_blank'>Deferred Revenue Journal Entry </a>"
    # frappe.msgprint('One Journal Entry has been created, See Here ')
    # msg = 'A Deferred Revenue Journal Entry has been made today. '+'Please see here '+deferred_link
    # subject = 'ERPNext: Deferred Revenue Journal Entry'
    # sendEmail(msg,subject,deferred.doctype,deferred.name)
    # except Exception as e:
    #     print('exception: ',e)

def getJEALastDR(yearMonth):
    # for real
    # title = getLastMonthName(2)
    # deferred = frappe.get_last_doc('Deferred Revenue Journal Entry',filters={'name':title})
    # for testing
    # title = getLastMonthName(2)
    dr_exist = False
    try:
        deferred = frappe.get_last_doc('Deferred Revenue Journal Entry')
        dr_exist = True
    except:
        return dr_exist,'',''
    
    # name = deferred.doc_name
    # split = name.split(' ')
    # month = split[0]
    # if month == 'February' or month == 'March':
    # last_posting_date = deferred.tag_id
    # last_posting_date = deferred.posting_date
    last_posting_date = getNextDate2(deferred.doc_name,yearMonth)


    row_list = deferred.accounts
    next_date = getNextDate(last_posting_date)

    rows_list = []
    for row in row_list:
        if row.revenue_account != '':
            print('=== month: ',row.month_count)
        if row.month_count != 0:
            acc_dict = {
                'account':row.account,
                'account_number':row.account_number,
                'cost_center':row.cost_center,
                'cost_center_number':row.cost_center_number,
                'currency':row.currency,
                'debit_in_account_currency' : float(row.debit_in_account_currency),
                'credit_in_account_currency' : float(row.credit_in_account_currency),
                'remark':row.remark,
                'group':row.group,
                'year': row.year,
                # 'posting_date':row.posting_date,
                'posting_date':next_date,
                'tax_amount':row.tax_amount,
                'tax_code':row.tax_code,
                'profit_or_cost_center_number':row.profit_or_cost_center_number,
                'san_count':row.san_count,
                'monthly_charge':row.monthly_charge,
                'month_count':row.month_count,
                'current_month':row.current_month,
                'revenue_account':row.revenue_account,
                'journal_entry':row.journal_entry,
                'new_cost_center':row.new_cost_center
            }
            rows_list.append(acc_dict)
    
    return dr_exist, rows_list, last_posting_date

# def createDeferredAccountingEntries(journal,new_date):
def createDeferredAccountingEntries(deferred,tag_id):
    deferredje = frappe.new_doc('Journal Entry')
    deferredje.report_type = 'Deferred Revenue'
    deferredje.entry_type = "Journal Entry"

    # deferreds = getDocList('Deferred Revenue Journal Entry','',True)
    # if not deferreds:
    #     print('No Previous Deferred Revenue Found!')
    #     return
    # else:
    #     deferred = getDoc('Deferred Revenue Journal Entry','')
    # acc = deferred.accounts

    acc = deferred.accounts
    counter = 1
    dr = []
    isBegin = True
    complete = False
    seq = 0
    posting_date = acc[0].posting_date
    for row in acc:
        # print('-----debit: ',row.debit_in_account_currency,' ---credit: ',row.credit_in_account_currency)
        # print('acccc debit: ',row.debit_in_account_currency,' credit: ',row.credit_in_account_currency)
        
        if isBegin:
            counter = 2
            if row.debit_in_account_currency != 0.0:
                counter = 1
            isBegin = False
            seq = 1
            complete = False

        if not complete:
            if seq == 2:
                complete = True
                isBegin = True
            if counter == 1:
                # print('debit')
                if seq == 1:
                    counter = 2
                    seq += 1
                rows_dict = {
                    'account':row.account,
                    'account_number':row.account_number,
                    'cost_center':row.cost_center,
                    'cost_center_number':row.cost_center_number,
                    # 'cost_center':cost_center.name,
                    'currency':row.currency,
                    'debit_in_account_currency' : float(row.debit_in_account_currency),
                    'credit_in_account_currency' : float(0),
                    'remark':row.remark,
                    'group':row.group,
                    'year': row.year,
                    'posting_date':row.posting_date,
                    'tax_amount':row.tax_amount,
                    'tax_code':row.tax_code,
                    'profit_or_cost_center_number':row.profit_or_cost_center_number,
                    'san_count':row.san_count,
                    'monthly_charge':row.monthly_charge,
                    'month_count':row.month_count,
                    'current_month':row.current_month,
                    'revenue_account':row.revenue_account,
                    'journal_entry':row.journal_entry
                }
                dr.append(rows_dict)
            elif counter == 2:
                # print('credit')
                if seq == 1:
                    counter = 1
                    seq += 1
                rows_dict = {
                    'account':row.account,
                    'account_number':row.account_number,
                    'cost_center':row.cost_center,
                    'cost_center_number':row.cost_center_number,
                    # 'cost_center':cost_center.name,
                    'currency':row.currency,
                    'debit_in_account_currency' : float(0),
                    'credit_in_account_currency' : float(row.credit_in_account_currency),
                    'remark':row.remark,
                    'group':row.group,
                    'year': row.year,
                    'posting_date':row.posting_date,
                    'tax_amount':row.tax_amount,
                    'tax_code':row.tax_code,
                    'profit_or_cost_center_number':row.profit_or_cost_center_number,
                    'san_count':row.san_count,
                    'monthly_charge':row.monthly_charge,
                    'month_count':row.month_count,
                    'current_month':row.current_month,
                    'revenue_account':row.revenue_account,
                    'journal_entry':row.journal_entry
                }
                dr.append(rows_dict)
        
    # for i in dr:
    #     print(i)
    #     print('\n\n')

    new_list = doLogicDeferred2(dr)
    print("new list length",len(new_list))
    counter = 1
    total_debit = 0
    total_credit = 0
    print('------------testest  sdsdss-----------------')
    for row in new_list:
        print(row)
        if row['debit_in_account_currency'] != 0:
            total_debit += row['debit_in_account_currency']
        else:
            total_credit += row['credit_in_account_currency']
        # try:
        #     if row['debit_in_account_currency'] != 0:
        #         total_debit += row['debit_in_account_currency']
        # except:
        #     if row['credit_in_account_currency'] != 0:
        #         total_credit += row['credit_in_account_currency']
        deferredje.append('accounts',row)
        # deferredje.append('deferred_accounts',row)
    print('total debit: ',total_debit)
    print('total_credit: ',total_credit)
    # print('dr: ')  
    # for i in dr:
    #     print(i) 
    #     print('\n\n')
    # deferredje.total_deferred_debit = getRM(total_debit)
    # deferredje.total_deferred_credit = getRM(total_credit)
    deferredje.total_debit = getRM(total_debit)
    deferredje.total_credit = getRM(total_credit)
    deferredje.posting_date = posting_date
    deferredje.tag_id = tag_id
    deferredje.title = 'Deferred Revenue - '+ getDateString(posting_date)
    deferredje.save()
    deferredje.submit()
    frappe.db.commit()
    print('Done Create DR je')
  



    








