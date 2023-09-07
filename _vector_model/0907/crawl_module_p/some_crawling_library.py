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
        upper_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div[5]/div[1]/div")
        driver.execute_script("arguments[0].click();", upper_button)
        print("상의 클릭.")
        time.sleep(10)


        for _ in range(200):
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
        product_blocks = soup.find_all('div', class_='css-7ny53m')

        # 이미지 다운로드 횟수 제한
        max_images = 1100
        images_downloaded = 0

        for block in product_blocks:
            if images_downloaded >= max_images:
                break

            name_element = block.find('span', class_='MuiTypography-BodyS')
            name = name_element.find('div', class_='MuiBox-root').text.strip()
            
            price_element = block.find('span', class_='MuiTypography-LabelM')
            price = price_element.find('div', class_='MuiBox-root').text.strip()

            rating_element = block.find('span', class_='MuiTypography-LabelXS')
            rating = rating_element.find('div', class_='MuiBox-root').text.strip() if rating_element else ""
            

            # 이미지 URL 추출 - 두 번째 <img> 태그 선택
            img_elements = block.find_all('img')
            image_url = ""
            for img_element in img_elements:
                if "https://" in img_element['src']:
                    image_url = img_element['src']
                    break
            
            if not image_url:
                continue

            if image_url and image_url not in image_urls:
                products.append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'ImageURL': image_url
                })
                image_urls.add(image_url)
                images_downloaded += 1
                time.sleep(2)
                


        
        for i, img_tag in enumerate(img_tags):
            img_url = img_tag['src']
            img_name = f"product_{i}.jpg"

            # 이미지 저장
            with open(os.path.join(self.save_path, img_name), 'wb') as f:
                img_data = requests.get(img_url).content
                f.write(img_data)

            # 상품 링크 저장
            product_link = link_tags[i]['href']
            self.product_links.append(product_link)
            
        # CSV 파일로 상품 정보 저장
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating', 'ImageURL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
    
        # Selenium 드라이버 종료
        driver.quit()

if __name__ == '__main__':
    crawler = QueenitCrawler()
    crawler.crawl_images()


