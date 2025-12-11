from lab4_func import (
    load_dataframe,
    add_brightness_columns,
    sort_by_brightness,
    filter_by_brightness,
    plot_brightness_curves    
)

import argparse

def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ изображений: вычисление средней яркости по каналам RGB и визуализация."
    )
    parser.add_argument(
        '--input_csv',
        type=str,
        default='annotation.csv',
        help='Путь к входному CSV-файлу с колонками absolute_path и relative_path (по умолчанию: annotation.csv)'
    )
    parser.add_argument(
        '--output_csv',
        type=str,
        default='anno_mid_rgb.csv',
        help='Путь для сохранения итогового CSV с данными (по умолчанию: anno_mid_rgb.csv)'
    )
    parser.add_argument(
        '--output_plot',
        type=str,
        default='mid_rgb.png',
        help='Путь для сохранения графика (по умолчанию: mid_rgb.png)'
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    df = load_dataframe(args.input_csv)
    print(f"Загружено {len(df)} изображений.")

    df = add_brightness_columns(df)
    
    df_sorted = sort_by_brightness(df, channel='mean_R')
    
    df_sorted = filter_by_brightness(df_sorted, 'mean_R', min_val=100)

    plot_brightness_curves(df_sorted, args.output_plot)

    df_sorted.to_csv(args.output_csv, index=False)
    print(f"DataFrame сохранён: {args.output_csv}")

    print("\nПервые 5 строк итогового DataFrame:")
    print(df_sorted.head())


if __name__ == "__main__":
    main()