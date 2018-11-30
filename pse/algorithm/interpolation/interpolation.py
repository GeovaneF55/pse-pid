from scipy import ndimage

def nearest_neighbor(image, scale, order):
    """ Aplica a nterpolação por vizinho mais próximo.
    
    @param image numpy array.
    @param dim tupla contendo as dimensões originais.
    @param scale valor escalar para redimensionamento.
    
    @return numpy array.
    """

    return ndimage.zoom(image, (scale, scale, 1), order=order)
