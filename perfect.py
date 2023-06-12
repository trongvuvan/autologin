import requests
from bs4 import BeautifulSoup
proxies = {
    "http" : "http://localhost:8080",
    "https" : "http://localhost:8080"
}
def login_to_dvwa(loginurl,userparam,passparam,csrfparam,username,password):
    # Set up a session
    login_data = {
        userparam: username,
        passparam: password,
    }
    session = requests.Session()

    # Send a GET request to retrieve the login page
    response = session.get(loginurl,verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    button_element = soup.find('button')
    if button_element:
    # Get the name and value attributes of the button
        button_name = button_element.get('name')
        button_value = button_element.get('value')
        login_data[button_name] = button_value
    # Extract the CSRF token from the login form\
    loginname = ''
    loginvalue = ''
    csrf_token = ''
    try :
        csrf_token = soup.find('input', {'name': csrfparam}).get('value')
        login_data[csrfparam] = csrf_token
    except :
        print("nothings")
    try :
        loginvalue = soup.find('input', {'type': 'submit'}).get('value')
        loginname = soup.find('input', {'type': 'submit'}).get('name')
        login_data[loginname] = loginvalue
    except:
        print("nothings")
        # Send a POST request to the login page with the login data
    response = session.post(loginurl, data=login_data,proxies=proxies,verify=False)
    print(login_data)
    # Check if the login was successful by analyzing the response
    if 'Welcome' in response.text:
        print("Login successful!")
    else:
        print("Login failed.")
    return session

# Usage example:
dvwa_url = 'http://127.0.0.1:3456/login.php'  # Replace with the actual DVWA URL
username = 'admin'  # Replace with the DVWA username
password = 'password'  # Replace with the DVWA password
userparam = 'username'
passparam = 'password'
csrfparam = 'user_token'
login_to_dvwa(dvwa_url,userparam,passparam,csrfparam,username,password)
