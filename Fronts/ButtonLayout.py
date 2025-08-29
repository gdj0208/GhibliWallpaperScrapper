
from Fronts.Maker import make_button
from Fronts.QClickableLabel import QClickableLabel
from Fronts.ShowlistLayout import ShowlistLayout
from Backs.DownloadMovieList import DownloadMovieList
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QSizePolicy, QMessageBox
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from data.movie_data import MOVIE_DATA, IMG_DIR

class ButtonLayout(QVBoxLayout) :
    def __init__(self, 
                 parent=None, 
                 dwn_movie_list : DownloadMovieList = None,
                 showlist_layout : ShowlistLayout = None
                 ):
        super().__init__(parent)
        self.download_movie_list = dwn_movie_list
        self.showlist_layout = showlist_layout
        self._initUI()
    
    def _initUI(self):
        add_remove_layout = QHBoxLayout()

        remove_button = make_button("삭제", self.remove_movie_in_list)
        add_button = make_button("추가", self.add_movie_in_list)
        download_button = make_button("다운로드", self.scrap_all)

        add_remove_layout.addWidget(remove_button)
        add_remove_layout.addWidget(add_button)

        self.addLayout(add_remove_layout)
        self.addWidget(download_button)

    def add_movie_in_list(self, event):
        """저장 리스트에서 영화를 추가합니다."""
        if not MOVIE_DATA: 
            return
        
        movie_title = MOVIE_DATA[self.download_movie_list.current_movie_index]['title']
        
        if self.download_movie_list.current_movie_index not in self.download_movie_list.movie_list:
            self.download_movie_list.movie_list.append(self.download_movie_list.current_movie_index)
            print(f"'{movie_title}'을(를) 저장할 리스트에 추가했습니다.")
            print("현재 리스트:", self.download_movie_list.movie_list)
            self.showlist_layout.refresh_poster()
        else:
            print(f"'{movie_title}'은(는) 이미 리스트에 있습니다.")
        
    def remove_movie_in_list(self, event):
        """저장 리스트에서 영화를 제거합니다."""
        if not MOVIE_DATA:
            return
        
        movie_title = MOVIE_DATA[self.download_movie_list.current_movie_index]['title']

        if self.download_movie_list.current_movie_index in self.download_movie_list.movie_list:
            self.download_movie_list.movie_list.remove(self.download_movie_list.current_movie_index)
            print(f"'{movie_title}'을(를) 리스트에서 삭제했습니다.")
            print("현재 리스트:", self.download_movie_list.movie_list)
            self.showlist_layout.refresh_poster()
        else :
            print(f"'{movie_title}'은(는) 이미 리스트에 없습니다.")

    def scrap_all(self):
        title_list = []
        for idx in self.download_movie_list.movie_list :
            title_list.append({MOVIE_DATA[idx]['title'], MOVIE_DATA[idx]['url']})
            

        self.SCRAPPER.scrap_all_page(title_list)
        QMessageBox.information(self, "완료", "모든 지브리 월페이퍼가 스크랩되었습니다!")
