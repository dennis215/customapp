import frappe
from datetime import datetime,date,timedelta
import csv, requests, json, calendar, os,zipfile,io
# from frappe.utils.file_manager import upload
# from frappe.core.doctype.file.file import File
import io
from customapp.general_function import *
import pytz

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
                
            journal.append('accounts',row)

        # now = datetime.now().date()
        journal.total_debit = total_debit
        journal.total_credit = total_credit
        journal.entry_type = "Journal Entry"
        postingdate=pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.combine(latest_posting, datetime.min.time()))
        journal.posting_date = postingdate.strftime('%Y-%m-%d')
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

# @frappe.whitelist(allow_guest=True)
def doImportCollectionReport():
    errors=[]
    getFileData = {"name": "Collection"}
    headers = {
        "Content-Type": "application/json",
    }
    # prod internal
    # getFileReqUrl = 'http://172.18.96.101:80/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    # returnReqUrl = 'http://172.18.96.101:80/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
    # prod
    # getFileReqUrl = 'https://bsportal.indahwater.app:8443/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    # returnReqUrl = 'https://bsportal.indahwater.app:8443/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
    # Staging
    getFileReqUrl = 'https://bsstg1.indahwater.app:8443/internal/SchedulerEOD/RetrieveFiles?ApiKey=lDw6rUrzz5mf7fdNiiAdEdKort5el21TpcmC'
    returnReqUrl = 'https://bsstg1.indahwater.app:8443/internal/SchedulerEOD/ERPNextFileChecking?ApiKey=vGDkYOrDj5FPhxZrXCKLf5x6lnCIvsSZnsAC'
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
    
