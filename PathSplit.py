#! /usr/bin/env python3

class PathSplit:
	def pathSplit(path):
		import os.path

		path = os.path.normpath("/" + os.path.relpath("/" + path, "/"))
		splitedPath = []

		while path != "":
			if path[-1] == "/":
				path = path[:-1]

			head, tail = os.path.split(path)
			if tail != "":
				splitedPath.insert(0, tail)
			path = head
		if path == "":
			return splitedPath

