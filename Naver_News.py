import json, time, os
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


load_dotenv()

AGENT = os.getenv("USER_AGENT")
NEWS_URL = "https://news.naver.com/section/"
Category = {"정치":100, "경제":101, "사회":102, "생활/문화":103, "세계":104, "IT/과학":105,"연애":106, "스포츠":107}


def by_Ranking(driver):
    news_list = []

    #언론사별 가장 많이 본 뉴스의 ul 태그들 가져오기
    news_items = driver.find_elements(By.CSS_SELECTOR ,"ul.ranking_list")
    news_items = news_items[0:17]
    for items in news_items:
        #li 태그들
        item = items.find_elements(By.CLASS_NAME ,"rl_coverlink")

        for A_tag in item:
            #뉴스 상세페이지 링크 얻어오기
            link = A_tag.get_attribute("href")
            
            #새 탭에서 상세 페이지 접속
            driver.execute_script(f'window.open("{link}");')
            driver.switch_to.window(driver.window_handles[-1])
                
            #뉴스 상세정보 저장
            news_title = driver.find_element(By.ID, "title_area")
            news_text = driver.find_element(By.ID, "dic_area")
                
            #정상적으로 얻어온 경우만 저장
            if news_title.text and news_text.text:
                news_list.append({"title":news_title.text, "summary":news_text.text, "url":link})

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

    return news_list

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
#options.headless = True
#options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome( options=options)

news_list = []

for value in Category.values():
    try:
        #뉴스 페이지로 이동
        driver.get(NEWS_URL+str(value))
        
        #news_list = by_Ranking(driver) #언론사별 가장 많이 본 뉴스 가져오기 ( 수정필요 )
        
        #최신 뉴스의 시간 요소 가져오기
        news_times = driver.find_elements(By.CSS_SELECTOR ,"div.sa_text_datetime")

        for news_time in news_times:
            #1시간 이상 지난 뉴스 생략
            if  "시간" in news_time.text :# and news_time.text != "1시간전":
                break
            
            #뉴스 상세페이지 링크 가져오기
            el = news_time.find_element(By.XPATH, '../../..')
            link = el.find_element(By.CSS_SELECTOR ,"a").get_attribute("href")
            
            #새 탭에서 상세 페이지 접속
            driver.execute_script(f'window.open("{link}");')
            driver.switch_to.window(driver.window_handles[-1])
            
            #뉴스 상세정보 저장
            news_title = driver.find_element(By.ID, "title_area")
            news_text = driver.find_element(By.ID, "dic_area")
                
            #정상적으로 얻어온 경우만 저장
            if news_title.text and news_text.text:
                news_list.append({"title":news_title.text, "summary":news_text.text, "url":link})

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

    except Exception as e:
        print(f"Error processing item: {e}")


result_news = {"length":len(news_list),"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "news": news_list}

# 드라이버 종료
driver.quit()

# result_news를 JSON 형식의 텍스트 파일로 저장
with open("result_news_Naver.txt", "w", encoding="utf-8") as file:
    json.dump(result_news, file, ensure_ascii=False, indent=4)

