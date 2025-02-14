from io import BytesIO
from PIL.Image import Image


def drawer(content)
    im = BytesIO(content)
    opened_image = Image.open(im)
    opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы