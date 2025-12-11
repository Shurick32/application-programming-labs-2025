from show import display_images
from func import (
    parse_args,
    load_image,
    print_image_size,
    convert_to_grayscale,
    save_image,
    
)
from pathlib import Path

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
