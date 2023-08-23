# Copyright (c) 2023, mysite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import csv, calendar
from datetime import date, datetime

class DeferredRevenueJournalEntry(Document):
	def before_insert(self):
		# return True
		# dates = self.tag_id
		# month = dates.month
		# year = dates.year
		# monthname = calendar.month_name[month]
		# doc_name = str(monthname)+' '+str(year)
		# self.doc_name = doc_name



		# ---------------------------real punya
		# now = datetime.now()
		# month = now.replace(month=now.month - 1).strftime('%B')
		# self.doc_name = month +' '+ now.strftime('%Y')

		# ---------------------------iwk testing
		# docs = frappe.get_list('Deferred Revenue Journal Entry')
		# if docs:
		# 	doc = frappe.get_last_doc('Deferred Revenue Journal Entry')
		# 	# doc = frappe.get_last_doc('Deferred Revenue Journal Entry')
		# 	name = doc.doc_name
		# 	split = name.split()
		# 	month = datetime.strptime(split[0],'%B').month
		# 	month = str(month + 1)
		# 	month = datetime.strptime(month, '%m')
		# 	month = month.strftime('%B')
		# 	print('month: ',month)
		# 	year = datetime.now().year
		# 	name = month +' ' +str(year)
		# 	self.doc_name = name
		# else:
		# 	self.doc_name = 'January 2023'
		# now = datetime.now()
		# doc.doc_name = 
		# now.strftime('%Y')






		# acsv = self.billing_report_csv
		# cr = []
		# site = frappe.utils.get_site_path()
		# split = site.split('/')
		# site = split[1]
		# print('site: ',site)
		# print('acsv: ',acsv)
		# acsv = site+acsv
		# if acsv != '':
		# 	with open(acsv,'r') as file:
		# 		reader = csv.reader(file)
		# 		# print('reader')
		# 		# print(reader)
		# 		for r in reader:
		# 			# print('row: ',r)
		# 			cr.append(r)
		# print('---------cr')
		# print(cr)
		# print('length: ',len(cr))
		# for c in cr:
		# 	print(c)

		# llist = createAccountEntries(cr)
		# # print('list 1')
		# # print(llist[0])
		# # print('llist 2')
		# # print(llist[1])
		# for l in llist:
		# 	self.append('accounts',l)
		return True

	# def after_insert(self):
	# 	now = datetime.now()
	# 	month = now.replace(month=now.month - 1).strftime('%B')
	# 	self.name = month + now.strftime('%Y')

def getDict(cr):
	row_list = []
	counter = 1
	for row in cr:
		if counter == 1:
			counter += 1
			year = row[1]
			account_number = row[2]
			cost_center_number = row[3]
			currency = row[12]
			debit = row[15]
			remark = row[23]
			posting_date = row[30]
			group = row[31]
			tax_amount = row[32]
			tax_code = row[33]
			second_cost_center_number = row[34]
			san_count = row[35]
			monthly_charge = row[36]
			month_count = row[37]
			current_month = row[38]
			revenue_account = row[39]
			# try:
			# 	revenue_account = row[39]
			# except:
			# 	revenue_account = 0
			
			if revenue_account:
				# print('account number: ',account_number)
				account = frappe.get_last_doc('Account',filters={'account_number':account_number})
				# print('cost center: ',cost_center_number)
				cost_center = frappe.get_last_doc('Cost Center', filters={'cost_center_number':cost_center_number})

				rows_dict = {
					'account':account.name,
					'account_number':account_number,
					'cost_center':cost_center.name,
					'cost_center_number':cost_center_number,
					# 'cost_center':cost_center.name,
					'currency':currency,
					'debit_in_account_currency' : float(debit),
					'credit_in_account_currency' : float(0),
					'remark':remark,
					'group':group,
					'year': year,
					'posting_date':posting_date,
					'tax_amount':tax_amount,
					'tax_code':tax_code,
					'second_cost_center_number':second_cost_center_number,
					'san_count':san_count,
					'monthly_charge':monthly_charge,
					'month_count':month_count,
					'current_month':current_month,
					'revenue_account':revenue_account
				}
				print('row dict 1')
				print(rows_dict)
				row_list.append(rows_dict)
			else:
				continue
		elif counter == 2:
			counter = 1
			year = row[1]
			account_number = row[2]
			cost_center_number = row[3]
			currency = row[12]
			credit = abs(float(row[15]))
			remark = row[23]
			posting_date = row[30]
			group = row[31]
			tax_amount = row[32]
			tax_code = row[33]
			second_cost_center_number = row[34]
			san_count = row[35]
			monthly_charge = row[36]
			month_count = row[37]
			current_month = row[38]
			revenue_account = row[39]
			# try:
			# 	revenue_account = row[39]
			# except:
			# 	revenue_account = 0
			
			if revenue_account:
				# print('account number: ',account_number)
				account = frappe.get_last_doc('Account',filters={'account_number':account_number})
				cost_center = frappe.get_last_doc('Cost Center', filters={'cost_center_number':cost_center_number})

				rows_dict = {
					'account':account.name,
					'account_number':account_number,
					'cost_center':cost_center.name,
					'cost_center_number':cost_center_number,
					# 'cost_center':cost_center.name,
					'currency':currency,
					'debit_in_account_currency' : float(0),
					'credit_in_account_currency' : float(credit),
					'remark':remark,
					'group':group,
					'year': year,
					'posting_date':posting_date,
					'tax_amount':tax_amount,
					'tax_code':tax_code,
					'second_cost_center_number':second_cost_center_number,
					'san_count':san_count,
					'monthly_charge':monthly_charge,
					'month_count':month_count,
					'current_month':current_month,
					'revenue_account':revenue_account
				}
				print('row dict 2')
				print(rows_dict)
				row_list.append(rows_dict)
			else:
				continue
	print('row list: ')
	print(row_list)
	return row_list
		

def createAccountEntries(cr):
	ddict = getDict(cr)
	print('length: ',len(ddict))
	llist = []
	for d in ddict:
		# print(d)
		# print(d.account)
		llist.append(d)
	return llist

