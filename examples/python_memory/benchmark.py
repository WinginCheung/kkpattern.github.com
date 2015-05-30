#!/usr/bin/env python
import argparse
import time
import gc
import resource
import sys
import weakref


ATTRIBUTE_NAME_LIST = None


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-g",
		"--disable-gc",
		action="store_true",
		help="Disable gc.")
	parser.add_argument(
		"-t",
		"--gc-threshold0",
		type=int,
		help="GC threshold0. If gc is not enabled this parameter is omitted.")
	parser.add_argument(
		"-u",
		"--unloop-model",
		type=int,
		choices=[0, 1, 2],
		help=(
			"Unloop model. 0: do not unloop; 1: unloop manually;"
			"2: unloop by weakref."))
	parser.add_argument(
		"-i",
		"--max-iteration",
		type=int,
		default=1000,
		help="Max iteration of test.")
	parser.add_argument(
		"-d",
		"--dungeon-per-iter",
		type=int,
		default=50,
		help="Dungeon created per iteration.")
	parser.add_argument(
		"-m",
		"--monster-per-dungeon",
		type=int,
		default=200,
		help="Monster added per dungeon.")
	parser.add_argument(
		"-a",
		"--monster-data",
		type=int,
		default=10,
		help="The data length in a monster.")
	return parser.parse_args()


class Dungeon(object):
	def __init__(self):
		self._monster_list = []

	def add_monster(self, monster):
		self._monster_list.append(monster)
		monster.on_add_to_dungeon(self)

	def destroy(self):
		self._monster_list = []

class Monster(object):
	ATTRIBUTE_NAME_LIST = None
	def __init__(self, monster_data):
		self._dungeon = None
		for i in xrange(monster_data):
			self.__dict__[Monster.ATTRIBUTE_NAME_LIST[i]] = i

	def on_add_to_dungeon(self, dungeon):
		self._dungeon = dungeon


class MonsterWithWeakref(Monster):
	def on_add_to_dungeon(self, dungeon):
		self._dungeon = weakref.ref(dungeon)


def run_logic_with_unloop_manullay(
		max_iteration, dungeon_per_iter, monster_per_dungeon, monster_data):
	max_iter_time = 0
	for i in xrange(max_iteration):
		begin_at = time.time()
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				monster = Monster(monster_data)
				dungeon.add_monster(monster)
			dungeon.destroy()
		end_at = time.time()
		max_iter_time = max(max_iter_time, end_at-begin_at)
	return max_iter_time


def run_logic_without_unloop(
		max_iteration, dungeon_per_iter, monster_per_dungeon, monster_data):
	max_iter_time = 0
	for i in xrange(max_iteration):
		begin_at = time.time()
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				monster = Monster(monster_data)
				dungeon.add_monster(monster)
		end_at = time.time()
		max_iter_time = max(max_iter_time, end_at-begin_at)
	return max_iter_time


def run_logic_with_unloop_weakref(
		max_iteration, dungeon_per_iter, monster_per_dungeon, monster_data):
	max_iter_time = 0
	for i in xrange(max_iteration):
		begin_at = time.time()
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				monster = MonsterWithWeakref(monster_data)
				dungeon.add_monster(monster)
		end_at = time.time()
		max_iter_time = max(max_iter_time, end_at-begin_at)
	return max_iter_time


def main():
	arguments = parse_arguments()
	if arguments.disable_gc:
		gc.disable()
	elif arguments.gc_threshold0 is not None:
		gc.set_threshold(arguments.gc_threshold0)
	if arguments.unloop_model == 0:
		benchmark_method = run_logic_without_unloop
	elif arguments.unloop_model == 1:
		benchmark_method = run_logic_with_unloop_manullay
	elif arguments.unloop_model == 2:
		benchmark_method = run_logic_with_unloop_weakref
	else:
		# This shouldn't happen.
		sys.exit(1)
	gc_model = not arguments.disable_gc
	gc_threshold0 = gc.get_threshold()[0]
	unloop = arguments.unloop_model
	monster_data = arguments.monster_data
	Monster.ATTRIBUTE_NAME_LIST = [
		"attribute_{0}".format(i) for i in xrange(monster_data)]
	begin_at = time.time()
	max_iter_time = benchmark_method(
		arguments.max_iteration,
		arguments.dungeon_per_iter,
		arguments.monster_per_dungeon,
		arguments.monster_data)
	end_at = time.time()
	time_usage = end_at-begin_at
	memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*0.001
	print "{0},{1},{2},{3},{4},{5},{6}".format(
		gc_model, gc_threshold0, unloop, monster_data, time_usage, memory,
		max_iter_time)


if __name__ == "__main__":
	main()
