from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# To check keys if the login is successful
def check_keys(username, password, username_box, password_box, login_box,driver):
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
def check_user_key(username,username_box,login_box,driver):
    current_url = driver.current_url
    username_box.send_keys(username)
    login_box.submit()
    
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))
    
    if(driver.find_elements_by_class_name("webcam")):
        return True
    else:
        return False

# To determining the category of login credentials
def determine_type(link,driver):
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
  
#  Check if it is without any password
def no_pass_check(ip,help_dict,driver):
    driver.get(ip)
    if("id" in help_dict.keys()):
        if(driver.find_elements_by_id(help_dict["id"])):
            return True
        return False
    elif("class" in help_dict.keys()):
        if(driver.find_elements_by_class_name(help_dict["class"])):
            return True
        return False


