""" Bibliotecas externas. """
import numpy
from enum import Enum
from scipy.ndimage import filters

Filter = Enum('Filter', 'BOX MEDIAN MODE GAUSSIAN')
FilterLabel = {
    Filter.BOX: 'Filtro de Média',
    Filter.MEDIAN: 'Filtro de Mediana',
    Filter.GAUSSIAN: 'Filtro Gaussiano',
}

def applyFilter(image, maskSize, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.BOX: boxFilter,
        Filter.MEDIAN: medianFilter,
        Filter.GAUSSIAN: gaussianFilter,
    }

    return filters[filterKey](image, maskSize)


def boxFilter(image, mask):
    """ Aplica o filtro de média (box) em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser uma matriz (numpy)
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro.
    """

    maskDims = list(map(int, mask.split('x')))
    return filters.uniform_filter(image, (maskDims[0], maskDims[1], 1))


def medianFilter(image, mask):
    """ Aplica o filtro de mediana em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.

    @param image deve ser uma matriz (numpy)
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro.
    """
    maskDims = list(map(int, mask.split('x')))
    return filters.median_filter(image, (maskDims[0], maskDims[1], 1))


def gaussianFilter(image, sigma):
    """ Aplica o filtro gaussiano em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser uma matriz (numpy)
    @param sigma parâmetro do filtro gaussiano

    @return matriz com novos valores após aplicação do filtro.
    """

    return filters.gaussian_filter(image, (sigma, sigma, 0))
