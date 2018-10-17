from PyQt5.QtGui import (QPixmap)

def nearest_neighbour(image, scale):

    width = image.width()
    height = image.height()

    pixmap = QPixmap( width * scale, height * scale)

    for i in range(height):
        for j in range(width):
            pass

    # Cria uma cópia da imagem original
    newImage = image.copy()

    return newImage