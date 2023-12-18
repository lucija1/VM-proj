from keras.models import load_model
from VM_proj_flask.cnn_model.MNIST_CNN_util import *
from numpy import argmax
from PIL import Image


class MNIST_CNN_model:
    def __init__(self, model_path: str) -> None:
        self.model = load_model(model_path)
        print("\nMODEL CREATED!\n")

    def predict(self, img_path: str = None, img_file: str = None, image: Image = None):
        if img_path is not None:
            start_img, formatted_img = load_image_from_path(img_path)
        elif img_file is not None:
            start_img, formatted_img = load_image_from_file(img_path)
        elif image is not None:
            formatted_img = image
        else:
            return "error"
        predict_value = self.model.predict(formatted_img, verbose=0)
        digit = argmax(predict_value)
        return digit


if __name__ == "__main__":
    MNIST_CNN_model = MNIST_CNN_model("cnn_model/final_model.h5")
    result = MNIST_CNN_model.predict("img/sample_image.png")

    print(result)
