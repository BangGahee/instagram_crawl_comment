from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv

def get_instagram_comments(post_url, username, password, page):
    # 웹 드라이버 초기화
    driver = webdriver.Chrome()  # 크롬 드라이버 경로를 적절하게 수정하세요.

    # 인스타그램 접속
    driver.get("https://www.instagram.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))

    # 로그인
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(50)

    # 게시글로 이동
    driver.get(post_url)

    try:
        load_more_comment = driver.find_element(By.CSS_SELECTOR ,"svg[aria-label='댓글 더 읽어들이기']")
        print("Found {}".format(str(load_more_comment)))
        i = 0
        while load_more_comment.is_displayed() and i < int(page):
            load_more_comment.click()
            time.sleep(1.5)
            load_more_comment = driver.find_element(By.CSS_SELECTOR,"svg[aria-label='댓글 더 읽어들이기']")
            print("Found {}".format(str(load_more_comment)))
            i += 1
    except Exception as e:
        print(e)
        pass

    try:
        reply_more_comment = driver.find_element(By.XPATH ,"//*[contains(text(), '답글 보기')]")
        print("Found {}".format(str(reply_more_comment)))
        while reply_more_comment.is_displayed():
            reply_more_comment.click()
            time.sleep(1.5)
            reply_more_comment = driver.find_element(By.XPATH ,"//*[contains(text(), '답글 보기')]")
            print("Found {}".format(str(reply_more_comment)))
    except Exception as e:
        print(e)
        pass

    # 댓글 가져오기
    comments = []
    user_comments = {}
    comment = driver.find_elements(By.CSS_SELECTOR,"ul[class='_a9ym']")
    for c in comment:
        container = c.find_element(By.CSS_SELECTOR,"div[class='_a9zr']")
        name = container.find_element(By.CSS_SELECTOR,"a[role='link']").text
        content = container.find_element(By.CSS_SELECTOR,"span").text
        content = content.replace('\n', ' ').strip().rstrip()
        datetime = c.find_element(By.CSS_SELECTOR,"time").get_attribute("datetime")
        print(name)
        print(content)
        print(datetime)
        user_comments = {'name':name, 'content':content, 'time':datetime}
        comments.append(user_comments)
    #user_names.pop(0)
    #user_comments.pop(0)

    # 드라이버 종료
    driver.quit()

    return comments

# 인스타그램 게시글 URL과 로그인 정보를 입력하세요
# 댓글 긁어올 게시글 주소 입력 
post_url = "https://www.instagram.com/p/포스트정보/"
# 인스타그램 로그인 ID
username = "ID"
# 인스타그램 로그인 PW
password = "Password"

#몇번째 페이지까지 가져올건지 맨 뒤에 파라미터로 넘기기
comments = get_instagram_comments(post_url, username, password, 1000)
print(comments)
#data = json.load(comments)

'''
data[0] 은 json 파일의 한 줄을 보관 {"title:"Super Duper", "songId": ...}
data[0]['컬럼명'] 은 첫 번째 줄의 해당 컬럼 element 보관
'''

with open('output.csv','w',newline='',encoding='utf-8-sig') as f:
    f = csv.writer(f)

    # csv 파일에 header 추가
    f.writerow(["name", "content", "datetime"])
    for datum in comments:
        f.writerow([datum["name"], datum["content"], datum["time"]])
