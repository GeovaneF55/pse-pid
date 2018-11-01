""" Bibliotecas externas. """
from enum import Enum
from PIL import ImageFilter
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
    
    @param image deve ser um PIL.Image.
    @param maskDim inteiro representando as dimensões da máscara.
    """
    
    return image.filter(ImageFilter.MaxFilter(maskDim))


def minFilter(image, maskDim):
    """ Aplica o filtro de mínimo em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param maskDim inteiro representando as dimensões da máscara.
    """

    return image.filter(ImageFilter.MinFilter(maskDim))
