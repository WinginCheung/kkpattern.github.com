#!/usr/bin/env python
import argparse
import time
import gc
import resource
import sys
import weakref

import matplotlib.pyplot as plt


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
		default=0,
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
		"--attribute-count",
		type=int,
		default=20,
		help="The attribute count in a monster.")
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
	def __init__(self, attribute_count):
		self._dungeon = None
		for i in xrange(attribute_count):
			self.__dict__[Monster.ATTRIBUTE_NAME_LIST[i]] = i

	def on_add_to_dungeon(self, dungeon):
		self._dungeon = dungeon


class MonsterWithWeakref(Monster):
	def on_add_to_dungeon(self, dungeon):
		self._dungeon = weakref.ref(dungeon)


def run_logic(
		max_iteration, dungeon_per_iter, monster_per_dungeon, attribute_count,
		unloop_model):
	iter_timer_list = []
	for i in xrange(max_iteration):
		begin_at = time.time()
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				if unloop_model == 2:
					monster = MonsterWithWeakref(attribute_count)
				else:
					monster = Monster(attribute_count)
				dungeon.add_monster(monster)
			if unloop_model == 1:
				dungeon.destroy()
		end_at = time.time()
		iter_timer_list.append(end_at-begin_at)
	return iter_timer_list


def run_test_and_plot(
		test_name, max_iteration, dungeon_per_iter, monster_per_dungeon,
		attribute_count, unloop_model):
	print "Run test:", test_name
	gc.collect()
	iter_timer_list = run_logic(
		max_iteration,
		dungeon_per_iter,
		monster_per_dungeon,
		attribute_count,
		unloop_model)
	plt.plot(iter_timer_list, label=test_name)
	gc.collect()


def main():
	arguments = parse_arguments()
	if arguments.disable_gc:
		gc.disable()
	elif arguments.gc_threshold0 is not None:
		gc.set_threshold(arguments.gc_threshold0)
	Monster.ATTRIBUTE_NAME_LIST = [
		"attribute_{0}".format(i) for i in xrange(arguments.attribute_count)]

	test_list = [
		("GC(threshold0:700)", 700, 0),
		("GC(threshold0:10000)", 700, 0),
		("Manual", None, 1),
		("Weakref", None, 2),
	]

	for test_name, threshold, unloop_model in test_list:
		if threshold is not None:
			gc.set_threshold(threshold)
		run_test_and_plot(
			test_name,
			arguments.max_iteration,
			arguments.dungeon_per_iter,
			arguments.monster_per_dungeon,
			arguments.attribute_count,
			unloop_model)
	lgd = plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
	plt.savefig(
		"benchmark.png", bbox_extra_artists=[lgd,], bbox_inches="tight")


if __name__ == "__main__":
	main()
