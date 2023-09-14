# Copyright (c) 2023, mysite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, time, timedelta, date
import csv, json, calendar, os, requests

class CollectionJournalEntryErrorLog(Document):
	def onload(self):
		if not self.seen and not frappe.flags.read_only:
			self.db_set("seen", 1, update_modified=0)
			frappe.db.commit()
	
	# def after_insert(self):
	# 	start_date = self.start_date
	# 	if not isinstance(start_date, str):
	# 		start_date = start_date.strftime('%Y-%m-%d')
	# 	end_date = start_date

	# 	file,filename,path = createcsv(start_date,end_date)
	# 	print('FILENAME: ',filename)

	# 	# file_name = save_file(fname=filename, content=file.read(), dt="attachcsv", dn=self.name)
	# 	file_doc = frappe.get_doc({
	# 		"doctype": "File",
	# 		"file_url": "/files/"+filename,
	# 		# "file_url": "/collection_report/"+filename,
	# 		# "file_url": path,
	# 		"file_name": filename,
	# 		# "attached_to_doctype": self.doctype,
	# 		# "attached_to_name": self.name,
	# 		"content": frappe.read_file(path)
	# 	})
	# 	# file_doc.insert(ignore_permissions=True)
	# 	file_doc.save()
	# 	print('file url: ',file_doc.file_url)
	# 	self.collection_report_csv = file_doc.file_url
	# 	return True

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

def getCR(start_end_year):
    start_date = start_end_year['start_date']
    end_date = start_end_year['end_date']
    year = start_end_year['year']
    reportcr = frappe.get_last_doc("API Key", filters={'api_name':'ERPNextMthEndJob'})
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

def getDateOnly(start_date):
	date_only = start_date[:10]
	new_date = datetime.strptime(date_only,'%Y-%m-%d')
	year = new_date.year
	day = new_date.day
	month = new_date.month
	new_date = date(year,month,day)
	print('new_date: ',new_date)
	return new_date

def createcsv(start_date, end_date):
	start_date = datetime.strptime(start_date,'%Y-%m-%d')
	end_date = datetime.strptime(end_date,'%Y-%m-%d')
	dates = {'start_date':start_date,'end_date':end_date}
	start_date, end_date, year = getIsoDate(dates)
	start_end_year = {'start_date':start_date,'end_date':end_date,'year':year}
	ready,cr = getCR(start_end_year)
	print('CR: ',cr)

	if ready:
		# path = 'collection_report'
		path = 'mysite.localhost/public/files'
		date_name = getDateOnly(start_date)
		print('DATE NAME -------------------: ',date_name)
		pathtofile = path+'/Attach_CSV_'+ str(date_name)+'.csv'
		filename = 'Attach_CSV_' + str(date_name)+'.csv'

		if os.path.exists(path):
			with open(pathtofile,'w',newline='') as file:
				writer = csv.writer(file)
				for row in cr:
					print('row: ',row)
					writer.writerow(row)
		else:
			os.makedirs(path)
			with open(pathtofile,'w',newline='') as file:
				writer = csv.writer(file)
				for row in cr:
					print('row: ',row)
					writer.writerow(row)
		
		with open(pathtofile,'rb') as file:
			print('return file')
			return file, filename, pathtofile