from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import webbrowser
import base64
import requests
import urllib.request
import os
import time

url = "https://snowe.sookmyung.ac.kr/bbs5/users/login"

browser = webdriver.Chrome()
browser.implicitly_wait(10) # 페이지가 로딩될 때까지 최대 10초 기다림
browser.maximize_window() # 화면 최대화
browser.get(url) # 페이지 열기 

# 아이디 입력
# <input type="text" title="아이디" class="input_txt" name="userId" id="userId" value="" placeholder="아이디" minlength="3" maxlength="20">
id = browser.find_element(By.ID, 'userId')
id.click()
id.send_keys("c3nqmy39i")
time.sleep(0.5) # 로그인 입력 0.5초 대기기

# 비밀번호 입력
# <input type="password" title="비밀번호" class="input_txt pw" name="userPassword" id="userPassword" placeholder="비밀번호" minlength="4" maxlength="50">
pw = browser.find_element(By.ID, 'userPassword')
pw.click()
pw.send_keys("0nej2vwn0")

# 로그인 클릭
# <button type="submit" id="loginButton" alt="로그인">로그인</button>
login_btn = browser.find_element(By.ID, 'loginButton')
login_btn.click()

# '교내식당 시간표' 버튼 클릭
# <a href="/bbs5/boards/cafeteria" title="교내식당 식단표">교내식당 식단표</a>

cafeteria_btn = browser.find_element(By.CLASS_NAME, 'meal')
cafeteria_btn.click()

# 날짜별 식단표 버튼 클릭
message_list = browser.find_element(By.CSS_SELECTOR, '#messageList > li:nth-child(1) > a > span')
message_list.click()

# 페이지 소스 가져와서 BeautifulSoup 객체 생성
soup = BeautifulSoup(browser.page_source, 'html.parser')

# 날짜별 식단표 이름 가져오기
img_name = soup.select_one('#messageList > li:nth-child(1) > a > span')

# 이미지 찾기
img_element = browser.find_element(By.CSS_SELECTOR, '#_ckeditorContents > p > img')

# 이미지 URL 추출
img_url = img_element.get_attribute('src')

# 드라이버 종료
browser.quit()

# 이미지 저장 이름
img_name = f"{img_name.text}.png"

# 저장 경로
save_path = r"E:\python_crawling\img"

# 'data:image/png;base64,' 부분 제거하고 base64 인코딩된 데이터만 추출
if img_url.startswith('data:image'):
    img_data = img_url.split('base64,')[1]
    img_bytes = base64.b64decode(img_data)

    # 이미지 저장
    img_path = os.path.join(save_path, img_name)
    with open(img_path, 'wb') as file:
        file.write(img_bytes)

    print(f"이미지 저장 완료: {img_path}")
else:
    print("이미지 URL이 올바른 base64 형식이 아닙니다.")

# HTML 코드 생성
html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>식단표</title>
</head>
<body>
    <div style="text-align:center;">
        <h1>이번 주 식단표</h1>
        <img src="{img_path}" width="80%" height="65%">
    </div>
</body>
</html>
"""

# HTML 파일 저장 경로
html_file_path = r"E:\python_crawling\output.html"
with open(html_file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

# **여기서 웹 브라우저 열기!** (Selenium이 아니라 webbrowser 사용)
webbrowser.open(f"file:///{html_file_path}")
print("------------------------------------------")
print("             ")
print("주소는", html_file_path)
print("             ")
print("------------------------------------------")