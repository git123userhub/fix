import pygame
from natrium.graphics.draw import ellipse
from natrium.graphics import color, transform
from natrium.typehinting import *
from natrium import common

def render_round_rect(rect:pygame.Rect, color:IsColor, radius:int = 0, antialias:bool = True, gaussian:int = 0):
    main_surf = pygame.Surface([x+2 for x in rect.size], pygame.SRCALPHA, 32)

    if isinstance(radius, int):
        radius = [radius]*4

    elif isinstance(radius, (list, tuple)):
        if len(radius) == 2:
            radius *= 2
        elif len(radius) != 4:
            raise ValueError("Radius must be an integer or a list of 2 or 4 integers.")

    max_radius = max(*radius)

    deflated_rt = rect.inflate(-(max_radius * 2 + 1), -(max_radius * 2 + 1))
    deflated_rt.topleft = (max_radius, max_radius)

    rt_coords = [deflated_rt.topleft, deflated_rt.topright,
                 deflated_rt.bottomright, deflated_rt.bottomleft]
    rt_coords2 = []

    for i, (x, y) in enumerate(rt_coords):
        diff_rad = max_radius - radius[i]
        if i == 0: new_pos = [x-diff_rad, y-diff_rad]
        elif i == 1: new_pos = [x+diff_rad, y-diff_rad]
        elif i == 2: new_pos = [x-diff_rad, y+diff_rad]
        elif i == 3: new_pos = [x+diff_rad, y+diff_rad]
        rt_coords2.insert(i, new_pos)

    if antialias:
        for i, pos in enumerate(rt_coords2):
            if i == 0:
                pos[0] += 1; pos[1] += 1
            elif i == 1:
                pos[1] += 1
            elif i == 3:
                pos[0] += 1

            ellipse.instant_ellipse(main_surf, pos, radius[i], radius[i], color)

    for i, (x, y) in enumerate([[rt_coords[0], rt_coords[1]], [rt_coords[1], rt_coords[2]],
                             [rt_coords[2], rt_coords[3]], [rt_coords[3], rt_coords[0]]]):

        diff_rad = max_radius - radius[i]
        diff_rad1 = max_radius - radius[(i+1)%4]
        length_offsetx, length_offsety, height_offsetx, height_offsety = (diff_rad, diff_rad1)*2

        if i % 2 == 0:
            height_offsetx, height_offsety = 0, 0
            if i == 0:
                x2 = [x[0]-length_offsetx+1, x[1]-height_offsetx]
                y2 = [y[0]+length_offsety, y[1]-height_offsety]

            else:
                x2 = [x[0]+length_offsetx, x[1]-height_offsetx]
                y2 = [y[0]+length_offsety, y[1]-height_offsety]

        else:
            length_offsetx, length_offsety = 0, 0
            if i == 1:
                x2 = [x[0]+length_offsetx, x[1]+height_offsetx]
                y2 = [y[0]-length_offsety, y[1]-height_offsety]

            else:
                x2 = [x[0]+length_offsetx, x[1]+height_offsetx]
                y2 = [y[0]-length_offsety, y[1]+height_offsety]

        pygame.draw.line(main_surf, color, x2, y2, max_radius*2)

    pygame.draw.rect(main_surf, color, deflated_rt)

    main_surf = transform.gaussian_blur_surface(main_surf, gaussian)
    return main_surf


def render_round_rect_grad2(rect:pygame.Rect, c1:IsColor, c2:IsColor, radius:int = 0, antialias:bool = True,
                            gaussian:int = 0, orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    main_surf = pygame.Surface([x+2 for x in rect.size], pygame.SRCALPHA, 32)
    grad_surf = color.Color2(c1, c2).gradient([x+4+gaussian*4 for x in rect.size], orient, gradient_blend)

    main_surf.blit(render_round_rect(pygame.Rect(0, 0, *rect.size), 'white', radius, antialias, gaussian), (0, 0))

    main_surf.blit(grad_surf, [0, 0], special_flags=pygame.BLEND_RGBA_MIN)
    return main_surf

def render_round_rect_grad3(rect:pygame.Rect, c1:IsColor, c2:IsColor, c3:IsColor, radius:int = 0, antialias:bool = True,
                            gaussian:int = 0, orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

        main_surf = pygame.Surface([x + 2 for x in rect.size], pygame.SRCALPHA, 32)
        grad_surf = color.Color3(c1, c2, c3).gradient([x+2+gaussian*4 for x in rect.size], orient, gradient_blend)

        main_surf.blit(render_round_rect(pygame.Rect(0, 0, *rect.size), 'white', radius, antialias, gaussian), (0, 0))

        main_surf.blit(grad_surf, [0, 0], special_flags=pygame.BLEND_RGBA_MIN)
        return main_surf

def render_dynamic_rect(rect:pygame.Rect, colors:clcs.Sequence[IsColor], radius:int, antialias:bool = True,
                        gaussian=0, orient:IsOrientLiteral = "horizontal", gradient_blend:int = 10):

    if isinstance(colors[0], int) or common.is_str(colors) or isinstance(colors, pygame.Color):
        return render_round_rect(rect, colors, radius, antialias, gaussian)

    elif isinstance(colors[0], (list, tuple, pygame.Color, str)) and len(colors) == 2:
        return render_round_rect_grad2(rect, *colors, radius, antialias, gaussian, orient, gradient_blend)

    elif isinstance(colors[0], (list, tuple, pygame.Color, str)) and len(colors) == 3:
        return render_round_rect_grad3(rect, *colors, radius, antialias, gaussian, orient, gradient_blend)

    else:
        raise ValueError("Colors argument must be a Sequence[IsColor] with a length of 2-3 or a single color.")

def instant_round_rect(surface:pygame.Surface, rect:pygame.Rect, color:IsColor, radius:int = 0, antialias:bool = True,
                       gaussian:int = 0):
    surf = render_round_rect(rect, color, radius, antialias, gaussian)
    surface.blit(surf, rect.topleft)

def instant_round_rect_grad2(surface:pygame.Surface, rect:pygame.Rect, c1:IsColor, c2:IsColor, radius:int = 0,
                             antialias:bool = True, gaussian:int = 0):
    surf = render_round_rect_grad2(rect, c1, c2, radius, antialias, gaussian)
    surface.blit(surf, rect.topleft)

def instant_round_rect_grad3(surface:pygame.Surface, rect:pygame.Rect, c1:IsColor, c2:IsColor, c3:IsColor, radius:int = 0,
                             antialias:bool = True, gaussian:int = 0):
    surf = render_round_rect_grad3(rect, c1, c2, c3, radius, antialias, gaussian)
    surface.blit(surf, rect.topleft)

def instant_dynamic_rect(surface:pygame.Surface, rect:pygame.Rect, colors:clcs.Sequence[IsColor], radius:int = 0,
                         antialias:bool = True, gaussian:int = 0):
    surf = render_dynamic_rect(rect, colors, radius, antialias, gaussian)
    surface.blit(surf, rect.topleft)