from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time
import csv

#https://www.youtube.com/watch?v=jOzTLAUh7-w 참고 유튜브

class QueenitCrawler:
    def __init__(self, save_path='C:/queenit'):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.csv_path = os.path.join(self.save_path, 'queenit_crawl.csv')
        self.product_links = []

    def crawl_images(self):
        # Selenium을 사용하여 동적 로딩 대응
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get('https://web.queenit.kr/')
        
        # 앱 다음에 받기 닫기 버튼 클릭
        try:
            close_iwillgetapplater_button = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/button[1]")
            driver.execute_script("arguments[0].click();", close_iwillgetapplater_button)
            print("잠깐! 웹으로 보고 계신가요? 닫아짐.")
            time.sleep(10)
        except NoSuchElementException:
            print("앱 다음에 받기 버튼을 찾지 못함ㅠ")
        #html/body/div/div/div/div/div[4]/div[2]/div[3]/div/div[1]/div[1]/span/img
        
        # 상의 클릭
        #upper_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div[5]/div[1]/div")
        upper_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div[5]/div[1]/div/div[1]")
        driver.execute_script("arguments[0].click();", upper_button)
        print("상의 클릭.")
        time.sleep(10)


        for _ in range(4):
            driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
            time.sleep(7)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')        
        img_tags = soup.select('img_selector')  # 실제 선택자로 변경 필요
        link_tags = soup.select('a_selector')  # 실제 선택자로 변경 필요

        # 상품 저장할 리스트 생성
        products = []

        # 이미지 URL을 중복 없이 저장하기 위한 set
        image_urls = set()

        #찾을 div
        #product_blocks = soup.find_all('div', class_='css-7ny53m')

        # 찾을 div
        try:
            product_blocks = soup.find_all('div', class_='css-7ny53m')  # 실제 CSS 선택자로 교체
        except AttributeError:
            print("WebDriver 객체에 'find_elements_by_css_selector' 메소드가 없습니다.")
            driver.quit()
            exit()

        for i, block in enumerate(product_blocks):
            img_element = block.find_element_by_css_selector('img')  # 실제 CSS 선택자로 교체
            img_url = img_element.get_attribute('src')
            img_name = f"product_{i}.jpg"

            if img_url not in image_urls:
                # 이미지 저장
                with open(os.path.join(self.save_path, img_name), 'wb') as f:
                    img_data = requests.get(img_url).content
                    f.write(img_data)

                # 상품 정보 저장 (예시)
                name = "example_name"
                price = "example_price"
                products.append({
                    'Name': name,
                    'Price': price,
                    'ImageURL': img_url
                })

                image_urls.add(img_url)

        # CSV 파일로 상품 정보 저장
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'ImageURL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)

        # Selenium 드라이버 종료
        driver.quit()

if __name__ == '__main__':
    crawler = QueenitCrawler()
    crawler.crawl_images()


