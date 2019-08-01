from time import sleep
from config import driver, email, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login():
    print('logging in...')
    try:
        driver.get('https://intranet.hbtn.io')
        driver.find_element_by_id("user_login").send_keys(email)
        driver.find_element_by_id("user_password").send_keys(password)
        driver.find_element_by_name("commit").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'signed_in')))
    except:
        print("login failed.")
        driver.quit()
        exit()


def checker(project, problems):
    for count, problem in enumerate(problems):
        print('checking #' + str(problem) + '...')
        if count != 0:
            driver.execute_script('window.open('');')
            driver.switch_to.window(driver.window_handles[count])
        driver.get('https://intranet.hbtn.io/projects/' + project)
        buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Check your code?')]")

        try:
            buttons[problem].click()
            sleep(0.5)
            check = driver.find_elements_by_class_name('correction_request_test_admin')
            check[problem].click()
        except IndexError:
            print(str(problem) + ' is not a valid problem number, or cannot be checked.')
    return problems


def results(problems):
    old_code_passed = []
    old_code_failed = []
    old_req_passed = []
    old_req_failed = []
    for count, problem in enumerate(problems):
        driver.switch_to.window(driver.window_handles[count])
        sleep(1)  # allow time for tab switch
        try:
            sleep(25)  # sleep
            code_passed = driver.find_elements_by_xpath('//*[@title="Correct output of your code - success"]')
            code_failed = driver.find_elements_by_xpath('//*[@title="Correct output of your code - fail"]')
            req_passed = driver.find_elements_by_xpath('//*[@title="Requirement - success"]')
            req_failed = driver.find_elements_by_xpath('//*[@title="Requirement - fail"]')
            code_passed_count = len(code_passed) - len(old_code_passed)
            code_failed_count = len(code_failed) - len(old_code_failed)
            req_passed_count = len(req_passed) - len(old_req_passed)
            req_failed_count = len(req_failed) - len(old_req_failed)

            print('-------- Problem #' + str(problem) + ' --------')
            print('REQUIREMENTS: ' + str(req_passed_count) + ' passed. ' + str(req_failed_count) + ' failed.')
            print('OUTPUT: ' + str(code_passed_count) + ' passed. ' + str(code_failed_count) + ' failed.')

            if count == 0 or code_passed_count:
                old_code_passed = code_passed[:]
            if count == 0 or code_failed_count:
                old_code_failed = code_failed[:]
            if count == 0 or req_passed_count:
                old_req_passed = req_passed[:]
            if count == 0 or req_failed_count:
                old_req_failed = req_failed[:]
        except:
            print('-------- Problem #' + str(problem) + ' --------')
            print('Results failed to load.')
