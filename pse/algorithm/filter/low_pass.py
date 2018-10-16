""" Bibliotecas externas. """
import numpy
from enum import Enum
from PyQt5.QtGui import (QColor)
import scipy.stats

LowPassFilter = Enum('LowPassFilter', 'BOX MEDIAN MODE NEG MIN MAX')

def applyFilter(image, maskSize, filterKey):
    filters = {
        LowPassFilter.BOX: box,
        LowPassFilter.MEDIAN: median,
    }

    return filters[filterKey](image, maskSize)


def box(image, maskDim):
    """ Aplica o filtro de média (box) em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um QImage.
    @param maskDim inteiro representando as dimensões da máscara.
    """
    
    # Máscara a ser usada no filtro
    center = maskDim // 2
    mask = [[(i - center, j - center) for j in range(maskDim)]
           for i in range(maskDim)]
    
    # Cria uma cópia da imagem original
    newImage = image.copy()

    # Dimensões da imagem
    height = newImage.height()
    width = newImage.width()

    for i in range(height):
        for j in range(width):
            red = []
            green = []
            blue = []
            
            for (index, maskRow) in enumerate(mask):
                for (sr, sc) in maskRow:
                    # Tratamento de borda circular
                    x = (i + sr) % height
                    y = (j + sc) % width

                    pixelColor = image.pixelColor(x, y)

                    red.append(pixelColor.red())
                    green.append(pixelColor.green())
                    blue.append(pixelColor.blue())

            newColor = {'red': round(numpy.mean(red)),
                        'green': round(numpy.mean(green)),
                        'blue': round(numpy.mean(blue))}

            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage

def median(image, maskDim):
    """ Aplica o filtro de mediana em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um QImage.
    @param maskDim inteiro representando as dimensões da máscara.
    """
    
    # Máscara a ser usada no filtro
    center = maskDim // 2
    mask = [[(i - center, j - center, 1) for j in range(maskDim)]
           for i in range(maskDim)]
    
    # Cria uma cópia da imagem original
    newImage = image.copy()

    # Dimensões da imagem
    height = newImage.height()
    width = newImage.width()

    for i in range(height):
        for j in range(width):
            newColor = {'red': 0, 'green': 0, 'blue': 0}
            
            for row in mask:
                for (sr, sc, weight) in row:
                    # Tratamento de borda circular
                    x = (i + sr) % height
                    y = (j + sc) % width

                    pixelColor = image.pixelColor(x, y)

                    newColor['red'] += pixelColor.red() * weight
                    newColor['green'] += pixelColor.green() * weight
                    newColor['blue'] +=  pixelColor.blue() * weight

            newColor = {key: round(value / (maskDim * maskDim)) \
                        for key, value in newColor.items()}

            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage
