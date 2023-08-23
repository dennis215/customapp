# Copyright (c) 2023, mysite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
# from customapp.scheduler_import_billing_report import doImportBillingReport
from customapp.deferred_revenue import deferredRevenue
import time
from datetime import datetime, date
from customapp.general_function import getDocList, getDoc, getLastDay, getDatetimeFull
import calendar
# from apscheduler.schedulers.background import BackgroundScheduler

class SchedulerManager(Document):
	def before_insert(self):
		name = self.scheduler
		self.name1 = name

		return True
	
	def after_insert(self):
		return True

	def on_update(self):
		try:
			job_type = self.scheduled_job_type
		except:
			return
		# print('job type: ',job_type)
		exist = False
		periodic = self.periodic
		try:
			job = frappe.get_last_doc('Scheduled Job Type',filters={'name':job_type})
			self.scheduled_job_type_method = job.method
			# sch = frappe.get_last_doc('Scheduled Job Type',filters={'method':job_name.method})
			# exist = True
			
		except Exception as e:
			print('exception weh: ',str(e))
			return True
		
		# if exist:
		if job:
			if self.control == 'Play':
				job.stopped = 0
				print('----------played-----------')
			else:
				job.stopped = 1
				print('----------stopped------------')
		
			if self.scheduler == 'Deferred Revenue (Export)' or self.scheduler == 'Collection Report (Export)' or self.scheduler == 'Billing Report (Export)':
				cron_format = '59 23 * * *'
				if self.follow_periodic == 'Yes':
					if periodic == 'Month End':
						now = datetime.now()
						last_day = calendar.monthrange(now.year, now.month)[1]
						cron_format = '59 23 '+str(last_day)+' * *'
				
				elif self.follow_periodic == 'Every Minute':
					cron_format = '* * * * *'
				
				print('cron format: ',cron_format)
				print('periodic: ',periodic)
				job.cron_format = cron_format

			elif self.scheduler == 'Accounting Period':
				closing_day = self.closing_day
				try:
					times = int(self.every_minute)
					timing = True
					if times == 0:
						timing = False
				except:
					timing = False
				if closing_day < 1:
					print('Closing day cannot be less than 1!')
					raise Exception('Closing day cannot be more than 1!')
				accper_exist = getDocList('Accounting Period','',True)
				if not accper_exist:
					print('No Previous Accounting Period Exist!')
					start_date = date(day=1,month=3,year=2023)
				else:
					accper = getDoc('Accounting Period')
					start_date = accper.start_date
				month = start_date.month
				year = start_date.year
				month += 1
				if month > 12:
					month = 1
					year += 1
				last_day = getLastDay(month,year)
				if last_day < closing_day:
					print('Closing Day cannot be more than the number of day of current month')
					raise Exception('Invalid Closing Day!')
				# cron_format = '1 * '+str(closing_day)+' '+str(month)+' '+str(year)

				if timing:
					cron_format = '*/'+str(times)+' * * * *'
					job.cron_format = cron_format
			job.save()
		frappe.db.commit()
			
		return True

def getCronFormat(minute):
	# if interval < 59:
	if minute > 1:
		cron_format = '*/'+str(minute)+' * * * *'
	elif minute == 1:
		cron_format = '* * * * *'
	else:
		cron_format = '* * * * *'
	return cron_format