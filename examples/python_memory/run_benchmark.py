import subprocess

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def normalize_result(result):
	result_list = result.split(',')
	result_list[0] = bool(result_list[0])
	result_list[1] = int(result_list[1])
	result_list[2] = int(result_list[2])
	result_list[3] = int(result_list[3])
	result_list[4] = float(result_list[4])
	result_list[5] = float(result_list[5])
	result_list[6] = float(result_list[6])
	return result_list


def run_command(command):
	command.extend(["-i", "1"])
	print "Run command", command
	p = subprocess.Popen(command, stdout=subprocess.PIPE)
	p.wait()
	out, err = p.communicate()
	return normalize_result(out)


def run_case(case_name, base_command, data_parameters):
	case_result = []
	for monster_data in data_parameters:
		command = list(base_command)
		command.extend(["-i", "1"])
		command.extend(["-a", str(monster_data)])
		result = run_command(command)
		case_result.append(result)
	return case_result


def main():
	method_list = [
		("gc", ["-u", "0"]),
		("manual", ["-u", "1"]),
		("weakref", ["-u", "2"]),
	]
	threshold_list = [700, 3000, 10000]
	attribute_count_list = [0, 20, 40, 60, 80, 100]
	case_list = []
	for threshold in threshold_list:
		for attribute_count in attribute_count_list:
			for method_name, method_parameter in method_list:
				parameter = ["./benchmark.py"]
				parameter.extend(["-t", str(threshold)])
				parameter.extend(["-a", str(attribute_count)])
				parameter.extend(method_parameter)
				case_list.append((method_name, parameter))
	result_list = []
	# Test for manual result.
	for case_name, base_command in case_list:
		result_list.append(run_command(base_command))
	print result_list

	# colors = ['r', 'g', 'b']

	# plt.xlabel("Data per monster")
	# plt.ylabel("Time(seconds)")
	# for i in xrange(2):
	# 	for k, d in enumerate(data_parameters):
	# 		for j in range(3):
	# 			index = i*3+j
	# 			case_result = result_list[index]
	# 			plt.bar(
	# 				(i*6+k)*7+j,
	# 				case_result[k][4],
	# 				color=colors[j])
	# # lgd = plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
	# plt.savefig("total_time.png", bbox_extra_artists=[], bbox_inches="tight")
	# plt.close()

	# plt.xlabel("Data per monster")
	# plt.ylabel("Memory(kb)")
	# for i in xrange(2):
	# 	for k, d in enumerate(data_parameters):
	# 		for j in range(3):
	# 			index = i*3+j
	# 			case_result = result_list[index]
	# 			plt.bar(
	# 				(i*6+k)*7+j,
	# 				case_result[k][5],
	# 				color=colors[j])
	# # lgd = plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
	# plt.savefig("max_memory.png", bbox_extra_artists=[], bbox_inches="tight")
	# plt.close()

	# plt.xlabel("Data per monster")
	# plt.ylabel("Time(seconds)")
	# for i in xrange(2):
	# 	for k, d in enumerate(data_parameters):
	# 		for j in range(3):
	# 			index = i*3+j
	# 			case_result = result_list[index]
	# 			plt.bar(
	# 				(i*6+k)*7+j,
	# 				case_result[k][6],
	# 				color=colors[j])
	# gc_legend = mpatches.Patch(color="r", label="GC")
	# manual_legend = mpatches.Patch(color="g", label="manual")
	# weakref_legend = mpatches.Patch(color="b", label="weakref")
	# lgd = plt.legend(
	# 	handles=[gc_legend, manual_legend, weakref_legend],
	# 	loc="center left",
	# 	bbox_to_anchor=(1, 0.5))
	# plt.savefig("max_iter_time.png", bbox_extra_artists=[lgd,], bbox_inches="tight")
	# plt.close()


if __name__ == "__main__":
	main()
