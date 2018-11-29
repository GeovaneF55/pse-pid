""" Bibliotecas externas. """
from enum import Enum
import numpy
from scipy import ndimage
from skimage import color

Filter = Enum('Filter', 'CLOSING DILATION EROSION OPENING')
FilterLabel = {
    Filter.CLOSING: 'Fechamento',
    Filter.DILATION: 'Dilatação',
    Filter.EROSION: 'Erosão',
    Filter.OPENING: 'Abertura',
}

def applyFilter(image, maskSize, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.CLOSING: closingFilter,
        Filter.DILATION: dilationFilter,
        Filter.EROSION: erosionFilter,
        Filter.OPENING: openingFilter,
    }

    image = color.rgb2gray(image) * 255
    return filters[filterKey](image, maskSize)


def dilationFilter(image, mask):
    """ Aplica o filtro de dilatação em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro
    """

    threshold = 0.8
    sumColors = numpy.float(numpy.sum(image))
    isbinary = sumColors / image.size <= 1 - threshold

    
    (row, col) = [int(dim) for dim in mask.split('x')]
    structure = [[1 for i in range(col)] for j in range(row)]

    if isbinary:
        return ndimage.binary_dilation(image, structure=structure)
    else:
        return ndimage.grey_dilation(image, structure=structure)
    

    
def erosionFilter(image, mask):
    """ Aplica o filtro de erosão em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro
    """

    threshold = 0.8
    sumColors = numpy.float(numpy.sum(image))
    isbinary = sumColors / image.size <= 1 - threshold

    
    (row, col) = [int(dim) for dim in mask.split('x')]
    structure = [[1 for i in range(col)] for j in range(row)]

    if isbinary:
        return ndimage.binary_erosion(image, structure=structure)
    else:
        return ndimage.grey_erosion(image, structure=structure)


def openingFilter(image, mask):
    """ Aplica o filtro de fechamento em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro
    """

    threshold = 0.8
    sumColors = numpy.float(numpy.sum(image))
    isbinary = sumColors / image.size <= 1 - threshold

    
    (row, col) = [int(dim) for dim in mask.split('x')]
    structure = [[1 for i in range(col)] for j in range(row)]

    if isbinary:
        return ndimage.binary_closing(image, structure=structure)
    else:
        return ndimage.grey_closing(image, structure=structure)


def closingFilter(image, mask):
    """ Aplica o filtro de abertura em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser um PIL.Image.
    @param mask string "row x cols"

    @return matriz com novos valores após aplicação do filtro
    """

    threshold = 0.8
    sumColors = numpy.float(numpy.sum(image))
    isbinary = sumColors / image.size <= 1 - threshold

    
    (row, col) = [int(dim) for dim in mask.split('x')]
    structure = [[1 for i in range(col)] for j in range(row)]

    if isbinary:
        return ndimage.binary_opening(image, structure=structure)
    else:
        return ndimage.grey_opening(image, structure=structure)
