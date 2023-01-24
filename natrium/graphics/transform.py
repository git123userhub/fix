from PIL import Image, ImageOps, ImageFilter
from natrium.typehinting import *
import pygame

def surface_to_image(surface:pygame.Surface):
    bytes_surf = pygame.image.tostring(surface, 'RGBA')
    img = Image.frombuffer('RGBA', surface.get_size(), bytes_surf)

    return img

def expand_image(image:Image.Image, offset:int, fill:IsColor):
    new_image = ImageOps.expand(image, offset, fill)
    return new_image

def gaussian_blur_image(image:Image.Image, radius:int, allow_expansion:bool = False):
    new_image = expand_image(image, round(radius * 2), (0, 0, 0, 0)) if allow_expansion else image
    image_blur = new_image.filter(ImageFilter.GaussianBlur(radius))
    return image_blur

def image_to_surface(image:Image.Image):
    bytes_image = image.tobytes()
    new_surf = pygame.image.frombuffer(bytes_image, image.size, 'RGBA')
    return new_surf

def expand_surface(surface:pygame.Surface, offset:int, fill:IsColor):
    img = surface_to_image(surface)
    expand_img = expand_image(img, offset, fill)
    expand_surf = image_to_surface(expand_img)
    return expand_surf

def gaussian_blur_surface(surface, radius, allow_expansion=False):
    img = surface_to_image(surface)
    gaussian_img = gaussian_blur_image(img, radius, allow_expansion)
    gaussian_surf = image_to_surface(gaussian_img)
    return gaussian_surf
