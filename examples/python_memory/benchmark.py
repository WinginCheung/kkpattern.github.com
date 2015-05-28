import argparse
import time
import gc
import resource


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
		"--enable-unloop",
		action="store_true",
		help="Enable manunally unloop.")
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
		default=100,
		help="Dungeon created per iteration.")
	parser.add_argument(
		"-m",
		"--monster-per-dungeon",
		type=int,
		default=500,
		help="Monster added per dungeon.")
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
	def __init__(self):
		self._dungeon = None

	def on_add_to_dungeon(self, dungeon):
		self._dungeon = dungeon


def run_logic_with_unloop(max_iteration, dungeon_per_iter, monster_per_dungeon):
	for i in xrange(max_iteration):
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				monster = Monster()
				dungeon.add_monster(monster)
			dungeon.destroy()


def run_logic(max_iteration, dungeon_per_iter, monster_per_dungeon):
	for i in xrange(max_iteration):
		for dc in xrange(dungeon_per_iter):
			dungeon = Dungeon()
			for mc in xrange(monster_per_dungeon):
				monster = Monster()
				dungeon.add_monster(monster)


def main():
	arguments = parse_arguments()
	if arguments.disable_gc:
		gc.disable()
	elif arguments.gc_threshold0 is not None:
		gc.set_threshold(arguments.gc_threshold0)
	if arguments.enable_unloop:
		benchmark_method = run_logic_with_unloop
	else:
		benchmark_method = run_logic
	gc_model = not arguments.disable_gc
	gc_threshold0 = gc.get_threshold()[0]
	unloop = arguments.enable_unloop
	begin_at = time.time()
	benchmark_method(
		arguments.max_iteration,
		arguments.dungeon_per_iter,
		arguments.monster_per_dungeon)
	end_at = time.time()
	time_usage = end_at-begin_at
	memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*0.001
	print "{0},{1},{2},{3},{4}".format(
		gc_model, gc_threshold0, unloop, time_usage, memory)


if __name__ == "__main__":
	main()
