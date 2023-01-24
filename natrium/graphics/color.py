import pygame
from pygame import gfxdraw
from natrium.typehinting import *
from natrium.graphics import transform

class Color2:
    def __init__(self, color1:IsColor, color2:IsColor):
        self.color1 = pygame.Color(color1)
        self.color2 = pygame.Color(color2)

    def gradient(self, size: IsSizeSequence, orient:IsOrientLiteral = "horizontal", blend:int = 10):
        if orient == "horizontal":
            gradient_surf = pygame.Surface((2, 1), pygame.SRCALPHA, 32)
            gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
            gfxdraw.pixel(gradient_surf, 1, 0, self.color2)

        elif orient == "vertical":
            gradient_surf = pygame.Surface((1, 2), pygame.SRCALPHA, 32)
            gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
            gfxdraw.pixel(gradient_surf, 0, 1, self.color2)

        else:
            return None

        gradient_surf = pygame.transform.scale(gradient_surf, size)
        gradient_surf = transform.gaussian_blur_surface(gradient_surf, blend)
        return gradient_surf

class Color3:
    def __init__(self, color1:IsColor, color2:IsColor, color3:IsColor):
        self.color1 = pygame.Color(color1)
        self.color2 = pygame.Color(color2)
        self.color3 = pygame.Color(color3)

    def gradient(self, size:IsSizeSequence, orient:IsOrientLiteral = "horizontal", blend:int = 10):
        if orient == "horizontal":
            gradient_surf = pygame.Surface((3, 1), pygame.SRCALPHA, 32)
            gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
            gfxdraw.pixel(gradient_surf, 1, 0, self.color2)
            gfxdraw.pixel(gradient_surf, 2, 0, self.color3)

        elif orient == "vertical":
            gradient_surf = pygame.Surface((1, 3), pygame.SRCALPHA, 32)
            gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
            gfxdraw.pixel(gradient_surf, 0, 1, self.color2)
            gfxdraw.pixel(gradient_surf, 0, 2, self.color3)

        else:
            return None

        gradient_surf = pygame.transform.scale(gradient_surf, size)
        gradient_surf = transform.gaussian_blur_surface(gradient_surf, blend)
        return gradient_surf

def color_to_rgb(color:IsColor):
    return color.r, color.g, color.b

def color_to_rgba(color:IsColor):
    return *color_to_rgb(color), color.a

def hsv_to_rgb(h, s, v):
    color = pygame.Color((0, 0, 0, 255))
    color.hsva = (h, s, v, 100)
    return color_to_rgb(color)

def hsva_to_rgba(h, s, v, a):
    color = pygame.Color((0, 0, 0, 0))
    color.hsva = (h, s, v, a)
    return color_to_rgba(color)
