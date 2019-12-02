#!/usr/bin/python

import argparse
import os
import subprocess
import json
from template import TEMPLATE as TEMPLATE_DATA

def strf(flush):
	return "[!] " + flush

def debug(flush):
	print(strf(flush))

def add_problem(PATH, PLATFORM, CONTEST, PROBLEM):
	create_config(PATH, CONFIG_DATA)
	with open(PATH, "r+") as config_file:
		data = json.load(config_file)
		data["contests"][CONTEST]["problems"] = data["contests"][CONTEST]["problems"] + [PROBLEM]
		data["contests"][CONTEST]['recent'] = PROBLEM

		config_file.seek(0)
		json.dump(data, config_file)
		config_file.truncate()

def set_config(PATH, PLATFORM, CONTEST):
	create_config(PATH, CONFIG_DATA)
	with open(PATH, "r+") as config_file:
		data = json.load(config_file)
		data["contests"][CONTEST] = {
			'platform' : PLATFORM,
			'problems' : [],
			'recent' : ''
		}
		config_file.seek(0)
		json.dump(data, config_file)
		config_file.truncate()


def create_config(PATH, CONFIG_DATA):
	if os.path.exists(PATH):
		debug("Config already present!")
	else:
		with open(PATH, 'w') as outfile:
			json.dump(CONFIG_DATA, outfile)


def clear_config(CONFIG_PATH):
	os.remove(CONFIG_PATH)
	create_config(CONFIG_PATH, CONFIG_DATA)
	debug("Clean Complete")


def set_template(PATH):
	with open(PATH, 'w') as temp_file:
		temp_file.write(TEMPLATE_DATA)


def set_inp(PATH):
	with open(PATH, 'w') as inp_file:
		inp_file.write("")

def set_recent_contest(PATH, CONTEST):
	create_config(PATH, CONFIG_DATA)
	with open(PATH, "r+") as config_file:
		data = json.load(config_file)
		data["recent"] = CONTEST

		config_file.seek(0)
		json.dump(data, config_file)
		config_file.truncate()


def get_recent_contest(CONFIG_PATH):
	if not os.path.exists(CONFIG_PATH):
		return None, None

	current_contest = ""
	current_platform = ""

	with open(CONFIG_PATH, 'r') as config_file:
		data = json.load(config_file)
		current_contest = data['recent']
		current_platform = data['contests'][current_contest]['platform']

	return current_contest, current_platform


def show_all(CONFIG_PATH):
	all_contests = []
	with open(CONFIG_PATH, "r") as config_file:
		data = json.load(config_file)
		all_contests = data['contests'].keys()

	for contest in all_contests:
		debug(contest)



DESCRIPTION = strf("Contest CLI for ELEMENT13")
CREATE = strf("New Contest Name")
NEWFILE = strf("New File Name for the Contest")
TEMPLATE = strf("Template for Contest")
PLATFORM = strf("Platform such as Codechef, Codeforces, Codejam")
CONTESTNAME = strf("Existing Contest Name for -c <Contest Name> -n <File Name>")

DESKTOP = os.path.join(os.path.expanduser('~'), 'Desktop')
CONTESTS = 'Contests'
CONFIG_NAME = '.contests.json'
TEMPLATE_NAME = '.template'
CONFIG_PATH = os.path.join(DESKTOP, CONTESTS, CONFIG_NAME)
TEMPLATE_PATH = os.path.join(DESKTOP, CONTESTS, TEMPLATE_NAME)

OUT_OBJ = "out.o"
INP_FILE = "inp.txt"

CONFIG_DATA = {
	'contests' : {},
	'recent' : ''
}


def get_args():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('--setup', action='store_true', required=False)
	parser.add_argument('--create', action='store_true', help=CREATE, required=False)
	parser.add_argument('--template', type=str, help=TEMPLATE, required=False)
	parser.add_argument('--prob', type=str, help=NEWFILE, required=False)
	parser.add_argument('--platform', type=str, help=PLATFORM, required=False)
	parser.add_argument('--contest', type=str, help=CONTESTNAME, required=False)
	parser.add_argument('--compile', action='store_true', required=False)
	parser.add_argument('--clean', action='store_true', required=False)
	parser.add_argument('--run', action='store_true', required=False)
	parser.add_argument('--edit', type=str, required=False)
	parser.add_argument('--all', action='store_true', required=False)

	return parser.parse_args()

def setup(PATH, NAME):
	if os.path.exists(PATH):
		debug(NAME + " is already present!")
	else:
		os.mkdir(PATH)
		# debug("Setup Complete!")

def setup_contest(platform, contest):
	PATH = os.path.join(DESKTOP, CONTESTS)

	if not os.path.exists(PATH):
		setup(PATH, "CONTESTS")

	platform = platform.capitalize()
	PATH = os.path.join(PATH, platform)

	if not os.path.exists(PATH):
		setup(PATH, platform)

	contest = contest.capitalize()
	PATH = os.path.join(PATH, contest)

	if not os.path.exists(PATH):
		setup(PATH, contest)

	PATH = os.path.join(DESKTOP, CONTESTS, platform, contest)
	PATH_INP = os.path.join(PATH, INP_FILE)
	
	set_inp(PATH_INP)

	# debug("Contest Created")

	set_config(CONFIG_PATH, platform, contest)

	# debug("Config Setup Complete")


	set_template(TEMPLATE_PATH)
	# debug("Template setup Complete")

	set_recent_contest(CONFIG_PATH, contest)

	debug("Done creating contest")


def create_problem(platform, contest, filename):
	platform, contest = platform.capitalize(), contest.capitalize()
	PATH = os.path.join(DESKTOP, CONTESTS, platform, contest, filename)

	if os.path.exists(PATH):
		debug("Problem already exists in the Contest")
	else:
		with open(PATH, 'w') as problem_file:
			with open(TEMPLATE_PATH, 'r') as template_file:
				problem_file.write(template_file.read())
				problem_file.truncate()

	add_problem(CONFIG_PATH, platform, contest, filename)
	set_current_problem(filename)

def compile(platform, contest, problem):
	PATH = os.path.join(DESKTOP, CONTESTS, platform, contest)
	PATH_PROB = os.path.join(PATH, problem)
	PATH_OUT = os.path.join(PATH, OUT_OBJ)

	compile_format = "g++ {0} -o {1} -std=c++11".format(PATH_PROB, PATH_OUT)

	returned_value = subprocess.call(compile_format, shell=True)


def compile_recent(contest):
	current_problem = ""
	current_contest = ""
	current_platform = ""
	with open(CONFIG_PATH, 'r') as config_file:
		data = json.load(config_file);
		current_contest = data['recent']
		current_platform = data['contests'][current_contest]['platform']
		current_problem = data['contests'][current_contest]['recent']

	compile(current_platform, current_contest, current_problem)


def run_problem(contest, platform):
	PATH = os.path.join(DESKTOP, CONTESTS, platform, contest)
	PATH_OUT = os.path.join(PATH, OUT_OBJ)
	PATH_INP = os.path.join(PATH, INP_FILE)

	run_format = "{0} < {1}".format(PATH_OUT, PATH_INP)

	returned_value = subprocess.call(run_format, shell=True)


def set_current_problem(problem):
	contest, platform = get_recent_contest(CONFIG_PATH)

	with open(CONFIG_PATH, 'r+') as config_file:
		data = json.load(config_file)
		data['contests'][contest]['recent'] = problem

		config_file.seek(0)

		json.dump(data, config_file)
		config_file.truncate()



def main():

	args = get_args()

	if args.setup:
		PATH = os.path.join(DESKTOP, CONTESTS)
		setup(PATH, "CONTEST")
		create_config(CONFIG_PATH, CONFIG_DATA)
		debug("Setup done")

	elif args.clean:
		clear_config(CONFIG_PATH)

	elif args.all:
		show_all(CONFIG_PATH)

	elif args.create:

		platform = args.platform
		contest = args.contest

		if platform == None:
			debug("Platform is not present!")
		else:

			if contest == None:
				debug("Contest Name is not present!")
			else:

				setup_contest(platform, contest)

	elif args.prob:
		contest, platform= get_recent_contest(CONFIG_PATH)
		filename = args.prob

		if platform != None and contest != None:
			# setup_contest(platform, contest)
			create_problem(platform, contest, filename)

		debug("Problem created")

	elif args.compile:
		contest,_ = get_recent_contest(CONFIG_PATH)
		compile_recent(contest)

	elif args.run:
		contest, platform = get_recent_contest(CONFIG_PATH)
		run_problem(contest, platform)

	elif args.edit:
		problem = args.edit
		set_current_problem(problem)

if __name__ == '__main__':
	main()