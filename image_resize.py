from PIL import Image
import argparse
import os


class ResizeParametersException(Exception):
    pass


def create_parser():
    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('input', help='Path to original image')
    parser.add_argument('-width', help='Width of resulting image', type=int)
    parser.add_argument('-height', help='Height of resulting image', type=int)
    parser.add_argument('-scale', help='Resizing scale', type=float)
    parser.add_argument('-output', help='Path to resulting image')
    args = parser.parse_args()
    return args


def get_result_size(width, height, scale, original_width, original_height):
    reshaped = False

    if scale and (width or height):
        raise ResizeParametersException('Only scale or size can be specified')

    if width and not height:
        result_width = width
        result_height = original_height * result_width / original_width

    if not width and height:
        result_height = height
        result_width = original_width * result_height / original_height

    if width and height:
        result_height = height
        result_width = width
        reshaped = True

    if scale:
        result_width = original_width * scale
        result_height = original_height * scale

    return round(result_width), round(result_height), reshaped


def get_path_to_result(path_to_original, path_requested, width, height):
    if path_requested:
        return path_requested

    root_original, ext = os.path.splitext(path_to_original)
    root_result = '{}__{}x{}'.format(root_original, width, height)
    path_to_result = ''.join((root_result, ext))
    return path_to_result


def resize_image(path_to_original, path_to_result, width, height):
    image = Image.open(path_to_original)
    resized_image = image.resize((width, height))
    resized_image.save(path_to_result)


def check_original(path_to_original):
    if not os.path.exists(path_to_original):
        print('File does not exist')
        return False

    if not os.path.isfile(path_to_original):
        print('Not a file')
        return False

    if not os.path.splitext(path_to_original)[1] in ['.jpg', '.png']:
        print('Filetype of original is not supported')
        return False
    return True


def main():
    parser = create_parser()

    path_to_original = parser.input

    original_found = check_original(path_to_original)
    if not original_found:
        return None

    if parser.output and not os.path.splitext(
            parser.output)[1] in ['.jpg', '.png']:
        print('Filetype of result is not supported')
        return None

    image = Image.open(path_to_original)

    original_width = image.width
    original_height = image.height

    width = parser.width
    height = parser.height
    scale = parser.scale
    if not (scale or width or height):
        print('Size or scale must be specified')
        return None

    result_width, result_height, reshaped = get_result_size(
        width, height, scale, original_width, original_height)

    if reshaped:
        print('Proportions of the image will be changed')

    path_to_result = get_path_to_result(path_to_original, parser.output,
                                        result_width, result_height)

    resize_image(path_to_original, path_to_result, result_width, result_height)
    print('Image successfully resized')


if __name__ == '__main__':
    main()
