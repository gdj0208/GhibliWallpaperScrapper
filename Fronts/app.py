
import sys
import os
import json
from Backs.Scrapper import Scrapper
from Backs.unwrapper import unwrap_json
from Backs.DownloadMovieList import DownloadMovieList
from Fronts.QClickableLabel import QClickableLabel
from Fronts.Maker import make_button
from Fronts.MovieSelectorLayout import MovieSelectorLayout
from Fronts.ShowlistLayout import ShowlistLayout
from Fronts.ButtonLayout import ButtonLayout
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
        self.download_movie_list = DownloadMovieList()
        # self.movie_list = []
        # self.current_movie_index = 0
        
        # self._load_movie_data()
        if not MOVIE_DATA:
            QMessageBox.warning(self, "경고", "이미지 파일이 없습니다.")
        self.initUI()

        # self._show_current_image()   

    def update_current_index(self, new_idx):
        self.download_movie_list.current_movie_index = new_idx

    def initUI(self):
        self.setWindowTitle('지브리 월페이퍼 스크래퍼')
        self.setGeometry(100, 100, 400, 640)

        main_layout = QVBoxLayout()

        self.movie_selector_layout = MovieSelectorLayout(dwn_movie_list=self.download_movie_list)
        self.showlist_layout = ShowlistLayout(movie_selector_layout=self.movie_selector_layout, dwn_movie_list = self.download_movie_list)
        self.button_layout = ButtonLayout(dwn_movie_list=self.download_movie_list, showlist_layout=self.showlist_layout)

        main_layout.addLayout(self.movie_selector_layout)
        main_layout.addLayout(self.showlist_layout)
        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = Wallpaper_Downloader()
    downloader.show()
    sys.exit(app.exec())
    