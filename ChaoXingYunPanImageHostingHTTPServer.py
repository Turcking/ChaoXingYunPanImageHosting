#! /usr/bin/env python3

import http.server as __http_server

class ChaoXingYunPanImageHostingHTTPServer(__http_server.ThreadingHTTPServer):
	import ChaoXingYunPan as __ChaoXingYunPan

	def __init__(self, config):
		import ChaoXingYunPanImageHostingRequestHandler
		super().__init__((config["host"], config["port"]), ChaoXingYunPanImageHostingRequestHandler.ChaoXingYunPanImageHostingRequestHandler)
		self.config = config
		self.chaoXingYunPan = self.__ChaoXingYunPan.ChaoXingYunPan(config)
		self.chaoXingYunPan.login(config["uname"], config["password"])
		self.chaoXingYunPan.initVariables()

