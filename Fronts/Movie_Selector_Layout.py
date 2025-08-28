
import os
from Fronts.Maker import make_button, make_title_label
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from data.movie_data import MOVIE_DATA, IMG_DIR

class Movie_Selector_Layout(QVBoxLayout) :
    movie_idx_changed = pyqtSignal(int)

    def __init__(self, parent=None, current_movie_idx = 0):
        super().__init__(parent)
        self.current_movie_idx = current_movie_idx
        self.init_UI()

    def init_UI(self):

        self.title_label = make_title_label()
        self.selector_layout = QHBoxLayout()
        self.prev_btn = make_button("이전", self._show_prev_image)
        self.next_btn = make_button("다음", self._show_next_image)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 이미지 클릭 이벤트 연결
        # self.image_label.mousePressEvent = self.on_image_clicked
        
        self.addWidget(self.title_label)
        self.selector_layout.addWidget(self.prev_btn)
        self.selector_layout.addWidget(self.image_label)
        self.selector_layout.addWidget(self.next_btn)
        self.addLayout(self.selector_layout)

        #self._show_current_image()

    def _show_prev_image(self):
        """이전 이미지를 표시합니다."""
        if not MOVIE_DATA: 
            return
        
        self.current_movie_idx = (self.current_movie_idx - 1 + len(MOVIE_DATA)) % len(MOVIE_DATA)
        self.show_current_image()

    def _show_next_image(self):
        """다음 이미지를 표시합니다."""
        if not MOVIE_DATA: 
            return
        
        self.current_movie_idx = (self.current_movie_idx + 1) % len(MOVIE_DATA)
        self.show_current_image()

    def show_current_image(self):
        """현재 인덱스에 해당하는 이미지를 표시합니다."""
        if not MOVIE_DATA:
            self.image_label.setText("이미지 없음")
            self.title_label.setText("작품 없음")
            return
        
        # 부모 클래스에 변수값이 바뀜을 알림
        self.movie_idx_changed.emit(self.current_movie_idx)

        image_name = MOVIE_DATA[self.current_movie_idx]['image']
        image_path = os.path.join(IMG_DIR, image_name)
        movie_title = MOVIE_DATA[self.current_movie_idx]['title']

        # 영화 제목 라벨 업데이트
        self.title_label.setText(movie_title)
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaledToWidth(320, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText(f"이미지를 찾을 수 없습니다.{image_name}")
