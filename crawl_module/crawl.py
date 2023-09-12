from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import csv
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import requests
from urllib.parse import urlparse
import re

# 파일 이름을 깔끔하게 정리하는 함수
def clean_filename(filename):
    cleaned_filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    return cleaned_filename

# 이미지를 다운로드하는 함수
def download_images(csv_path, save_folder, session):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    headers = {'User-Agent': 'Mozilla/5.0'}  # User-Agent 설정
    with open(csv_path, 'r', encoding='cp949') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            image_url = row['ImageURL']
            parsed_url = urlparse(image_url)
            filename = clean_filename(row['Name']) + os.path.splitext(parsed_url.path)[1]
            save_path = os.path.join(save_folder, filename)

            response = requests.get(image_url,headers=headers, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    response.raw.decode_content = True
                    file.write(response.content)
                print("이미지 다운로드 완료:", save_path)
            else:
                print("이미지 다운로드 실패:", image_url)


class QueenitCrawling:    
    @staticmethod
    def queenit_crawling(url, path_input, category):
        driver = webdriver.Chrome()
        path = os.path.join(path_input, category)

        if not os.path.exists(path):
            os.makedirs(path)


        driver.get(url)
        # Selenium 세션 정보를 가져옵니다.
        cookies = driver.get_cookies()
        session = requests.Session()
        
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # 카테고리별 XPath 설정
        category_xpath = {
            'top': "/html/body/div/div/div/div/div/div/div[5]/div[1]/div",
            "onepiece":"/html/body/div/div/div/div/div/div/div[5]/div[2]/div",
            'pants': "/html/body/div/div/div/div/div/div/div[5]/div[3]/div",
            'outer': "/html/body/div/div/div/div/div/div/div[5]/div[4]/div",
            'skirt': "/html/body/div/div/div/div/div/div/div[5]/div[6]/div"        
            
        }
        
        

        # 앱 다음에 받기 닫기 버튼 클릭
        try:
            close_iwillgetapplater_button = driver.find_element(By.XPATH, "/html/body/div/div/div[3]/button[1]")
            driver.execute_script("arguments[0].click();", close_iwillgetapplater_button)
            print("잠깐! 웹으로 보고 계신가요? 닫아짐.")
            time.sleep(10)
        except NoSuchElementException:
            print("앱 다음에 받기 버튼을 찾지 못함ㅠ")

        # 버튼클릭
        category_button = driver.find_element(By.XPATH, category_xpath[category])
        driver.execute_script("arguments[0].click();", category_button)
        print(f"{category} 클릭.")
        time.sleep(3)


        for _ in range(2):
            driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
            time.sleep(1)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # 상품 저장할 리스트 생성
        products = []

        # 이미지 URL을 중복 없이 저장하기 위한 set
        image_urls = set()

        #찾을 div
        product_blocks = soup.find_all('div', class_='css-7ny53m')

        # 이미지 다운로드 횟수 제한
        max_images = 1000
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
            

        # CSV 파일로 상품 정보 저장
        csv_path = os.path.join(path, f'queenit_crawl_{category}.csv')
        with open(csv_path, 'w', newline='', encoding='cp949') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating', 'ImageURL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)

        # 크롤링 후 이미지 다운로드
        download_images(csv_path, path, session)

if __name__ == '__main__':
    url = 'https://web.queenit.kr/'
    path_input = 'c:/queenit/'    
     # 'top'과 'under'에 대한 크롤링을 순차적으로 실행
    QueenitCrawling.queenit_crawling(url, path_input, 'top')
    QueenitCrawling.queenit_crawling(url, path_input, 'onepiece')
    QueenitCrawling.queenit_crawling(url, path_input, 'pants')    
    QueenitCrawling.queenit_crawling(url, path_input, 'outer')
    QueenitCrawling.queenit_crawling(url, path_input, 'skirt')
    