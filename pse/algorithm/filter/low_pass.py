""" Bibliotecas externas. """
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

    maskDims = [int(dim) for dim in mask.split('x')]
    weight = 1 / (maskDims[0] * maskDims[1])
    weights = [[weight for j in range(maskDims[1])] for i in range(maskDims[0])]
    return filters.convolve(image, weights)


def medianFilter(image, mask):
    """ Aplica o filtro de mediana em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.

    @param image deve ser uma matriz (numpy)
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro.
    """
    (row, col) = [int(dim) for dim in mask.split('x')]
    return filters.median_filter(image, (row, col))


def gaussianFilter(image, sigma):
    """ Aplica o filtro gaussiano em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser uma matriz (numpy)
    @param sigma parâmetro do filtro gaussiano

    @return matriz com novos valores após aplicação do filtro.
    """

    return filters.gaussian_filter(image, sigma)
