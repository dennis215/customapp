import frappe
from frappe.utils import get_url

def getDomain():
    domain = get_url()
    print('Domain: ',domain)