""" Bibliotecas externas. """
from enum import Enum
from skimage.color.adapt_rgb import (adapt_rgb,
                                     each_channel)
from skimage import filters

Filter = Enum('Filter', 'GAUSSIAN_LAPLACE LAPLACE PREWITT SOBEL ROBERTS')
FilterLabel = {
    Filter.GAUSSIAN_LAPLACE: 'Laplaciano do Gaussiano',
    Filter.LAPLACE: 'Laplace',
    Filter.PREWITT: 'Prewitt',
    Filter.SOBEL: 'Sobel',
    Filter.ROBERTS: 'Roberts'
}

@adapt_rgb(each_channel)
def sobel_rgb(image):
    """ Aplica o filtro Sobel, utilizando o decorador
    @adapt_rgb para que o filtro seja aplicado em todos
    os canais RGB da imagem.

    @param image numpy.ndarray.

    @return result numpy.ndarray.
    """

    return filters.sobel(image)


@adapt_rgb(each_channel)
def gaussian_rgb(image, sigma):
    """ Aplica o filtro Gaussiano, utilizando o decorador
    @adapt_rgb para que o filtro seja aplicado em todos
    os canais RGB da imagem.

    @param image numpy.ndarray.
    @param sigma

    @return result numpy.ndarray.
    """

    return filters.gaussian(image, sigma)


@adapt_rgb(each_channel)
def laplace_rgb(image):
    """ Aplica o filtro Laplaciano, utilizando o decorador
    @adapt_rgb para que o filtro seja aplicado em todos
    os canais RGB da imagem.

    @param image numpy.ndarray.

    @return result numpy.ndarray.
    """

    return filters.laplace(image)

@adapt_rgb(each_channel)
def prewitt_rgb(image):
    """ Aplica o filtro Prewitt, utilizando o decorador
    @adapt_rgb para que o filtro seja aplicado em todos
    os canais RGB da imagem.

    @param image numpy.ndarray.

    @return result numpy.ndarray.
    """

    return filters.prewitt(image)


@adapt_rgb(each_channel)
def roberts_rgb(image):
    """ Aplica o filtro Roberts, utilizando o decorador
    @adapt_rgb para que o filtro seja aplicado em todos
    os canais RGB da imagem.

    @param image numpy.ndarray.

    @return result numpy.ndarray.
    """

    return filters.roberts(image)


def applyFilter(image, param, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.GAUSSIAN_LAPLACE: gaussianLaplaceFilter,
        Filter.LAPLACE: laplaceFilter,
        Filter.PREWITT: prewittFilter,
        Filter.SOBEL: sobelFilter,
        Filter.ROBERTS: robertsFilter
    }

    if filterKey == Filter.GAUSSIAN_LAPLACE:
        return filters[filterKey](image, param)
    else:
        return filters[filterKey](image)


def gaussianLaplaceFilter(image, sigma):
    """ Aplica o filtro gaussiano laplaciano em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser uma matriz (numpy)
    @param sigma parâmetro do filtro gaussiano laplaciano

    @return matriz com novos valores após aplicação do filtro.
    """

    gaussian = gaussian_rgb(image.copy(), float(sigma))
    return laplace_rgb(gaussian) * 255


def laplaceFilter(image):
    """ Aplica o filtro de laplace em uma imagem.

    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """
    
    return laplace_rgb(image) * 255


def prewittFilter(image):
    """ Aplica o filtro prewitt em uma imagem.
    
    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """

    return prewitt_rgb(image) * 255


def sobelFilter(image):
    """ Aplica o filtro sobel em uma imagem.
    
    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """
    

    return sobel_rgb(image) * 255

def robertsFilter(image):
    """ Aplica o filtro de Roberts em uma imagem.
    
    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """
    

    return roberts_rgb(image) * 255
