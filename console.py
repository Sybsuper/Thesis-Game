import shutil
import sys
from os import path

import pygame.math

from core.items.items import Items
from settings import *
from world.world import World


class Console:
	def __init__(self, game):
		self.game = game
		self.running = True

	def run(self):
		while self.running:
			inp = sys.stdin.readline()
			s = inp.split()
			if s[0] == "give":
				try:
					it = Items.getItemFromName(s[1])
					if it is not None:
						self.game.player.inventory.add_new_item(it, 1 if len(s) == 2 else int(s[2]))
						continue
					print(f"Could not add {s[1]} to inventory, please check your spelling and try again")
				except ValueError:
					print("Could not convert int to string")
				except IndexError:
					print(f"Expected at least 1 argument, got {len(s) - 1} instead")
				continue
			elif s[0] == "spawn":
				try:
					# TODO: add all enemies with arguments
					if self.game.spawner.spawnEventLoc(float(s[1]), float(s[2])):
						print(f"Could not spawn an enemy at ({s[1]}, {s[2]})")
				except IndexError:
					self.game.spawner.spawnEvent()
				except ValueError:
					print(f"Could not convert ({s[1]}, {s[2]}) to a position, please try again.")
				print(self.game.world.entities)
				continue
			elif s[0] == "debug":
				try:
					if s[1] == "pos" or s[1] == "position":
						print(self.game.player.pos)
					elif s[1] == "chunk":
						print(self.game.player.pos / TILESIZE // 16)
					elif s[1] == "ent" or s[1] == "entity":
						if s[2] == "pos" or s[2] == "position":
							for ent in self.game.world.entities:
								print(ent.pos)
				except IndexError:
					print(f"Expected at least 1 argument, got {len(s) - 1} instead")
				continue
			elif s[0] == "setpos":
				try:
					self.game.player.pos = pygame.math.Vector2(float(s[1]), float(s[2]))
				except ValueError:
					print(
						f"Could not convert ({s[1]}. {s[2]}) to a valid position, please check your values and try again")
				except IndexError:
					print(f"Expected 2 arguments, got {len(s) - 1} instead")
				continue
			elif s[0] == "xp":
				try:
					if s[1] == "give" or s[1] == "add":
						if len(s) < 4:
							self.game.player.lvl.xp += int(s[2])
						else:
							try:
								if s[2].lower() == "p" or s[2].lower() == "player":
									self.game.player.lvl.xp += int(s[3])
							# TODO: Add all induvidual skills (possibly without if chain)
							except ValueError:
								print(f"Could not convert {s[3]} to an integer, please check your values and try again")
							except IndexError:
								print(f"Expected 4 arguments, got {len(s) - 1} instead")
				except ValueError:
					print(f"Could not convert {s[2]} to an integer, please check your values and try again")
				except IndexError:
					print(f"Expected at least 2 arguments, got {len(s) - 1} instead")
				else:
					self.game.player.check_levels()
				continue
			elif s[0] == "loadmap":
				try:
					p = path.join(GAMEDIR, f"saves/{s[1]}")
					if not path.isdir(p):
						raise NotADirectoryError
					self.game.world = World(p, self.game)
					self.game.world.load()
				except IndexError:
					print(f"Expected at least 1 argument, got {len(s) - 1} instead")
				except NotADirectoryError:
					try:
						p = path.join(GAMEDIR, f"world/dungeon/dungeons/{s[1].rsplit('/')[-1]}")
						if not path.isdir(p):
							raise NotADirectoryError
						try:
							print(f"Copying {p} to {path.join(GAMEDIR, f'saves/{self.game.world.name}/{s[1]}')}")
							p = shutil.copytree(p, path.join(GAMEDIR, f"saves/{self.game.world.name}/{s[1]}"))
						except FileExistsError:
							p = path.join(GAMEDIR, f"saves/{self.game.world.name}/{s[1]}")
						print(f"p: {p}")
						self.game.world = World(p, self.game)
						self.game.world.load()
					except NotADirectoryError:
						print(f"Could not open map: {s[1]}")
				continue

			print(f"Could not find command {s[0]}. Please check for correct spelling")

	def kill(self):
		self.running = False
