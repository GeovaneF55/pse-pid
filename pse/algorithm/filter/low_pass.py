""" Bibliotecas externas. """
from enum import Enum
from PyQt5.QtGui import (QColor)

Filter = Enum('Filter', 'BOX MEDIAN')
FilterLabel = {
    Filter.BOX: 'Filtro de Média',
    Filter.MEDIAN: 'Filtro de Mediana',
}

def applyFilter(image, maskSize, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.BOX: boxFilter,
        Filter.MEDIAN: medianFilter,
    }

    return filters[filterKey](image, maskSize)


def boxFilter(image, maskDim):
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
            red = 0
            green = 0
            blue = 0
            
            for maskRow in mask:
                for (sr, sc) in maskRow:
                    # Tratamento de borda circular
                    x = (i + sr) % height
                    y = (j + sc) % width

                    pixelColor = image.pixelColor(x, y)

                    red += pixelColor.red()
                    green += pixelColor.green()
                    blue += pixelColor.blue()

            newColor = {'red': round(red / (maskDim ** 2)),
                        'green': round(green / (maskDim ** 2)),
                        'blue': round(blue / (maskDim ** 2))}

            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage


def medianFilter(image, maskDim):
    """ Aplica o filtro de mediana em uma imagem,
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

    # Posição da mediana
    medianPos = (maskDim ** 2) // 2
    
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

            newColor = {'red': round(sorted(red)[medianPos]),
                        'green': round(sorted(green)[medianPos]),
                        'blue': round(sorted(blue)[medianPos])}
            
            newColor = QColor(newColor['red'], newColor['green'], newColor['blue'])
            newImage.setPixelColor(i, j, newColor)

    return newImage
