from io import BytesIO

from keras.preprocessing.image import img_to_array, load_img
from PIL import Image


# load and prepare the image
def load_image_from_path(filename):
    start_img = load_img(filename)

    formatted_image = load_img(filename, color_mode="grayscale", target_size=(28, 28))
    return start_img, format_image_for_model(formatted_image)


def load_image_from_file(file):
    start_img = Image.open(BytesIO(file.read()))

    file.seek(0)
    
    formatted_image = load_img(
        BytesIO(file.read()), color_mode="grayscale", target_size=(28, 28)
    )
    return start_img, format_image_for_model(formatted_image)


def format_image_for_model(start_img: Image):
    # convert to array
    formatted_img = img_to_array(start_img)
    # reshape into a single sample with 1 channel
    formatted_img = formatted_img.reshape(1, 28, 28, 1)
    # prepare pixel data
    formatted_img = formatted_img.astype("float32")
    formatted_img = formatted_img / 255.0

    return formatted_img
