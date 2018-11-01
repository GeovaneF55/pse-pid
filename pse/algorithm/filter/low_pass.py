""" Bibliotecas externas. """
from enum import Enum
from PIL import (ImageFilter,
                 ImageQt)
from PyQt5.QtGui import (QColor)

Filter = Enum('Filter', 'BOX MEDIAN MODE GAUSSIAN')
FilterLabel = {
    Filter.BOX: 'Filtro de Média',
    Filter.MEDIAN: 'Filtro de Mediana',
    Filter.MODE: 'Filtro de Moda',
    Filter.GAUSSIAN: 'Filtro Gaussiano',
}

def applyFilter(image, maskSize, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.BOX: boxFilter,
        Filter.MEDIAN: medianFilter,
        Filter.MODE: modeFilter,
        Filter.GAUSSIAN: gaussianFilter,
    }

    return filters[filterKey](image, maskSize)


def boxFilter(image, maskDim):
    """ Aplica o filtro de média (box) em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param maskDim inteiro representando as dimensões da máscara.
    """

    radius = (maskDim - 1) // 2
    return image.filter(ImageFilter.BoxBlur(radius))


def medianFilter(image, maskDim):
    """ Aplica o filtro de mediana em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.

    @param image deve ser um PIL.Image
    @param maskDim inteiro representando as dimensões da máscara.
    """

    return image.filter(ImageFilter.MedianFilter(maskDim))


def modeFilter(image, maskDim):
    """ Aplica o filtro de moda em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.

    @param image deve ser um PIL.Image
    @param maskDim inteiro representando as dimensões da máscara.
    """

    return image.filter(ImageFilter.ModeFilter(maskDim))


def gaussianFilter(image, maskDim):
    """ Aplica o filtro gaussiano em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.

    @param image deve ser um PIL.Image
    @param maskDim inteiro representando as dimensões da máscara.
    """

    radius = (maskDim - 1) // 2
    return image.filter(ImageFilter.GaussianBlur(radius))
