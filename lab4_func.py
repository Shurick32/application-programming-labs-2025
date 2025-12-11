import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from pathlib import Path

def load_dataframe(annotation_path: str) -> pd.DataFrame:
    """Загружает аннотацию и проверяет наличие файлов."""
    if not os.path.exists(annotation_path):
        raise FileNotFoundError(f"Файл аннотации не найден: {annotation_path}")

    df = pd.read_csv(annotation_path)

    required = {"absolute_path", "relative_path"}
    if not required.issubset(df.columns):
        raise ValueError(f"В CSV должны быть колонки: {required}")

    df["exists"] = df["absolute_path"].apply(lambda p: Path(p).exists())
    missing = df[~df["exists"]]
    if not missing.empty:
        print(f"⚠️  Внимание: {len(missing)} файлов не найдено. Они будут пропущены.")
        df = df[df["exists"]].copy()
        df.drop(columns=["exists"], inplace=True)

    return df.reset_index(drop=True)


def compute_rgb_means(image_path: str):
    """Вычисляет средние значения R, G, B для изображения."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            arr = np.array(img)
            r_mean = arr[:, :, 0].mean()
            g_mean = arr[:, :, 1].mean()
            b_mean = arr[:, :, 2].mean()
            return r_mean, g_mean, b_mean
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return np.nan, np.nan, np.nan


def add_brightness_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет колонки: mean_R, mean_G, mean_B."""
    rgb_means = df["absolute_path"].apply(lambda p: pd.Series(compute_rgb_means(p)))
    rgb_means.columns = ["mean_R", "mean_G", "mean_B"]
    df = pd.concat([df, rgb_means], axis=1)

    df = df.dropna(subset=["mean_R", "mean_G", "mean_B"]).reset_index(drop=True)
    return df


def sort_by_brightness(df: pd.DataFrame, channel: str = "mean_R") -> pd.DataFrame:
    """Сортирует DataFrame по указанному каналу (по умолчанию R)."""
    if channel not in df.columns:
        raise ValueError(
            f"Колонка {channel} не найдена. Доступны: mean_R, mean_G, mean_B"
        )
    return df.sort_values(by=channel).reset_index(drop=True)


def filter_by_brightness(
    df: pd.DataFrame, channel: str, min_val: float = 0, max_val: float = 255
) -> pd.DataFrame:
    """Фильтрует по диапазону значений канала."""
    return df[(df[channel] >= min_val) & (df[channel] <= max_val)].reset_index(
        drop=True
    )


def plot_brightness_curves(df: pd.DataFrame, save_path: str):
    """Строит график: X — номер изображения, Y — средние значения R, G, B."""
    plt.figure(figsize=(12, 6))
    x = np.arange(len(df))

    plt.plot(x, df["mean_R"], label="Канал R (Red)", color="red")
    plt.plot(x, df["mean_G"], label="Канал G (Green)", color="green")
    plt.plot(x, df["mean_B"], label="Канал B (Blue)", color="blue")

    plt.title("Средняя яркость по каналам RGB для изображений черепах")
    plt.xlabel("Номер изображения (после сортировки по среднему R)")
    plt.ylabel("Среднее значение интенсивности (0–255)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"График: {save_path}")
