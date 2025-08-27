from bs4 import BeautifulSoup
import requests, json, os
from unwrapper import unwrap_json


URLS = unwrap_json('movie_urls.json') 
MOVIE_LIST = unwrap_json('movie_data.json')

class Scrapper:
    def __init__(self):
        self.urls = {}
        self._set_save_folder()
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']  # 이미지 확장자 목록

    def _set_save_folder(self):
        self.save_folder = 'images'
        os.makedirs(self.save_folder, exist_ok=True)

    def add_url(self, title):
        if title not in URLS:
            print(f"❌ 오류: '{title}'는 지원하지 않는 제목입니다.")
            return

        self.urls[title] = URLS[title]
        # 영화 제목을 기준으로 폴더 생성
        # os.makedirs(os.path.join(self.save_folder, title), exist_ok=True)
        # print(f"✅ '{title}' URL이 추가되었고, 폴더가 생성되었습니다.")


    # 웹사이트에서 이미지 스크랩
    def scrap_all_image(self, title, url):

        os.makedirs(os.path.join(self.save_folder, title), exist_ok=True)
        print(f"✅ '{title}' URL이 추가되었고, 폴더가 생성되었습니다.")

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        #print(soup.prettify())
        
        for i, a_tag in enumerate(soup.find_all('a', href=True)):
            href = a_tag['href']
            # 확장자로 이미지 링크인지 판별
            if any(href.lower().endswith(ext) for ext in self.image_extensions):
                # 상대경로일 경우 절대경로로 변환
                img_url = requests.compat.urljoin(url, href)

                
                try:
                    img_data = requests.get(img_url).content
                    file_ext = os.path.splitext(img_url)[1]
                    img_name = img_url.replace('https://www.ghibli.jp/gallery/', '') .replace('.jpg', '')
                    file_name = os.path.join(self.save_folder+"/"+title, f'{img_name}{file_ext}')
                    
                    
                    with open(file_name, 'wb') as f:
                        f.write(img_data)
                    print(f'✅ 저장 완료: {file_name}')
                except Exception as e:
                    print(f'❌ 오류: {img_url} - {e}')
            
    # 모든 웹사이트에서 이미지 스크랩
    def scrap_all_page(self, movie_list):
        cnt = 0

        print("웹사이트에서 이미지 스크랩을 시작합니다.")
        print(f'스크랩 완료 후 {self.save_folder} 폴더를 확인하세요.')
        print("지브리 월페이퍼들을 다운로드 받는 중입니다...")

        if movie_list is not None :
            self.urls = movie_list
            for title, url in movie_list:
                self.scrap_all_image(title, url)
                cnt += 1
                print(f'{cnt}/{len(self.urls)}번째 스크랩 완료: {title}')
        else :
            for title, url in self.urls.items():
                print(title, url)
                self.scrap_all_image(title, url)
                cnt += 1
                print(f'{cnt}/{len(self.urls)}번째 스크랩 완료: {title}')

        print("스크랩 완료!")


    
if __name__ == "__main__":

    ghibli_scrapper = Scrapper()

    for url, title in MOVIE_LIST.items():
        ghibli_scrapper.add_url(title)

    ghibli_scrapper.scrap_all_page()