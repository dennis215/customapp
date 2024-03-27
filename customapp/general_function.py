import frappe
from datetime import datetime, date, time, timedelta
import os, json, calendar, csv

def getDomain():
    # domain = 'http://127.0.0.1:8000'
    domain = 'http://175.136.236.153:8003'
    return domain

def getDatetimeDate(dates):
    if isinstance(dates, str):
        dates = dates[:10]
        return datetime.strptime(dates,'%Y-%m-%d').date()
    if isinstance(dates, datetime):
        return dates.date()
    return dates

def getDateString(dates):
    if isinstance(dates, datetime) or isinstance(dates, date):
        return dates.strftime('%Y-%m-%d')
    return dates

def getDatetime(dates):
    if isinstance(dates, str):
        return datetime.strptime(dates, '%Y-%m-%d')
    return dates

def getDatetimeFull(dates):
    if isinstance(dates, str):
        return datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    return dates

def getISODate(dates,timing=1):
    times = time(0,0,0)
    if timing == 2: # start_date
        times = time(23,59,59)

    if isinstance(dates, str):
        dates = datetime.strptime(dates[:10], '%Y-%m-%d').date()
        
    dates = datetime.combine(dates,times)

    return dates.isoformat() + 'Z'

def getNextDate(dates):
    if isinstance(dates, str) or isinstance(dates, datetime):
        dates = getDatetimeDate(dates)
    
    day = dates.day
    month = dates.month
    year = dates.year

    day += 1
    last_day = calendar.monthrange(year=year,month=month)[1]
    if day > last_day:
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    return date(day=day, month=month, year=year)

def getNextDate2(doc_name,yearMonth):
    if(doc_name==yearMonth):
        raise Exception('Deferred entry created for '+yearMonth)
    print('---doc_name--: ',doc_name)
    split = doc_name.split(' ')
    month_name = split[2]
    print('---month_name--: ',month_name)
    year = int(split[0])
    month_datetime = datetime.strptime(month_name, '%B')
    print('---month_datetime--: ',month_datetime)
    month_num = month_datetime.month
    print('---month_num--: ',month_num)
    days = calendar.monthrange(year=year, month=month_num)
    dates = date(day=days[1],year=year,month=month_num)
    print('---dates--: ',dates)
    return dates

def getDoc(doctype, filters={}):
    doc = frappe.get_last_doc(doctype, filters=filters)
    return doc

def checkListExist(doclist):
    if len(doclist) > 0:
        return True
    return False

def getDocList(doctype, filters={}, checkExist = False):
    doclist = frappe.get_list(doctype, filters=filters)
    if checkExist:
        exist = checkListExist(doclist)
        return exist
    return doclist

# def getListDoc(doctype, filters={}):
#     doclist = frappe.get_list(doctype, filters=filters)
#     return doclist

def getJETitle(dates,report=1):
    if isinstance(dates, datetime) or isinstance(dates, date):
        dates = dates.strftime('%Y-%m-%d')
    title = 'Collection - '+dates
    if report == 2:
        title = 'Billing - '+dates
    return title

def getMonthName(month):
    monthname = calendar.month_name[month]
    return monthname

def getMonthNumber(month_name):
    month_datetime = datetime.strptime(month_name, '%B')
    month_num = month_datetime.month
    return month_num

def getLastDay(month, year):
    days = calendar.monthrange(month=month,year=year)
    last_day = days[1]
    return last_day

# uat
def getDRTitle(dates):
    if isinstance(dates, str):
        dates = datetime.strptime(dates, '%Y-%m-%d')
    month = dates.month
    year = dates.year
    monthname = calendar.month_name[month]
    # title = monthname +' - '+str(year)
    title = str(year) +' - '+ monthname
    print("------------------------------------title---------------------")
    print(title)
    return title

def sendEmail(msg,subject,doctype,name,role):
    userlist = []
    users = frappe.get_all('User')
    for user in users:
        u = frappe.get_last_doc('User',filters={'name':user.name})
        rolelist = u.roles
        if rolelist:
            for r in rolelist:
                if r.role == role:
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

def getBatchID(filename,days):
    split = filename.split('_')
    if len(days) < 2:
        days = '0'+str(days)
    batch_id = split[0]+days
    print('noooooo')
    # return split[0]
    return batch_id

def getBatchID2(filename,days):
    split = filename.split('_')
    if len(days) < 2:
        days = '0'+str(days)
    batch_id = split[0]+days
    print('noooooo')
    # return split[0]
    return batch_id


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

def checkExist(tag_id, report):
    try:
        print('tag_id: ',tag_id)
        je = frappe.get_last_doc('Journal Entry',filters={'report_type':report,'tag_id':tag_id})
        # domain = 'http://127.0.0.1:8000' + '/app/journal-entry/'+ je.name
        # domain = 'http://175.136.236.153:8003' + '/app/journal-entry/'+ je_name
        # domains = domain + '/app/journal-entry/'+ je.name
        domains = getDomain() + '/app/journal-entry/'+ je.name
        journal_link = "<a href='"+domains+"' target='_blank'>"+report+" Journal Entry "+tag_id+"</a>"
        print('exist: true')
        return True, je.name
    except Exception as e:
        print('exception:::::::: ',str(e))
        print('exist: false')
        return False, ''


# for both billing and collection
def checkEmpty(file,f1,row,errors,error_list):
    field = f1['field']
    val = f1['value']
    error = {
        'filename':file,      
        'row':row,
        'field':field,
        'value':val
    }

    if val == '':
        errors['error'] = True
        error['description'] = 'Missing Value'
        error_list.append(error)

def getSite():
    site = frappe.utils.get_site_path()
    split = site.split('/')
    site = split[1]
    return site



# for billing

def billingConvertToDict(dje):
    new_list = []
    for row in dje:
        rows_dicts = {
            'account':row.account_number,
            'account_number':row.account_number,
            'cost_center':row.cost_center,
            'cost_center_number':row.cost_center_number,
            # 'cost_center':row.cost_center.name,
            'currency':row.currency,
            'debit_in_account_currency' : row.debit,
            'credit_in_account_currency' : row.credit,
            'remark':row.remark,
            'group':row.group,
            'year': row.year,
            'posting_date':row.posting_date,
            'tax_amount':row.tax_amount,
            'tax_code':row.tax_code,
            'second_cost_center_number':row.second_cost_center_number,
            'san_count':row.san_count,
            'monthly_charge':row.monthly_charge,
            'month_count':row.month_count,
            'current_month':row.current_month,
            'revenue_account':row.revenue_account
        }
        new_list.append(rows_dicts)
    return new_list

def makeDict(row,counter):
    # print('counter: ',counter,' val: ',row[15])
    print('-------------------makeDict----------------')
    print(row)
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
        dicts['new_cost_center'] = row[40]
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

def getDict(cr):
    dict_list = []
    counter = 1     # 1 for debit, 2 for credit
    counters = 0    # 0 for next pair, 1 for current pair
    seq = 0         # 0 for 1st partner, 1 for 2nd partner
    print('------------------getDict-----------------')
    print(cr)
    for r in cr:
        if counters == 0:
            if float(r[15]) > 0:
                counter = 1
            else:
                counter = 2
            seq = 1
            counters = 1
        if counters == 1:
            if counter == 1 and seq != 3:
                # for debit
                new_row = makeDict(r,counter)
                # print('1')
                counter = 2

            elif counter == 2 and seq != 3:
                # for credit
                new_row = makeDict(r,counter)
                # print('2')
                counter = 1
            dict_list.append(new_row)
        seq += 1
        if seq == 3:
            seq = 0
            counters = 0
    # for l in dict_list:
    #     try:
    #         print('debit-- ',l['debit'])
    #         # print(l['debit'])
    #     except:
    #         print('credit-- ',l['credit'])
    #         # print(l['credit'])
    return dict_list

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

    print('-----------------------getCrString15-------------------')
    print(cr)
    cr_dict = getDict(cr)
    print('typeee getCr: ',type(cr_dict))
    return cr_dict,cr

def getCr_pass_file(zip,file,isCollection):
    print('file: ',file)
    # print(file_url)
    cr = []
    with zip.open(file, 'r') as csv_file:
        # file.read().decode('utf-8')
        read_file = csv_file.read().decode('utf-8')
        reader = csv.reader(read_file.strip().splitlines())
        print(read_file)
        for r in reader:
            print('row: ',r)
            cr.append(r)

    print('-----------------------getCrString15-------------------',cr[1][1])
    print(cr)
    cr_dict = getDict2(cr,isCollection)
    print('typeee getCr: ',type(cr_dict))
    return cr_dict,cr


def getCrString15(template,new_date):
    str_date = getDateString(new_date)
    if not template:
        new_date = '2023-03-31'
    file_name = '15_string(15) perfect data.csv'
    cr_dict,cr = getCr(file_name)
    print('typeee getstring15: ',type(cr_dict))
    changeTemplate(cr,str_date)
    print('typeee22 getstring15: ',type(cr_dict))
    return cr_dict

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
                print('row: ',row)
                writer.writerow(row)
            print('done1')
    else:
        os.makedirs(path)
        with open(pathtofile,'w',newline='') as file:
            writer = csv.writer(file)
            for row in cr:
                print('row: ',row)
                writer.writerow(row)
            print('done2')

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

def getError(file,row_list,row,error_list,errors,balance):
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
    checkEmpty(file,objYear,row,errors,error_list)
    result = checkError(file,objYear,2,'number',row,errors,error_list,'')  # check number type
    if result:
        current_year = datetime.now().date().year
        checkError(file,objYear,4,str(current_year),row,errors,error_list,'')  # check current year
    # account
    checkEmpty(file,objAccount,row,errors,error_list)
    checkError(file,objAccount,2,'number',row,errors,error_list,'')  # check number type
    checkError(file,objAccount,1,'',row,errors,error_list,'')    # check exist
    # # cost center
    checkEmpty(file,objCost,row,errors,error_list)
    checkError(file,objCost,1,'',row,errors,error_list,'') # check exist
    # #currency
    # checkError(objCurrency,2,'string',row,errors,error_list,'') # check string type
    checkEmpty(file,objCurrency,row,errors,error_list)
    checkError(file,objCurrency,4,'MYR',row,errors,error_list,'') # check value MYR
    # # debit
    if amt_type == 'debit':
        f1 = {'field':'debit_in_account_currency','value':float(debit_credit)}
        checkError(file,f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(file,f1,row,errors,error_list)
        # balance = checkError(f1,'','',row,errors,error_list,'') # get value
        checkError(file,f1,'','',row,errors,error_list,balance) # get value
    # credit
    elif amt_type == 'credit':
        f1 = {'field':'credit_in_account_currency','value':abs(float(debit_credit))}
        checkError(file,f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(file,f1,row,errors,error_list)
        checkError(file,f1,'','',row,errors,error_list,balance)  # check balance

    # # tax amount
    # checkEmpty(file,objTaxAmount,row,errors,error_list)
    # checkError(file,objTaxAmount,2,'number',row,errors,error_list,'') # check number type
    # # tax code
    # # second_cost_center_number
    # checkEmpty(file,objProfitOrCostCenterNumber,row,errors,error_list)
    # # san_count
    # checkEmpty(file,objSanCount,row,errors,error_list)
    # checkError(file,objSanCount,2,'number',row,errors,error_list,'') # check number type
    # # monthly charge
    # checkEmpty(file,objMonthlyCharge,row,errors,error_list)
    # checkError(file,objMonthlyCharge,2,'number',row,errors,error_list,'') # check number type
    # # month count
    # checkEmpty(file,objMonthCount,row,errors,error_list)
    # checkError(file,objMonthCount,2,'number',row,errors,error_list,'') # check number type
    # # current month
    # checkError(file,objCurrentMonth,7,'',row,errors,error_list,'')      
    # checkEmpty(file,objCurrentMonth,row,errors,error_list)
    # checkError(file,objCurrentMonth,2,'number',row,errors,error_list,'') # check number type
    # # revenue account
    # checkEmpty(objRevenueAccount,row,errors,error_list)
    # checkError(objRevenueAccount,1,'',row,errors,error_list,'')    # check exist
    # # user remark
    
    checkEmpty(file,objUserRemark,row,errors,error_list)
    return balance  

def checkError(file,f1,f2,f3,row,errors,error_list,balance):
    # f1(data), f2(error type), f3(number/string, length), f4(),balance
    # checkExist('Account','account_number',row_list['account_number'],row,error_list,errors)
    field = f1['field']
    val = f1['value']
    error = {
        'filename':file,
        'row':row,
        'field':field,
        'value':val
    }

    if f2 == 1: # check record existence and ..
        doctype = f1['doctype']
        if f3 == '':
            try:
                obj = frappe.get_last_doc(doctype,filters={field:val})
            except:
                errors['error'] = True
                error['description'] = 'Invalid Data'
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
                error['description'] = doctype + ' Not Exist'
                error_list.append(error)
                # print(error_list)

    elif f2 == 2: # check format
        if f3 == 'string':  # only string
            if not val.isdigit():
                return True
            else:
                errors['error'] = True
                error['description'] = 'Invalid Format'
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
                error['description'] = 'Invalid Format'
                error_list.append(error)
                return False
                # print(error_list)
        elif f3 == 'float':
            # if not isinstance(val, float):
            try:
                float(val)
                if field == 'debit_in_account_currency' or field == 'credit_in_account_currency':
                    # print(val)
                    if val <= 0.0:
                        errors['error'] = True
                        error['description'] = 'Invalid Value'
                        error['value'] = str(error['value'])
                        error_list.append(error)
                        return False
                    return True
                return True
            except:
                errors['error'] = True
                error['description'] = 'Invalid Format'
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
                error['description'] = 'Invalid Length'
                error_list.append(error)
                # print(error_list)
            else:
                if field == 'current month':
                    month = str(val)[0:2]
                    year = str(val)[2:]
                    if int(month) > 12 or int(month) < 0:
                        errors['error'] = True
                        error['description'] = 'Invalid Month Value'
                        error_list.append(error)
                        # print(error_list)
                    if int(year) < 0:
                        errors['error'] = True
                        error['description'] = 'Invalid Year Value'
                        error_list.append(error)
                        # print(error_list)
    
    elif f2 == 4: # check exact value
        if val != f3:
            errors['error'] = True
            if field == 'currency':
                error['description'] = 'Invalid Currency'
            elif field == 'year':
                error['description'] = 'Invalid Year'
            error_list.append(error)
            # print(error_list)

    elif f2 == 5: # date for user remark
        current_date = datetime.now().date()
        current_date = current_date.strftime('%y%m%d')
        
        user_date = val[:6]
        user_year = int(user_date[:2])
        user_month = int(user_date[2:4])
        user_day = int(user_date[4:6])
        if user_month < 0 or user_month > 12:
            errors['error'] = True
            error['description'] = 'Invalid Date'
            error_list.append(error)
        else:
            first_day, lastday = calendar.monthrange(user_year,user_month)
            if user_day < 0 or user_day > lastday:
                errors['error'] = True
                error['description'] = 'Invalid Date'
                error_list.append(error)

        # print('year: ',str(int(user_year)),' '+str(int(user_month))+' '+str(int(user_day)))

        user_time = val[-4:]
        hour = int(user_time[:2])
        minute = int(user_time[2:])
        if hour > 23 or hour < 0 or minute > 59 or minute < 0:
            errors['error'] = True
            error['description'] = 'Invalid Time'
            error_list.append(error)
            # print(error_list)

    elif f2 == 6: # compare to current date
        current_date = datetime.now().date()
        current_date = current_date.strftime('%Y-%m-%d')
        if current_date != val:
            errors['error'] = True
            error['description'] = 'Wrong Date'
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
            error['description'] = 'Invalid Length'
            error_list.append(error)
            # print(error_list)

        if int(month) <= 0 or int(month) > 12:
            errors['error'] = True
            error['description'] = 'Invalid Month'
            error_list.append(error)
            # print(error_list)

        year = val_str[-2:]
        if int(year) <= 0:
            errors['error'] = True
            error['description'] = 'Invalid Year'
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
                    error['description'] = 'Not Balanced With Credit Row '+str(row-1)
                elif field == 'credit_in_account_currency':
                    error['description'] = 'Not Balanced With Debit Row '+str(row-1)
                error['val']=str(error['val'])
                error['value']=str(error['value'])
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
                        'description':'Wrong Data'
                    }
                error_list.append(error)

def handleError(file,cr):
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
    print('######cr: ',cr)
    for row in cr:
        # debit
        # try:
        #     row['debit']
        #     counter = 1
        # except:
        #     counter = 2
        print('---: ',row)
        # print(row)

        row_count += 1
        posting_date = row['posting_date']
        group = row['group']

        posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
        posting_date_list.append(posting_dates)
        groups = {'row':row_count,'field':'group','val':group}
        group_list.append(groups)
            
        # if counter == 1:
        balance['counter'] = balance_counter
        getError(file,row,row_count,error_list,errors,balance)

        if balance_counter == 1:
            try:
                balance['val'] = row['debit']
            except:
                balance['val'] = row['credit']
            balance_counter = 2

        elif balance_counter == 2:
            # balance['counter'] = balance_counter
            getError(file,row,row_count,error_list,errors,balance)
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



# for collection

def makeDict2(row,counter,isCollection):
    # print('counter: ',counter,' val: ',row[15])
    print('-------------------makeDict----------------')
    print(row)
    if(isCollection):
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
            'is_jb': 1 if row[33] else 0,
        }
        try:
            dicts['profit_or_cost_center_number'] = row[34]
        except:
            pass
    else:
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

def getDict2(cr,isCollection):
    dict_list = []
    counter = 1     # 1 for debit, 2 for credit
    counters = 0    # 0 for next pair, 1 for current pair
    seq = 0         # 0 for 1st partner, 1 for 2nd partner
    print('------------------getDict-----------------')
    print(cr)
    for r in cr:
        if counters == 0:
            if float(r[15]) > 0:
                counter = 1
            else:
                counter = 2
            seq = 1
            counters = 1
        if counters == 1:
            if counter == 1 and seq != 3:
                # for debit
                new_row = makeDict2(r,counter,isCollection)
                # print('1')
                counter = 2

            elif counter == 2 and seq != 3:
                # for credit
                new_row = makeDict2(r,counter,isCollection)
                # print('2')
                counter = 1
            dict_list.append(new_row)
        seq += 1
        if seq == 3:
            seq = 0
            counters = 0
    # for l in dict_list:
    #     try:
    #         print('debit-- ',l['debit'])
    #         # print(l['debit'])
    #     except:
    #         print('credit-- ',l['credit'])
    #         # print(l['credit'])
    return dict_list

def getCr2(filename,posting_dates):
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
            r[30] = posting_dates
            cr.append(r)

    print('-----------------------getCrString15-------------------',cr[1][1])
    print(cr)
    cr_dict = getDict2(cr)
    print('typeee getCr: ',type(cr_dict))
    return cr_dict,cr

def getCr2_pass_file(zip,file,isCollection):
    print('file: ',file)
    # print(file_url)
    cr = []
    with zip.open(file, 'r') as csv_file:
        # file.read().decode('utf-8')
        read_file = csv_file.read().decode('utf-8')
        reader = csv.reader(read_file.strip().splitlines())
        print(read_file)
        for r in reader:
            print('row: ',r)
            cr.append(r)
    print('-----------------------getCrString15-------------------',cr[1][1])
    print(cr)
    cr_dict = getDict2(cr,isCollection)
    print('typeee getCr: ',type(cr_dict))
    return cr_dict,cr

def getError2(file,row_list,row,error_list,errors,balance):
    year = row_list['year']
    account_number = row_list['account_number']
    cost_center_number = row_list['cost_center_number']
    currency = row_list['currency']
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
    # objRevenueAccount = {'field':'revenue_account','value':revenue_account,'doctype':'Account'}
    objUserRemark = {'field':'user_remark','value':remark}
    
    # year
    result = True
    checkEmpty(file,objYear,row,errors,error_list)
    result = checkError2(file,objYear,2,'number',row,errors,error_list,'')  # check number type
    if result:
        current_year = datetime.now().date().year
        checkError2(file,objYear,4,str(current_year),row,errors,error_list,'')  # check current year
    # account
    checkEmpty(file,objAccount,row,errors,error_list)
    checkError2(file,objAccount,2,'number',row,errors,error_list,'')  # check number type
    checkError2(file,objAccount,1,'',row,errors,error_list,'')    # check exist
    # # cost center
    checkEmpty(file,objCost,row,errors,error_list)
    checkError2(file,objCost,1,'',row,errors,error_list,'') # check exist
    # #currency
    # checkError(objCurrency,2,'string',row,errors,error_list,'') # check string type
    checkEmpty(file,objCurrency,row,errors,error_list)
    checkError2(file,objCurrency,4,'MYR',row,errors,error_list,'') # check value MYR
    # # debit
    if amt_type == 'debit':
        f1 = {'field':'debit_in_account_currency','value':float(debit_credit)}
        checkError2(file,f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(file,f1,row,errors,error_list)
        # balance = checkError(f1,'','',row,errors,error_list,'') # get value
        checkError2(file,f1,'','',row,errors,error_list,balance) # get value
    # credit
    elif amt_type == 'credit':
        f1 = {'field':'credit_in_account_currency','value':abs(float(debit_credit))}
        checkError2(file,f1,2,'float',row,errors,error_list,'') # check float type
        checkEmpty(file,f1,row,errors,error_list)
        checkError2(file,f1,'','',row,errors,error_list,balance)  # check balance
    
    # # user remark
    # checkEmpty(objUserRemark,row,errors,error_list)
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

def checkError2(file,f1,f2,f3,row,errors,error_list,balance):
    # f1(data), f2(error type), f3(number/string, length), f4(),balance
    # checkExist('Account','account_number',row_list['account_number'],row,error_list,errors)
    field = f1['field']
    val = f1['value']
    error = {
        'filename':file,
        'row':row,
        'field':field,
        'value':val
    }

    if f2 == 1: # check record existence and ..
        doctype = f1['doctype']
        if f3 == '':
            try:
                obj = frappe.get_last_doc(doctype,filters={field:val})
            except:
                errors['error'] = True
                error['description'] = 'Invalid Data'
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
                error['description'] = doctype + ' Not Exist'
                error_list.append(error)
                # print(error_list)

    elif f2 == 2: # check format
        if f3 == 'string':  # only string
            if not val.isdigit():
                return True
            else:
                errors['error'] = True
                error['description'] = 'Invalid Format'
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
                error['description'] = 'Invalid Format'
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
                        error['description'] = 'Invalid Value'
                        error_list.append(error)
                        return False
                    return True
                return True
            except:
                errors['error'] = True
                error['description'] = 'Invalid Format'
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
                error['description'] = 'Invalid Length'
                error_list.append(error)
                # print(error_list)
            else:
                if field == 'current month':
                    month = str(val)[0:2]
                    year = str(val)[2:]
                    if int(month) > 12 or int(month) < 0:
                        errors['error'] = True
                        error['description'] = 'Invalid Month Value'
                        error_list.append(error)
                        # print(error_list)
                    if int(year) < 0:
                        errors['error'] = True
                        error['description'] = 'Invalid Year Value'
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
                error['description'] = 'Invalid Currency'
            elif field == 'year':
                error['description'] = 'Invalid Year'
            error_list.append(error)
            # print(error_list)

    elif f2 == 5: # date for user remark
        current_date = datetime.now().date()
        current_date = current_date.strftime('%y%m%d')
        
        user_date = val[:6]
        user_year = int(user_date[:2])
        user_month = int(user_date[2:4])
        user_day = int(user_date[4:6])
        if user_month < 0 or user_month > 12:
            errors['error'] = True
            error['description'] = 'Invalid Date'
            error_list.append(error)
        else:
            first_day, lastday = calendar.monthrange(user_year,user_month)
            if user_day < 0 or user_day > lastday:
                errors['error'] = True
                error['description'] = 'Invalid Date'
                error_list.append(error)

        # print('year: ',str(int(user_year)),' '+str(int(user_month))+' '+str(int(user_day)))

        user_time = val[-4:]
        hour = int(user_time[:2])
        minute = int(user_time[2:])
        if hour > 23 or hour < 0 or minute > 59 or minute < 0:
            errors['error'] = True
            error['description'] = 'Invalid Time'
            error_list.append(error)
            # print(error_list)

    elif f2 == 6: # compare to current date
        current_date = datetime.now().date()
        current_date = current_date.strftime('%Y-%m-%d')
        if current_date != val:
            errors['error'] = True
            error['description'] = 'Wrong Date'
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
            error['description'] = 'Invalid Length'
            error_list.append(error)
            # print(error_list)

        if int(month) <= 0 or int(month) > 12:
            errors['error'] = True
            error['description'] = 'Invalid Month'
            error_list.append(error)
            # print(error_list)

        year = val_str[-2:]
        if int(year) <= 0:
            errors['error'] = True
            error['description'] = 'Invalid Year'
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
                    error['description'] = 'Not Balanced With Credit Row '+str(row-1)
                elif field == 'credit_in_account_currency':
                    error['description'] = 'Not Balanced With Debit Row '+str(row-1)
                print('error1: ',error,' val: ',val,' another: ',balance['val'])
                error_list.append(error)

def checkDominant2(f1,errors,error_list):
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
                        'description':'Wrong Data'
                    }
                error_list.append(error)

def handleError2(file,cr):
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
    print('######cr: ',cr)
    for row in cr:
        # debit
        # try:
        #     row['debit']
        #     counter = 1
        # except:
        #     counter = 2
        print('---: ',row)
        # print(row)

        row_count += 1
        posting_date = row['posting_date']
        group = row['group']

        posting_dates = {'row':row_count,'field':'posting_date','val':posting_date}
        posting_date_list.append(posting_dates)
        groups = {'row':row_count,'field':'group','val':group}
        group_list.append(groups)
            
        # if counter == 1:
        balance['counter'] = balance_counter
        getError2(file,row,row_count,error_list,errors,balance)

        if balance_counter == 1:
            try:
                balance['val'] = row['debit']
            except:
                balance['val'] = row['credit']
            balance_counter = 2

        elif balance_counter == 2:
            # balance['counter'] = balance_counter
            getError2(file,row,row_count,error_list,errors,balance)
            balance_counter = 1
            


    # check posting date dominant error
    # checkDominant(posting_date_list,errors,error_list)
    # check group dominant error
    checkDominant2(group_list,errors,error_list)
    
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

