import frappe

def test():
    # url = frappe.utils.get_url()
    # print('url: ',url)
    # urls = frappe.utils.get_url_to_list('Journal Entry')
    # print('urls: ',urls)
    from urllib.parse import urlparse

    # Get the current URL
    current_url = frappe.local.request.url

    # Parse the URL to extract the domain name
    parsed_url = urlparse(current_url)
    domain_name = parsed_url.netloc

    print(domain_name)