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
	command.extend(["-i", "1000"])
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
		("gc", ["-u", "0"], "r"),
		("manual", ["-u", "1"], "g"),
		("weakref", ["-u", "2"], "b"),
	]
	threshold_list = [700, 3000, 10000]
	attribute_count_list = [0, 20, 40, 60, 80, 100]
	case_list = []
	for threshold in threshold_list:
		for attribute_count in attribute_count_list:
			for method_name, method_parameter, color in method_list:
				parameter = ["./benchmark.py"]
				parameter.extend(["-t", str(threshold)])
				parameter.extend(["-a", str(attribute_count)])
				parameter.extend(method_parameter)
				case_list.append((method_name, parameter))
	result_list = []
	# Test for manual result.
	for case_name, base_command in case_list:
		result_list.append(run_command(base_command))

	legend_list = []
	for method_name, method_parameter, color in method_list:
		legend_list.append(mpatches.Patch(color=color, label=method_name))

	plt.xlabel("Attribute count\nGC threshold0")
	plt.ylabel("Time(seconds)")
	lgd = plt.legend(
		handles=legend_list,
		loc="center left",
		bbox_to_anchor=(1, 0.5))
	bar_index = 0
	xtick_index = []
	xtick_label = []
	for i, each_result in enumerate(result_list):
		method_index = i % len(method_list)
		if method_index == 0:
			bar_index += 2
			label = str(attribute_count_list[(i/len(method_list))%len(attribute_count_list)])
			if i % (len(method_list)*len(attribute_count_list)) == 0:
				bar_index += 1
				label += "\n{0}".format(threshold_list[i/(len(method_list)*len(attribute_count_list))])
			xtick_label.append(label)
			xtick_index.append(bar_index)
		else:
			bar_index += 1
		color = method_list[method_index][2]
		plt.bar(bar_index, each_result[4], color=color)
	plt.xticks(xtick_index, xtick_label, ha="left")
	plt.savefig("total_time.png", bbox_extra_artists=[lgd,], bbox_inches="tight")
	plt.close()

	plt.xlabel("Attribute count\nGC threshold0")
	plt.ylabel("Memory(kb)")
	lgd = plt.legend(
		handles=legend_list,
		loc="center left",
		bbox_to_anchor=(1, 0.5))
	bar_index = 0
	xtick_index = []
	xtick_label = []
	for i, each_result in enumerate(result_list):
		method_index = i % len(method_list)
		if method_index == 0:
			bar_index += 2
			label = str(attribute_count_list[(i/len(method_list))%len(attribute_count_list)])
			if i % (len(method_list)*len(attribute_count_list)) == 0:
				bar_index += 1
				label += "\n{0}".format(threshold_list[i/(len(method_list)*len(attribute_count_list))])
			xtick_label.append(label)
			xtick_index.append(bar_index)
		else:
			bar_index += 1
		color = method_list[method_index][2]
		plt.bar(bar_index, each_result[5], color=color)
	plt.xticks(xtick_index, xtick_label, ha="left")
	plt.savefig("max_memory.png", bbox_extra_artists=[lgd,], bbox_inches="tight")
	plt.close()

	plt.xlabel("Attribute count\nGC threshold0")
	plt.ylabel("Time(seconds)")
	lgd = plt.legend(
		handles=legend_list,
		loc="center left",
		bbox_to_anchor=(1, 0.5))
	bar_index = 0
	xtick_index = []
	xtick_label = []
	for i, each_result in enumerate(result_list):
		method_index = i % len(method_list)
		if method_index == 0:
			bar_index += 2
			label = str(attribute_count_list[(i/len(method_list))%len(attribute_count_list)])
			if i % (len(method_list)*len(attribute_count_list)) == 0:
				bar_index += 1
				label += "\n{0}".format(threshold_list[i/(len(method_list)*len(attribute_count_list))])
			xtick_label.append(label)
			xtick_index.append(bar_index)
		else:
			bar_index += 1
		color = method_list[method_index][2]
		plt.bar(bar_index, each_result[-1], color=color)
	plt.xticks(xtick_index, xtick_label, ha="left")
	plt.savefig("max_time.png", bbox_extra_artists=[lgd,], bbox_inches="tight")
	plt.close()


if __name__ == "__main__":
	main()
