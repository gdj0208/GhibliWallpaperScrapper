
import os
from Fronts.QClickableLabel import QClickableLabel
from Fronts.MovieSelectorLayout import MovieSelectorLayout
from Backs.DownloadMovieList import DownloadMovieList
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QWidget, QSizePolicy
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt
from data.movie_data import MOVIE_DATA, IMG_DIR


class ShowlistLayout(QHBoxLayout) :
    # movie_idx_changed = pyqtSignal(int)

    def __init__(self, 
                 parent=None,
                 movie_selector_layout : MovieSelectorLayout = None,
                 dwn_movie_list : DownloadMovieList = None
                 ) :
        super().__init__(parent)
        self.movie_selector_layout = movie_selector_layout
        self.dwn_movie_list = dwn_movie_list
        self._initUI()

    def _initUI(self):
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
        self.addWidget(scroll_area)

    def refresh_poster(self):
        """영화 리스트 내용을 업데이트 합니다"""
        # Clear existing posters
        while self.poster_layout.count():
            item = self.poster_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new posters
        for movie_idx in self.dwn_movie_list.movie_list:
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
        self.dwn_movie_list.current_movie_index = movie_idx
        self.movie_selector_layout.show_current_image()