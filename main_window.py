import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
    QWidget, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from lab2 import ImageIterator

class ImageViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("lab5")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        self.btn_load_folder = QPushButton("Выбрать папку")
        self.btn_load_csv = QPushButton("Выбрать аннотацию (CSV)")
        self.btn_next = QPushButton("Следующее изображение")
        self.btn_next.setEnabled(False)

        button_layout.addWidget(self.btn_load_folder)
        button_layout.addWidget(self.btn_load_csv)
        button_layout.addWidget(self.btn_next)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; }")

        layout.addLayout(button_layout)
        layout.addWidget(self.image_label)
        central_widget.setLayout(layout)

        self.btn_load_folder.clicked.connect(self.load_from_folder)
        self.btn_load_csv.clicked.connect(self.load_from_csv)
        self.btn_next.clicked.connect(self.show_next_image)

        self.iterator = None
        self.current_path = None

    def load_from_folder(self):
        """Выбор папки с изображениями."""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с датасетом")
        if folder:
            self.init_iterator(folder)

    def load_from_csv(self):
        """Выбор CSV-файла аннотации."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.init_iterator(file_path)

    def init_iterator(self, source):
        """Инициализация итератора и первой загрузки."""
        try:
            self.iterator = iter(ImageIterator(source))
            self.btn_next.setEnabled(True)
            self.show_next_image()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{str(e)}")
            self.btn_next.setEnabled(False)
            self.iterator = None

    def show_next_image(self):
        """Получает следующий путь и отображает изображение."""
        if self.iterator is None:
            return

        try:
            self.current_path = next(self.iterator)
            self.display_image(self.current_path)
        except StopIteration:
            QMessageBox.information(self, "Конец", "Больше изображений нет.")
            self.btn_next.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

    def display_image(self, image_path: str):
        """Отображает изображение с сохранением пропорций."""
        if not os.path.exists(image_path):
            self.image_label.setText("Файл не найден")
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Невозможно загрузить изображение")
            return

        label_size = self.image_label.size()
        scaled_pixmap = pixmap.scaled(
            label_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec_())