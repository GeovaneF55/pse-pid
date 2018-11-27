""" Bibliotecas externas. """
from enum import Enum
from scipy.ndimage import filters

Filter = Enum('Filter', 'GAUSSIAN_LAPLACE LAPLACE PREWITT SOBEL')
FilterLabel = {

    Filter.GAUSSIAN_LAPLACE: 'Filtro Gaussiano-Laplaciano',
    Filter.LAPLACE: 'Filtro de Laplace',
    Filter.PREWITT: 'Filtro Prewitt',
    Filter.SOBEL: 'Filtro de Sobel',
}

Border = Enum('Border', 'REFLECT NEAREST WRAP')
BorderLabel = {
    Border.REFLECT: 'Refletir',
    Border.NEAREST: 'Mais próximo',
    Border.WRAP: 'Circular'
}
BorderMap = {
    BorderLabel[Border.REFLECT]: 'reflect',
    BorderLabel[Border.NEAREST]: 'nearest',
    BorderLabel[Border.WRAP]: 'wrap'
}

def applyFilter(image, param, filterKey):
    """ Aplica o filtro de acordo com a chave
    passada por parâmetro.
    """
    
    filters = {
        Filter.GAUSSIAN_LAPLACE: gaussianLaplaceFilter,
        Filter.LAPLACE: laplaceFilter,
        Filter.PREWITT: prewittFilter,
        Filter.SOBEL: sobelFilter,
    }

    return filters[filterKey](image, param)


def gaussianLaplaceFilter(image, sigma):
    """ Aplica o filtro gaussiano laplaciano em uma imagem,
    de acordo com o tamanho da máscara passada por
    parâmetro.
    
    @param image deve ser uma matriz (numpy)
    @param sigma parâmetro do filtro gaussiano laplaciano

    @return matriz com novos valores após aplicação do filtro.
    """
    
    return filters.gaussian_laplace(image, float(sigma))


def laplaceFilter(image, border):
    """ Aplica o filtro de laplace em uma imagem.

    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """
    
    border = BorderMap[border]

    return filters.laplace(image, mode=border)


def prewittFilter(image, border):
    """ Aplica o filtro prewitt em uma imagem.
    
    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """

    border = BorderMap[border]

    return filters.prewitt(image, mode=border)


def sobelFilter(image, border):
    """ Aplica o filtro sobel em uma imagem.
    
    @param image deve ser uma matriz (numpy)

    @return matriz com novos valores após aplicação do filtro.
    """
    
    border = BorderMap[border]

    return filters.sobel(image, mode=border)
