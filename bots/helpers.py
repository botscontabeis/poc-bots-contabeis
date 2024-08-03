import base64
import os
from io import BytesIO

from PIL import Image


def convert_base64_to_jpg_and_save_file(base64_string, output_file_path):
    if base64_string.startswith("data:image/jpg;base64,"):
        base64_string = base64_string.replace("data:image/jpg;base64,", "")

    image_data = base64.b64decode(base64_string)
    Image.open(BytesIO(image_data)).save(output_file_path, "JPEG")

    return output_file_path


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
