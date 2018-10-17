""" Bibliotecas externas. """
from enum import Enum
import numpy
from PyQt5.QtGui import (QColor)

Filter = Enum('Filter', 'MIN MAX')
FilterLabel = {
    Filter.MAX: 'Filtro de Máximo',
    Filter.MIN: 'Filtro de Mínimo',
}

def applyFilter(image, maskSize, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.MAX: maxFilter,
        Filter.MIN: minFilter,
    }

    return filters[filterKey](image, maskSize)


def maxFilter(image, maskDim):
    """ Aplica o filtro de mínimo em uma imagem,
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
            
            for maskRow in mask:
                for (sr, sc) in maskRow:
                    # Tratamento de borda circular
                    x = (i + sr) % height
                    y = (j + sc) % width

                    pixelColor = image.pixelColor(x, y)

                    red.append(pixelColor.red())
                    green.append(pixelColor.green())
                    blue.append(pixelColor.blue())

            newColor = {'red': round(max(red)),
                        'green': round(max(green)),
                        'blue': round(max(blue))}

            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage


def minFilter(image, maskDim):
    """ Aplica o filtro de mínimo em uma imagem,
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
            
            for maskRow in mask:
                for (sr, sc) in maskRow:
                    # Tratamento de borda circular
                    x = (i + sr) % height
                    y = (j + sc) % width

                    pixelColor = image.pixelColor(x, y)

                    red.append(pixelColor.red())
                    green.append(pixelColor.green())
                    blue.append(pixelColor.blue())

            newColor = {'red': round(min(red)),
                        'green': round(min(green)),
                        'blue': round(min(blue))}

            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage
