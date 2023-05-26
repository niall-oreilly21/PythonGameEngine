from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.InputHandler import InputHandler
from Engine.Other.Interfaces.MovementInterface import MovementInterface
import pygame

from Engine.Other.Transform2D import Direction


class PlayerController(Component, MovementInterface):

    def __init__(self, name, speed_x, speed_y):
        super().__init__(name)
        self.__input_handler = InputHandler()
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__tap_threshold = 200

    def update(self, game_time):
        self.__input_handler.update()
        self._move_left(game_time)
        self._move_right(game_time)
        self._move_up(game_time)
        self._move_down(game_time)

    def _move_left(self, game_time):
        if self.__input_handler.is_tap(pygame.K_LEFT, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_x = True
                self._parent.get_component(SpriteAnimator2D).set_active_take(ActiveTake.PLAYER_WALKING)
                self._transform.translate_by(Direction.LEFT * self.__speed_x * game_time.elapsed_time)

    def _move_right(self, game_time):
        if self.__input_handler.is_tap(pygame.K_RIGHT, self.__tap_threshold):
            self._parent.get_component(SpriteRenderer2D).flip_x = False
            self._parent.get_component(SpriteAnimator2D).set_active_take(ActiveTake.PLAYER_RUNNING)
            self._transform.translate_by(Direction.RIGHT * self.__speed_x * game_time.elapsed_time)

    def _move_up(self, game_time):
        if self.__input_handler.is_tap(pygame.K_UP, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_y = True
                self._transform.translate_by(Direction.UP * self.__speed_y * game_time.elapsed_time)

    def _move_down(self, game_time):
        if self.__input_handler.is_tap(pygame.K_DOWN, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_y = False
                self._transform.translate_by(Direction.DOWN * self.__speed_y * game_time.elapsed_time)