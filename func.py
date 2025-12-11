import argparse
from pathlib import Path

import cv2
import numpy as np

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Преобразование изображения в полутоновое."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Путь к исходному изображению."
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Путь для сохранения изображения."
    )
    return parser.parse_args()

def load_image(input_path: Path):
    """Загружает изображение с помощью OpenCV. Возвращает массив и исходный путь."""
    if not input_path.is_file():
        raise FileNotFoundError(f"Исходный файл не найден: {input_path}")

    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {input_path}")

    return img


def print_image_size(img: np.ndarray):
    """Выводит размер изображения в консоль."""
    if img.ndim == 3:
        h, w, c = img.shape
    else:
        h, w = img.shape
        c = 1
    print(f"Размер изображения: {h} x {w} (каналов: {c})")
    return h, w, c


def convert_to_grayscale(img: np.ndarray):
    """Преобразует изображение в полутоновое."""
    if img.ndim == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img  # уже есть полутоновое
    return gray


def save_image(img, output_path: Path):
    """Сохраняет изображение в указанный файл."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    new_img = cv2.imwrite(str(output_path), img)
    if not new_img:
        raise RuntimeError(f"Не удалось сохранить изображение: {output_path}")
    print(f"Изображение сохранено: {output_path}")