from PIL import Image

def nearest_neighbor(image, dim, scale):
    (width, height) = dim
    width = round(width * scale)
    height = round(height * scale)

    return image.resize((width, height), Image.NEAREST)
