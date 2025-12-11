import cv2
import matplotlib.pyplot as plt
import numpy as np

def display_images(orig_img: np.ndarray, gray_img: np.ndarray):
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
        plt.imshow(orig_rgb, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Полутоновое изображение")
    plt.imshow(gray_img, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
