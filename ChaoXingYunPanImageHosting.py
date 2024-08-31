#! /usr/bin/env python3

import ChaoXingYunPanImageHostingHTTPServer

if __name__ == "__main__":
	import json, sys
	import argparse

	config = {}
	try:
		fp = open("config.json", "rt")
		config.update(json.loads(fp.read()))
		fp.close()
	except FileNotFoundError:
		pass
	except JSONDecodeError:
		sys.stderr.write("JSON Decode Error\n")
		fp.close()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--uname", help="User name")
	parser.add_argument("-p", "--password", help="User password")
	parser.add_argument("-H", "--host", help="Bind address, default \"0.0.0.0\"")
	parser.add_argument("-P", "--port", help="Bind port, default 8080")
	parser.add_argument("-U", "--user-agent", help="User Agent, default none")
	args = vars(parser.parse_args())
	if hasattr(args, "uname") and args.uname:
		config["uname"] = args.uname
	if "uname" not in config:
		sys.stderr.write("uname is not set\n")
		sys.exit(0)

	if "password" in args and args["password"]:
		config["password"] = args["password"]
	if "password" not in config:
		sys.stderr.write("password is not set\n")
		sys.exit(0)

	if "host" in args and args["host"]:
		config["host"] = args["host"]
	if "host" not in config:
		config["host"] = "0.0.0.0"

	if "port" in args and args["port"]:
		config["port"] = args["port"]
	if "port" not in config:
		config["port"] = 8080

	if "user-agent" in args and args["user-agent"]:
		config["user-agent"] = args["user-agent"]
	if "user-agent" not in config:
		config["user-agent"] = ""

	chaoXingYunPanImageHostingHTTPServer = ChaoXingYunPanImageHostingHTTPServer.ChaoXingYunPanImageHostingHTTPServer(config)
	chaoXingYunPanImageHostingHTTPServer.serve_forever()

