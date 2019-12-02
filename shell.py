#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime
import sqlite3

data = []
con = sqlite3.connect('./sqlite.db')
cur = con.cursor()

print(cur.execute("select * from commands").fetchall())

# commands_sql = """
# CREATE TABLE commands (
#     id integer PRIMARY KEY,
# 	command text NOT NULL,
#     output text NOT NULL,
#     time text NOT NULL)
# """

# cur.execute(commands_sql)

run = True

while run:
	command = input("$ ").split(" ")
	command_str = " ".join(command)
	if command[0] == "cd":
		if len(command) > 1:
			os.chdir(command[1])
		else:
			os.chdir("/Users/pry/")
	elif command[0] == "exit":
		# print(str(data))
		print(cur.execute("select * from commands").fetchall())
		con.close()
		quit()
	else:
		now = datetime.now()
		cmd = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes, "utf-8")
		# data.append({"cmd":command_str, "output":output_str, "time":datetime.timestamp(now)})
		print(output_str.strip())
		time = datetime.timestamp(now)
		cur.execute("insert into commands (command, output, time) values (?, ?, ?)", ([command_str, output_str, time]))
		con.commit()