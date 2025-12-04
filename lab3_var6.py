import cv2
import matplotlib.pyplot as plt
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Преобразование изображения в полутоновое.")
    parser.add_argument('--input', type=str, required=True, help="Путь к исходному изображению.")
    parser.add_argument('--output', type=str, required=True, help="Путь для сохранения изображения.")
    return parser.parse_args()


def load_image(input_path: Path):
    """Загружает изображение с помощью OpenCV. Возвращает массив и исходный путь."""
    if not input_path.is_file():
        raise FileNotFoundError(f"Исходный файл не найден: {input_path}")
    
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {input_path}")
    
    return img


def print_image_size(img):
    """Выводит размер изображения в консоль."""
    if img.ndim == 3:
        h, w, c = img.shape
    else:
        h, w = img.shape
        c = 1
    print(f"Размер изображения: {h} x {w} (каналов: {c})")
    return h, w, c


def convert_to_grayscale(img):
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


def display_images(orig_img, gray_img):
    """Отображает исходное и полутоновое изображения с помощью matplotlib."""
    # Конвертация BGR → RGB для корректного отображения в matplotlib
    if orig_img.ndim == 3:
        orig_rgb = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    else:
        orig_rgb = orig_img

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Исходное изображение")
    if orig_rgb.ndim == 3:
        plt.imshow(orig_rgb)
    else:
        plt.imshow(orig_rgb, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Полутоновое изображение")
    plt.imshow(gray_img, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    img = load_image(input_path)

    print_image_size(img)
    
    gray_img = convert_to_grayscale(img)
    
    print_image_size(gray_img)
    
    save_image(gray_img, output_path)
    
    display_images(img, gray_img)


if __name__ == "__main__":
    main()