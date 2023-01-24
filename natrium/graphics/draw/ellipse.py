import pygame
from natrium import common
from natrium.typehinting import *
from pygame import gfxdraw
from natrium.graphics import color as colorfile

def render_ellipse(r1:int, r2:int, color:IsColor, antialias:bool = True):
    color = pygame.Color(color)
    main_surf = pygame.Surface([r1*2+1, r2*2+1], pygame.SRCALPHA, 32)

    if antialias:
        gfxdraw.aaellipse(main_surf, r1, r2, r1, r2, color)
        gfxdraw.aaellipse(main_surf, r1, r2, r1, r2, color)
    gfxdraw.filled_ellipse(main_surf, r1, r2, r1, r2, color)

    return main_surf

def render_ellipsegrad2(r1:int, r2:int, c1:IsColor, c2:IsColor, antialias:bool = True,
                        orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    main_surf = render_ellipse(r1, r2, [255, 255, 255, 255], antialias)
    grad_surf = colorfile.Color2(c1, c2).gradient([r1*2+2, r2*2+2], orient, gradient_blend)

    main_surf.blit(grad_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return main_surf

def render_ellipsegrad3(r1:int, r2:int, c1:IsColor, c2:IsColor, c3:IsColor, antialias:bool = True,
                        orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    main_surf = render_ellipse(r1, r2, [255, 255, 255, 255], antialias)
    grad_surf = colorfile.Color3(c1, c2, c3).gradient([r1*2+2, r2*2+2], orient, gradient_blend)

    main_surf.blit(grad_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return main_surf

def instant_ellipse(surface:pygame.Surface, center:IsPosition, r1:int, r2:int, color:IsColor, antialias:bool = True):
    main_surf = render_ellipse(r1, r2, color, antialias)
    surface.blit(main_surf, [x-y for x, y in zip(center, [r1, r2])])

def instant_ellipsegrad2(surface:pygame.Surface, center:IsPosition, r1:int, r2:int, c1:IsColor, c2:IsColor,
                         antialias:bool = True, orient="horizontal", gradient_blend:int = 10):

    main_surf = render_ellipsegrad2(r1, r2, c1, c2, antialias, orient, gradient_blend)
    surface.blit(main_surf, [x-y for x, y in zip(center, [r1, r2])])

def instant_ellipsegrad3(surface:pygame.Surface, center:IsPosition, r1:int, r2:int, c1:IsColor, c2:IsColor, c3:IsColor,
                         antialias:bool = True, orient="horizontal", gradient_blend:int = 10):

    main_surf = render_ellipsegrad3(r1, r2, c1, c2, c3, antialias, orient, gradient_blend)
    surface.blit(main_surf, [x-y for x, y in zip(center, [r1, r2])])

def dynamic_render_ellipse(r1:int, r2:int, colors:clcs.Sequence[IsColor], antialias:bool = True,
                           orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    if isinstance(colors[0], int) or common.is_str(colors) or isinstance(colors, pygame.Color):

        return render_ellipse(r1, r2, colors, antialias)

    elif isinstance(colors[0], (list, tuple, pygame.Color, str)) and len(colors) == 2:
        return render_ellipsegrad2(r1, r2, *colors, antialias, orient, gradient_blend)

    elif isinstance(colors[0], (list, tuple, pygame.Color, str)) and len(colors) == 3:
        return render_ellipsegrad3(r1, r2, *colors, antialias, orient, gradient_blend)

    else:
        raise ValueError("Colors argument must be a Sequence[IsColor] with a length of 2-3 or a single color.")


def instant_dynamic_render_ellipse(surface:pygame.Surface, center:IsPosition, r1:int, r2:int, colors:clcs.Sequence[IsColor],
                                   antialias:bool = True, orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    main_surf = dynamic_render_ellipse(r1, r2, colors, antialias, orient, gradient_blend)
    surface.blit(main_surf, [x-y for x, y in zip(center, [r1, r2])])

