
import sys
import os
import json
from Backs.Scrapper import Scrapper
from Backs.unwrapper import unwrap_json
from Fronts.QClickableLabel import QClickableLabel
from Fronts.Maker import make_button, make_title_label
from Fronts.Movie_Selector_Layout import Movie_Selector_Layout
from data.movie_data import MOVIE_DATA, IMG_DIR, DATA_FILE

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt, QSize, pyqtSignal


class Wallpaper_Downloader(QWidget):
    def __init__(self):
        self.SCRAPPER = Scrapper() 
        super().__init__()

        IMG_DIR = 'src'
        #DATA_FILE = 'movie_data.json'
        self.movie_list = []
        self.current_movie_index = 0
        
        # self._load_movie_data()
        if not MOVIE_DATA:
            QMessageBox.warning(self, "경고", "이미지 파일이 없습니다.")
        self.initUI()

        # self._show_current_image()   

    def update_current_index(self, new_idx):
        self.current_movie_index = new_idx

    def initUI(self):
        self.setWindowTitle('지브리 월페이퍼 스크래퍼')
        self.setGeometry(100, 100, 400, 640)

        main_layout = QVBoxLayout()

        # 영화 선택창 레이아웃
        self.movie_selector_layout = Movie_Selector_Layout(current_movie_idx=self.current_movie_index)
        self.movie_selector_layout.movie_idx_changed.connect(self.update_current_index)
        self.movie_selector_layout.show_current_image()

        main_layout.addLayout(self.movie_selector_layout)
        main_layout.addLayout(self._get_showlist_layout())
        main_layout.addLayout(self._get_button_layout())
        self.setLayout(main_layout)

    def _get_button_layout(self):
        """버튼 레이아웃을 가져옵니다"""
        this_layout = QVBoxLayout()

        add_remove_layout = QHBoxLayout()

        remove_button = make_button("삭제", self.remove_movie_in_list)
        add_button = make_button("추가", self.add_movie_in_list)
        download_button = make_button("다운로드", self.scrap_all)

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

            movie_dir = MOVIE_DATA[movie_idx]['image']
            image_path = os.path.join(IMG_DIR, movie_dir)
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
        self.movie_selector_layout.current_movie_idx = self.current_movie_index = movie_idx
        self.movie_selector_layout.show_current_image()
        # print(f"선택된 포스터의 movie_idx: {movie_idx}")

    def add_movie_in_list(self, event):
        """저장 리스트에서 영화를 추가합니다."""
        if not MOVIE_DATA: 
            return
        
        current_image_name = MOVIE_DATA[self.current_movie_index]['image']
        movie_title = MOVIE_DATA[self.current_movie_index]['title']
        
        if self.current_movie_index not in self.movie_list:
            self.movie_list.append(self.current_movie_index)
            print(f"'{movie_title}'을(를) 저장할 리스트에 추가했습니다.")
            print("현재 리스트:", self.movie_list)
            self.refresh_poster()
        else:
            print(f"'{movie_title}'은(는) 이미 리스트에 있습니다.")
        
    def remove_movie_in_list(self, event):
        """저장 리스트에서 영화를 제거합니다."""
        if not MOVIE_DATA:
            return
        
        current_image_name = MOVIE_DATA[self.current_movie_index]['image']
        movie_title = MOVIE_DATA[self.current_movie_index]['title']

        if self.current_movie_index in self.movie_list:
            self.movie_list.remove(self.current_movie_index)
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
            title_list.append({MOVIE_DATA[idx]['title'], MOVIE_DATA[idx]['url']})
            

        self.SCRAPPER.scrap_all_page(title_list)
        QMessageBox.information(self, "완료", "모든 지브리 월페이퍼가 스크랩되었습니다!")

        # 스크래핑 완료 후 폴더 열기
        # os.startfile(self.SCRAPPER.save_folder)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Wallpaper_Downloader()
    downloader.show()
    sys.exit(app.exec())
    