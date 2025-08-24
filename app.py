
import sys
import os
import json
from Scrapper import Scrapper
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QLabel
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from unwrapper import unwrap_json


URLS = unwrap_json('movie_urls.json') 
MOVIE_LIST = unwrap_json('movie_data.json')

class Wallpaper_Downloader(QWidget):
    def __init__(self):
        self.SCRAPPER = Scrapper() 
        super().__init__()

        self.image_dir = 'src'
        self.data_file = 'movie_data.json'
        self.movie_list = []
        
        self._load_movie_data()
        self.initUI()

        self.current_image_index = 0
        self._show_current_image()

    def _load_movie_data(self):
        """이미지 경로와 영화 제목 데이터를 불러옵니다."""
        # 이미지 파일 목록을 정렬하여 순서를 정합니다.
        self.images = sorted(list(MOVIE_LIST.keys()))
        if not self.images:
            QMessageBox.warning(self, "경고", "이미지 파일이 없습니다.")


    def initUI(self):
        self.setWindowTitle('지브리 월페이퍼 스크래퍼')
        self.setGeometry(100, 100, 400, 640)

        main_layout = QVBoxLayout()

        # 제목 라벨
        self._make_title_label()
        main_layout.addWidget(self.title_label)

        # 이미지와 좌우 버튼을 담을 레이아웃
        main_layout.addLayout(self._get_movie_selector_layout())
        self.setLayout(main_layout)

    def _make_title_label(self):
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold)) # 폰트 크기 및 굵기 설정

    def _make_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button
    
    def _get_movie_selector_layout(self) :
        movie_selector_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton('이전')
        self.next_btn = QPushButton('다음')
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 이미지 클릭 이벤트 연결
        self.image_label.mousePressEvent = self.on_image_clicked
        
        movie_selector_layout.addWidget(self.prev_btn)
        movie_selector_layout.addWidget(self.image_label)
        movie_selector_layout.addWidget(self.next_btn)


        self.prev_btn.clicked.connect(self._show_prev_image)
        self.next_btn.clicked.connect(self._show_next_image)
        
        return movie_selector_layout

    def _show_current_image(self):
        """현재 인덱스에 해당하는 이미지를 표시합니다."""
        if not self.images:
            self.image_label.setText("이미지 없음")
            self.title_label.setText("작품 없음")
            return
        
        image_name = self.images[self.current_image_index]
        image_path = os.path.join(self.image_dir, image_name)
        movie_title = MOVIE_LIST.get(image_name, "알 수 없는 작품")
        # 영화 제목 라벨 업데이트
        self.title_label.setText(movie_title)
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText(f"이미지를 찾을 수 없습니다.{image_name}")

    def _show_prev_image(self):
        """이전 이미지를 표시합니다."""
        if not self.images: return
        self.current_image_index = (self.current_image_index - 1 + len(self.images)) % len(self.images)
        self._show_current_image()

    def _show_next_image(self):
        """다음 이미지를 표시합니다."""
        if not self.images: return
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self._show_current_image()

    def on_image_clicked(self, event):
        """이미지 클릭 시 영화 제목을 저장 리스트에 추가합니다."""
        if not self.images: return
        
        current_image_name = self.images[self.current_image_index]
        movie_title = MOVIE_LIST.get(current_image_name, "알 수 없는 영화")
        print(f"'{movie_title}'을(를) 클릭했습니다.")

        '''
        if movie_title not in self.movie_list:
            self.movie_list.append(movie_title)
            print(f"'{movie_title}'을(를) 저장할 리스트에 추가했습니다.")
            print("현재 리스트:", self.movie_list)
        else:
            print(f"'{movie_title}'은(는) 이미 리스트에 있습니다.")
        '''
    
    def scrap_all(self):
        self.SCRAPPER.scrap_all_page()
        QMessageBox.information(self, "완료", "모든 지브리 월페이퍼가 스크랩되었습니다!")

        # 스크래핑 완료 후 폴더 열기
        os.startfile(self.SCRAPPER.save_folder)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Wallpaper_Downloader()
    downloader.show()
    sys.exit(app.exec())
    