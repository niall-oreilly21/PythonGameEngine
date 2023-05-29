import pygame
from pygame import Vector2
from Engine.GameObjects.Components.Physics.ButtonCollider2D import ButtonCollider2D

class ButtonColliderHover2D(ButtonCollider2D):
    def __init__(self, name, event_handler, camera_manager, scale_factor, anchor=pygame.Vector2(0, 0)):
        super().__init__(name, event_handler, camera_manager, anchor)
        self.__old_scale = None
        self.__x_original_position = None
        self.__y_original_position = None
        self.__new_scale = None
        self.event_handler = event_handler
        self.camera_manager = camera_manager
        self.__scale_factor = scale_factor

    def start(self):
        super().start()
        self.__x_original_position = self.transform.position.x
        self.__y_original_position = self.transform.position.y

        self.__old_scale = self.transform.scale.copy()
        self.__new_scale = self.transform.scale + Vector2(self.__scale_factor, self.__scale_factor)

    def mouse_hover(self):
        if self.bounds.collidepoint(self._mouse_position):
            old_bounds = self.bounds
            self.transform.scale = self.__new_scale
            new_bounds = self.bounds
            translation_offset = Vector2(*old_bounds.center) - Vector2(*new_bounds.center)
            self.transform.translate_by(translation_offset)
        else:
            self.transform.scale = self.__old_scale
            self.transform.position = Vector2(self.__x_original_position, self.__y_original_position)

    def update(self, game_time):
        super().update(game_time)
        self.mouse_hover()

    def draw(self, screen, camera_manager):
        super().draw(screen, camera_manager)
