from typing import Dict

import pygame

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.GameObject import GameObject
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class CameraManager(Manager):
    def __init__(self, screen, sceneManager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__screen = screen
        self.__active_camera = None
        self.__active_game_object = None
        self.__cameras = {}
        self.__sceneManager = sceneManager
        self.player_is_moving = False

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CameraManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.MenuCamera:
            self.set_active_camera(GameConstants.Cameras.MENU_CAMERA)
            Application.ActiveCamera = self.__active_camera

        elif event_data.event_action_type == EventActionType.GameCamera:
            self.set_active_camera(GameConstants.Cameras.GAME_CAMERA)
            Application.ActiveCamera = self.__active_camera

        elif event_data.event_action_type == EventActionType.SetCameraTarget:
            target = event_data.parameters[0]
            self.__set_active_camera_target(target)


    @property
    def active_camera_transform(self):
        if self.__active_game_object is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_game_object.transform

    @property
    def active_camera_name(self):
        if self.__active_game_object is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_game_object.name

    @property
    def active_camera(self):
        if self.__active_camera is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_camera

    def __set_active_camera_target(self, target):

        third_person_controller = self.__active_game_object.get_component(ThirdPersonController)

        if third_person_controller:
            third_person_controller.target = target


    def add(self, camera):
        id = camera.name.strip().lower()

        if id in self.__cameras:
            return False

        self.__cameras[id] = camera
        return True

    def set_active_camera(self, id):
        camera_game_object = None
        id = id.strip().lower()

        if id in self.__cameras:
            camera_game_object = self.__cameras[id]

        if camera_game_object is not None:
            self.__active_camera = camera_game_object.get_component(Camera)
            self.__active_game_object = camera_game_object

        if self.__active_camera:
            self.__set_viewport()

    def get_active_camera_position(self):
        return self.__active_camera.transform.position

    def __set_viewport(self):
        self.__screen = pygame.display.set_mode((self.__active_camera.viewport.x, self.__active_camera.viewport.y))

    def start(self):
        for camera in self.__cameras:
            self.__cameras[camera].start()

    def update(self, game_time):
        self.__active_game_object.update(game_time)
