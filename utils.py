import pygame


def sprite_at(position, sprite_list):
    point = pygame.sprite.Sprite()
    point.image = pygame.Surface([1, 1])
    point.rect = point.image.get_rect()
    point.rect.x = position[0]
    point.rect.y = position[1]
    return pygame.sprite.spritecollideany(point, sprite_list)