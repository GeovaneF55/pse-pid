from PyQt5.QtGui import (QPixmap)

def nearest_neighbour(image, scale):

    pixmap = QPixmap(image.width() * scale, image.height() * scale)

    for i in range(height):
        for j in range(width):
            pass

    # Cria uma cópia da imagem original
    newImage = image.copy()

    return newImage