import frappe
from customapp.general_function import *

def doAccountingPeriod():
    print('----wahaioooooo-----')
    exist = getDocList('Scheduler Manager',{'scheduler':'Accounting Period'},True)
    if not exist:
        print('Cannot do Accounting Period Logic since there is no Scheduler for Accounting Period')
        return
    sch = getDoc('Scheduler Manager', {'scheduler':'Accounting Period'})
    if sch.control == 'Stop':
        print('Scheduler for Accounting Period is Stopped!')
        return
    
    print('Scheduler for Accounting Period is Playing!')
    now = datetime.now()
    now_month = now.month
    now_year = now.year
    if now_month == 1:
        now_year -= 1
        now_month = 12
    else:
        now_month -= 1
    
    new_acc_period = frappe.new_doc('Accounting Period')
    month_name = getMonthName(now_month)
    period_name = str(month_name) +' '+str(now_year)
    new_acc_period.period_name = period_name
    new_acc_period.start_date = date(day=1,month=now_month,year=now_year)
    lastday = getLastDay(now_month,now_year)
    new_acc_period.end_date = date(day=lastday,month=now_month,year=now_year)
    new_acc_period.append('closed_documents',{
        'document_type':'Journal Entry',
        'closed':1
    })
    new_acc_period.save()
    frappe.db.commit()
    print('period name: ',period_name)
    print('---------------------yahoooo-----------------------')





