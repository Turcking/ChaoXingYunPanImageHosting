#! /usr/bin/env python3

import http.server as __http_server

class ChaoXingYunPanImageHostingRequestHandler(__http_server.BaseHTTPRequestHandler):
	def do_GET(self):
		import urllib.parse

		fileInfo = self.server.chaoXingYunPan.getFileInfo(urllib.parse.unquote(self.path))
		if fileInfo is not None and fileInfo["type"] == 1:
			self.send_response(302)
			self.send_header("Location", fileInfo["preview"])
			self.end_headers()
		else:
			self.send_response(404)
			self.end_headers()

