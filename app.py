
import sys
import os
import json
from Scrapper import Scrapper
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from unwrapper import unwrap_json


URLS = unwrap_json('movie_urls.json') 
MOVIE_LIST = unwrap_json('movie_data.json')

class QClickableLabel(QLabel):
    # 클릭 시그널 정의
    clicked = pyqtSignal()
    
    def __init__(self, parent=None, movie_idx=-1):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.idx = movie_idx

    def mousePressEvent(self, event):
        self.clicked.emit()

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
        # self.images = sorted(list(MOVIE_LIST.keys()))
        self.images = list(MOVIE_LIST.keys())
        self.urls = list(URLS.items())
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
        main_layout.addLayout(self._get_showlist_layout())
        main_layout.addLayout(self._get_button_layout())
        self.setLayout(main_layout)

    def _get_button_layout(self):
        """버튼 레이아웃을 가져옵니다"""
        this_layout = QVBoxLayout()

        add_remove_layout = QHBoxLayout()

        remove_button = self._make_button("삭제", self.remove_movie_in_list)
        add_button = self._make_button("추가", self.add_movie_in_list)
        download_button = self._make_button("다운로드", self.scrap_all)

        add_remove_layout.addWidget(remove_button)
        add_remove_layout.addWidget(add_button)

        this_layout.addLayout(add_remove_layout)
        this_layout.addWidget(download_button)

        return this_layout

    def _get_showlist_layout(self):
        """다운받을 영화들의 목록을 보여주는 레이아웃을 가져옵니다"""
        this_layout = QHBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(140)
        scroll_area.setStyleSheet(
            """QWidget {
                border : 2px solid black;
            }"""
        )
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.poster_layout = QHBoxLayout(scroll_content_widget)
        self.poster_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(scroll_content_widget)

        #showlist_layout.add(button_layout)
        this_layout.addWidget(scroll_area)

        return this_layout

    def _make_title_label(self):
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold)) # 폰트 크기 및 굵기 설정

    def _make_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button
    
    def _get_movie_selector_layout(self) :
        """영화 선택 레이아웃을 가져옵니다"""
        movie_selector_layout = QHBoxLayout()
        
        prev_btn = self._make_button("이전", self._show_prev_image)
        next_btn = self._make_button("다음", self._show_next_image)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 이미지 클릭 이벤트 연결
        # self.image_label.mousePressEvent = self.on_image_clicked
        
        movie_selector_layout.addWidget(prev_btn)
        movie_selector_layout.addWidget(self.image_label)
        movie_selector_layout.addWidget(next_btn)
        
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
            self.image_label.setPixmap(pixmap.scaledToWidth(320, Qt.TransformationMode.SmoothTransformation))
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

    def refresh_poster(self):
        """영화 리스트 내용을 업데이트 합니다"""
        # Clear existing posters
        while self.poster_layout.count():
            item = self.poster_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new posters
        for movie_idx in self.movie_list:
            #poster_label = QLabel()
            poster_label = QClickableLabel(movie_idx=movie_idx)
            poster_label.setToolTip("No Image") # Show movie title on hover
            
            # Create a custom property to store the movie title
            poster_label.setProperty("movie_title", movie_idx)
            poster_label.clicked.connect(self.select_poster)

            movie_dir = self.images[movie_idx]
            image_path = os.path.join(self.image_dir, movie_dir)
            # print(image_path)

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(75, 100, 
                                              Qt.AspectRatioMode.KeepAspectRatio, 
                                              Qt.TransformationMode.SmoothTransformation)
                poster_label.setPixmap(scaled_pixmap)
            else:
                poster_label.setText("No Poster")
                
            poster_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            #poster_label.mousePressEvent = self.select_poster
            
            self.poster_layout.addWidget(poster_label)

    def select_poster(self):
        """클릭시 해당 영화를 선택합니다"""
        clicked_label = self.sender()
        if not clicked_label:
            return

        movie_idx = clicked_label.idx
        self.current_image_index = movie_idx
        self._show_current_image()
        # print(f"선택된 포스터의 movie_idx: {movie_idx}")

    def add_movie_in_list(self, event):
        """저장 리스트에서 영화를 추가합니다."""
        if not self.images: return
        
        current_image_name = self.images[self.current_image_index]
        movie_title = MOVIE_LIST.get(current_image_name, "알 수 없는 영화")
        
        if self.current_image_index not in self.movie_list:
            self.movie_list.append(self.current_image_index)
            print(f"'{movie_title}'을(를) 저장할 리스트에 추가했습니다.")
            print("현재 리스트:", self.movie_list)
            self.refresh_poster()
        else:
            print(f"'{movie_title}'은(는) 이미 리스트에 있습니다.")
        
    def remove_movie_in_list(self, event):
        """저장 리스트에서 영화를 제거합니다."""
        if not self.movie_list:
            return
        
        current_movie = self.images[self.current_image_index]
        movie_title = MOVIE_LIST.get(current_movie, "알 수 없는 영화")

        if self.current_image_index in self.movie_list:
            self.movie_list.remove(self.current_image_index)
            print(f"'{movie_title}'을(를) 리스트에서 삭제했습니다.")
            print("현재 리스트:", self.movie_list)
            self.refresh_poster()
        else :
            print(f"'{movie_title}'은(는) 이미 리스트에 없습니다.")
    
    def set_movie_list(self, movie_list_data):
        """1. Load images from the movie_list data."""
        self.movie_list = movie_list_data
        self.refresh_posters()

    def scrap_all(self):
        title_list = []
        for idx in self.movie_list :
            # title = self.images[idx]
            # url = self.urls[idx]
            title_list.append(self.urls[idx])
            

        self.SCRAPPER.scrap_all_page(title_list)
        QMessageBox.information(self, "완료", "모든 지브리 월페이퍼가 스크랩되었습니다!")

        # 스크래핑 완료 후 폴더 열기
        # os.startfile(self.SCRAPPER.save_folder)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Wallpaper_Downloader()
    downloader.show()
    sys.exit(app.exec())
    