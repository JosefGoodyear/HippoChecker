from time import sleep
from config import driver, email, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def login():
    print('logging in...')
    try:
        driver.get('https://intranet.hbtn.io')
        driver.find_element_by_id("user_login").send_keys(email)
        driver.find_element_by_id("user_password").send_keys(password)
        driver.find_element_by_name("commit").click()
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'signed_in')))
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
            sleep(1)
            check = driver.find_elements_by_class_name('correction_request_test_admin')
            check[problem].click()
        except IndexError:
            print(str(problem) + ' is not a valid problem number, or cannot be checked.')
            pass
    return problems


def results(problems):
    for count, problem in enumerate(problems):
        driver.switch_to.window(driver.window_handles[count])
        sleep(1)  # allow time for tab switch and loading to start
        wait = WebDriverWait(driver, 60)  # if you timeout during results reporting, try increasing this number.
        try:
            wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "check-inline")))
            sleep(1)  # allow time for all results to appear
        except TimeoutException:
            print('-------- Problem #' + str(problem) + ' --------')
            print("Upon reporting results, timeout occurred")
            continue
        code_passed_count = 0
        code_failed_count = 0
        req_passed_count = 0
        req_failed_count = 0
        code_passed = driver.find_elements_by_xpath('//div[@title="Correct output of your code - success"]')
        code_failed = driver.find_elements_by_xpath('//div[@title="Correct output of your code - fail"]')
        req_passed = driver.find_elements_by_xpath('//div[@title="Requirement - success"]')
        req_failed = driver.find_elements_by_xpath('//div[@title="Requirement - fail"]')
        for cp in code_passed:
            if cp.is_displayed():
                code_passed_count += 1
        for cf in code_failed:
            if cf.is_displayed():
                code_failed_count += 1
        for rp in req_passed:
            if rp.is_displayed():
                req_passed_count += 1
        for rf in req_failed:
            if rf.is_displayed():
                req_failed_count += 1
        if code_passed_count == 0 and code_failed_count == 0 and req_passed_count == 0 and req_failed_count == 0:
            print('-------- Problem #' + str(problem) + ' --------')
            print("Results failed to load.")
            continue
        print('-------- Problem #' + str(problem) + ' --------')
        print('REQUIREMENTS: ' + str(req_passed_count) + ' passed. ' + str(req_failed_count) + ' failed.')
        print('OUTPUT: ' + str(code_passed_count) + ' passed. ' + str(code_failed_count) + ' failed.')
