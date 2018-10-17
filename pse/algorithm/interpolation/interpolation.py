import numpy as np

def nearest_neighbour(image):

    channels_count = 4

    s = image.bits().asstring(image.width() * image.height() * channels_count)
    arr = np.fromstring(s, dtype=np.uint8).reshape((image.height(), image.width(), channels_count))

    # Cria uma cópia da imagem original
    newImage = image.copy()

    return newImage