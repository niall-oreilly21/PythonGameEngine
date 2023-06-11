import json
import random

import pygame
from pygame import Vector2

from App.Components.Controllers.BossEnemyController import BossEnemyController
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.EnemyHealthBarController import EnemyHealthBarController
from App.Components.Controllers.ZapEnemyController import ZapEnemyController
from App.Constants.Application import Application
from App.Constants.Constants import Constants
from App.Constants.EntityConstants import EntityConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.GameObjects.GameObject import GameObject
from Engine.GameObjects.Gun.Bullet import Bullet
from Engine.GameObjects.Gun.Gun import Gun
from Engine.GameObjects.Gun.GunController import GunController
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.MapID import MapID
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Transform2D import Transform2D


class MapLoader:
    def __init__(self, player):
        self.__player = player
        self.__enemies = \
            {
                Constants.Scene.EARTH: [],
                Constants.Scene.MARS: [],
                Constants.Scene.SATURN: []
            }

    def map_load(self, scene, planet_json):
        tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

        # Add tiles to the tileset
        tileset.add_tile(Tile("Grass", Constants.Tile.GRASS, Vector2(216, 12)))
        tileset.add_tile(Tile("Water", Constants.Tile.WATER, Vector2(264, 156)))
        tileset.add_tile(Tile("Dark Grass", Constants.Tile.DARK_GRASS, Vector2(216, 108)))
        tileset.add_tile(Tile("Dirt", Constants.Tile.DIRT, Vector2(308, 12)))
        tileset.add_tile(Tile("Sand", Constants.Tile.SAND, Vector2(216, 156)))
        tileset.add_tile(Tile("CoarseDirt", Constants.Tile.COARSE_DIRT, Vector2(216, 108)))
        tileset.add_tile(Tile("SaturnDirt", 10, Vector2(308, 12)))
        tileset.add_tile(Tile("SaturnSand", 7, Vector2(216, 156)))
        tileset.add_tile(Tile("SaturnSpawnRegion", 4, Vector2(216, 156)))

        map_data = []

        # load map data
        file_path = planet_json

        with open(file_path, "r") as file:
            json_data = json.load(file)

        tile_data = json_data["grounds"]
        object_data = json_data["objects"]

        width = 110
        height = 120

        if scene.name == Constants.Scene.EARTH:
            self.__load_planet_earth_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, None, None)
        elif scene.name == Constants.Scene.MARS:
            self.__load_planet_mars_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, [255, 100, 150], 220)
        elif scene.name == Constants.Scene.SATURN:
            self.__load_planet_saturn_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, [255, 255, 0], 150)

        # Object generation
        for object in object_data:
            if object["x"] < width and object["y"] < height:
                x = object["x"]
                y = object["y"]
                id = object["t"]["id"]
                if id == 5:
                    if planet_json == Constants.Map.PLANET_EARTH_JSON:
                        tree_object = random.choice(
                            [GameObjectConstants.Foliage.TALL_TREE.clone(),
                             GameObjectConstants.Foliage.LOW_TREE.clone()])
                        tree_collider = BoxCollider2D("TreeCollider")
                        if tree_object.name == "Tree":
                            tree_collider.scale = Vector2(0.3, 0.15)
                            tree_collider.offset = Vector2(3, 72)
                        else:
                            tree_collider.scale = Vector2(0.5, 0.25)
                            tree_collider.offset = Vector2(0, 32)
                        tree_object.add_component(tree_collider)
                        tree_object.transform.position = Vector2(x * 71,
                                                                 y * 71)  # starting area forces every tree to one point
                        scene.add(tree_object)
                    elif planet_json == Constants.Map.PLANET_SATURN_JSON:
                        tree_object = GameObjectConstants.NaturalStructures.ROCK_THREE.clone()
                        tree_collider = BoxCollider2D("TreeCollider")
                        tree_object.add_component(tree_collider)
                        tree_object.transform.position = Vector2(x * 71,
                                                                 y * 71)  # starting area forces every tree to one point
                        scene.add(tree_object)
                elif id == 15:
                    if planet_json == Constants.Map.PLANET_EARTH_JSON:
                        bush_object = random.choice(
                            [GameObjectConstants.Foliage.BUSH_ONE.clone(), GameObjectConstants.Foliage.BUSH_TWO.clone(),
                             GameObjectConstants.Foliage.BUSH_FOUR.clone(),
                             GameObjectConstants.NaturalStructures.ROCK_ONE.clone()])
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        if bush_object.name == "RockOne":
                            scale = random.uniform(0.7, 2)
                            bush_object.transform.scale = Vector2(scale, scale)
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                    elif planet_json == Constants.Map.PLANET_MARS_JSON:
                        bush_object = random.choice([GameObjectConstants.Foliage.BUSH_THREE.clone(),
                                                     GameObjectConstants.Foliage.DEAD_BUSH.clone()])
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                    elif planet_json == Constants.Map.PLANET_SATURN_JSON:
                        bush_object = GameObjectConstants.Foliage.DEAD_BUSH.clone()
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                elif id == 11:
                    lilypad_object = random.choice([GameObjectConstants.Foliage.LILYPAD_ONE.clone(),
                                                    GameObjectConstants.Foliage.LILYPAD_TWO.clone()])
                    lilypad_object.transform.rotation = random.randint(0, 360)
                    lilypad_object.transform.position = Vector2(x * 72.5, y * 72.5)

                    scene.add(lilypad_object)
                elif id == 1:
                    power_up_object = random.choice([GameObjectConstants.Consumables.POTION_SPEED.clone(),
                                                     GameObjectConstants.Consumables.POTION_HEAL.clone(),
                                                     GameObjectConstants.Consumables.POTION_ATTACK.clone(),
                                                     GameObjectConstants.Consumables.POTION_DEFENSE.clone(),
                                                     GameObjectConstants.Consumables.RANDOM_POWER_UP.clone()])
                    power_up_object.transform.position = Vector2(x * 72.5, y * 72.5)
                    power_up_collider = BoxCollider2D("PowerUpCollider")
                    power_up_collider.scale = Vector2(2.5, 2.5)
                    power_up_object.add_component(power_up_collider)
                    scene.add(power_up_object)

        # Create the map using the tileset and map data
        map_tiles = tileset.create_map(map_data)

        for tiles in map_tiles:
            for tile in tiles:
                tile.transform.scale = Vector2(2, 2)
                tile.transform.position *= 2
                scene.add(tile)

    def __color_tiles(self, map_data, tile_data, width, height, color, alpha):
        # Create Default Tiles
        for x in range(height):
            row = []
            for z in range(width):
                tile = TileAttributes(Constants.Tile.WATER, False, color, alpha)
                row.append(tile)
            map_data.append(row)

        for ground in tile_data:
            if ground["x"] < width and ground["y"] < height:
                x = ground["x"]
                y = ground["y"]
                s_id = ground["s"]["id"]
                if s_id == Constants.Tile.WATER:
                    map_data[y][x] = TileAttributes(s_id, True, color, alpha)
                else:
                    map_data[y][x] = TileAttributes(s_id, False, color, alpha)

    def load_planet_dynamic_objects(self, scene):
        if not scene.contains(self.__player):
            scene.add(self.__player)

        self.__check_enemy_in_scene(scene)
        scene.start()

    def __check_enemy_in_scene(self, scene):
        for enemy in self.__enemies[scene.name]:
            if not scene.contains(enemy):
                scene.add(enemy)

    def __add_enemy_to_scene(self, enemy, scene):
        self.__enemies[scene.name].append(enemy)

        if scene.name == Constants.Scene.EARTH:
            print(len(self.__enemies[scene.name]))

        scene.add(enemy)

    def load_enemies(self, enemy_waypoints, enemy_type, enemy, scene):
        enemy_type_name = EntityConstants.Enemy.ALIEN_ENEMY_NAME
        if enemy_type == GameObjectCategory.Rat:
            enemy_type_name = EntityConstants.Enemy.RAT_ENEMY_NAME
        elif enemy_type == GameObjectCategory.Wolf:
            enemy_type_name = EntityConstants.Enemy.WOLF_ENEMY_NAME

        for waypoints in enemy_waypoints[enemy_type_name]:
            new_enemy = enemy.clone()
            new_enemy.initial_position = waypoints[0]
            new_enemy.get_component(WaypointFinder).waypoints = waypoints
            self.__add_enemy_to_scene(new_enemy, scene)

    def load_planet_earth_enemies(self, scene):
        enemy = EntityConstants.Enemy.RAT_ENEMY.clone()
        enemy.add_component(EnemyController("Enemy movement", self.__player, Constants.EnemyRat.MOVE_SPEED, 400))

        HEALTH_BAR = GameObject("Health Bar", Transform2D(Vector2(0, 0), 0, Vector2(0.3, 0.3)), GameObjectType.Dynamic,
                                GameObjectCategory.Entity)

        __HEALTH_BAR_IMAGE = pygame.image.load("Assets/UI/health_bar.png")

        __MATERIAL_HEALTH_BAR = TextureMaterial2D(__HEALTH_BAR_IMAGE, None, Vector2(0, 0), None)

        __RECT_MATERIAL_HEALTH_BAR = RectMaterial2D(375, 50, (0, 224, 79), 255, Vector2(58, 28))
        __RECT_MATERIAL_HEALTH_BAR_BACKGROUND = RectMaterial2D(375, 50, (0, 0, 0), 255, Vector2(58, 28))

        HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Texture", __MATERIAL_HEALTH_BAR, RendererLayers.UIHealthBar, False))
        HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect Background", __RECT_MATERIAL_HEALTH_BAR_BACKGROUND,
                       RendererLayers.UIBackground, False))
        HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect", __RECT_MATERIAL_HEALTH_BAR, RendererLayers.UI, False))
        HEALTH_BAR.add_component(EnemyHealthBarController("Health Bar Controller Enemy", enemy))
        enemy.health_bar = HEALTH_BAR
        scene.add(HEALTH_BAR)

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Rat, enemy, scene)

    def load_planet_mars_enemies(self, scene):
        enemy = EntityConstants.Enemy.WOLF_ENEMY.clone()
        enemy.add_component(
            ZapEnemyController("Enemy movement", self.__player, Constants.EnemyWolf.MOVE_SPEED, 600, 20, 3))

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Wolf, enemy, scene)

    def load_planet_saturn_enemies(self, scene):
        gun = GameObjectConstants.Gun.Gun

        enemy = EntityConstants.Enemy.ALIEN_ENEMY.clone()
        enemy.add_component(
            BossEnemyController("Enemy movement", self.__player, Constants.EnemyAlien.MOVE_SPEED, 800, 10, gun))
        scene.add(gun)

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Alien, enemy, scene)

        # Boss?
        init_pos = 3200, 4000
        boss = EntityConstants.Enemy.ALIEN_ENEMY
        boss.initial_position = Vector2(init_pos)
        boss.transform.scale = Vector2(5, 5)
        boss.transform.position = Vector2(3207.8, 4013)
        boss.add_component(
            BossEnemyController("Enemy movement", self.__player, Constants.EnemyAlien.MOVE_SPEED, 800, 10, gun))
        boss.get_component(WaypointFinder).waypoints = [Vector2(init_pos), Vector2(3000, 4000)]

    def __load_planet_earth_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_ONE.clone()
        ruin.transform.position = Vector2(2850, 2600)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_TWO.clone()
        ruin.transform.position = Vector2(4800, 1900)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_THREE.clone()
        ruin.transform.position = Vector2(3100, 4600)
        scene.add(ruin)

        statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
        statue.transform.position = Vector2(2800, 4700)
        scene.add(statue)

        teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
        teleporter.transform.position = Vector2(2600, 4800)
        scene.add(teleporter)

        bridge_x = 6406
        bridge_y = 5463

        island = GameObjectConstants.NaturalStructures.ISLAND.clone()
        island.transform.position = Vector2(bridge_x + 47 * 7 + 22, bridge_y - 45)
        scene.add(island)

        bridge = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
        bridge.transform.position = Vector2(bridge_x, bridge_y)
        scene.add(bridge)

        bridge2 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
        bridge2.transform.position = Vector2(bridge_x + 47, bridge_y)
        scene.add(bridge2)

        bridge3 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
        bridge3.transform.position = Vector2(bridge_x + 47 * 3, bridge_y)
        scene.add(bridge3)

        bridge4 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
        bridge4.transform.position = Vector2(bridge_x + 47 * 5, bridge_y)
        scene.add(bridge4)

    def __load_planet_mars_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_FOUR.clone()
        ruin.transform.position = Vector2(2450, 3500)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_FIVE.clone()
        ruin.transform.position = Vector2(3700, 3700)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_SIX.clone()
        ruin.transform.position = Vector2(3900, 1800)
        scene.add(ruin)

        statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
        statue.transform.position = Vector2(2500, 4700)
        scene.add(statue)

        teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
        teleporter.transform.position = Vector2(3788.2, 4600)
        scene.add(teleporter)

    def __load_planet_saturn_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_SEVEN.clone()
        ruin.transform.position = Vector2(2800, 3500)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_EIGHT.clone()
        ruin.transform.position = Vector2(3700, 2600)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_NINE.clone()
        ruin.transform.position = Vector2(4500, 3500)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
        teleporter.transform.position = Vector2(584, 6350.2)
        scene.add(teleporter)
