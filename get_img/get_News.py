import json, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from selenium import webdriver
from newspaper import Article
from newspaper import Config

load_dotenv()

AGENT = os.environ.get('USER_AGENT')
NEWS_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?hl=" 
LANGUAGES = ["en","ko"] #"ko"

#agent 헤더 설정
header = {"User-Agent":AGENT}

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
#options.headless = True
#options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(options=options)

#뉴스 페이지로 이동
driver.get(NEWS_URL+LANGUAGES[0])


# 현재 시간
now = datetime.now()
one_hour_ago = now - timedelta(hours=1)

# 뉴스 아이템 크롤링
news_items = driver.find_elements_by_css_selector("article")

news_list = []
for item in news_items:
    try:
        #1시간이 넘은 뉴스는 패스
        #news_time = datetime.strptime(item.find_element_by_css_selector("time").get_attribute("datetime"),"%Y-%m-%dT%H:%M:%SZ")
        #if(3600<now-news_items):
        #   continue

        #뉴스 상세페이지 링크
        link = item.find_element_by_class_name("gPFEn").get_attribute("href")

        #뉴스 분석
        config = Config()
        config.browser_user_agent = AGENT
        article = Article(link, languge=LANGUAGES[0], config=config)
        article.download()
        article.parse()

        #값을 못받아오면 저장X
        if article.title and article.title:
           news_list.append({"title":article.title, "summary":article.text, "url":article.url})

    except Exception as e:
        print(f"Error processing item: {e}")

result_news = {"length":len(news_list),"time": now.strftime("%Y-%m-%d %H:%M:%S"), "news": news_list}

# 드라이버 종료
driver.quit()

# result_news를 JSON 형식의 텍스트 파일로 저장
with open("result_newsT3.txt", "w", encoding="utf-8") as file:
    json.dump(result_news, file, ensure_ascii=False, indent=4)