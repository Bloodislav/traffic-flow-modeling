import pygame

def blit_rotate_center(win, image, top_left, angle):
    """Отрисовка изображения на экране с учетом поворота."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text) -> None:
    """Отрисовка текста по центру"""
    render = font.render(text, 1, (0, 0, 0))
    win.blit(
        render,
        (
            win.get_width() / 2 - render.get_width() / 2,
            win.get_height() / 2 - render.get_height() / 2,
        ),
    )

