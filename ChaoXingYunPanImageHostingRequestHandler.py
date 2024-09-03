#! /usr/bin/env python3

import http.server as __http_server

class ChaoXingYunPanImageHostingRequestHandler(__http_server.BaseHTTPRequestHandler):
	def do_GET(self):
		import urllib.parse

		fileInfo = self.server.chaoXingYunPan.getFileInfo(urllib.parse.unquote(self.path))
		if fileInfo is not None and fileInfo["type"] == 1:
			# For file
			if fileInfo["preview"] != "":
				res = self.server.chaoXingYunPan.session.get(fileInfo["preview"], allow_redirects=True)
				res.close()
				self.send_response(200)
				self.end_headers()
				self.wfile.write(res.content)
			else:
				self.send_response(422)  # Return 422 if no preview
				self.end_headers()
		else:
			self.send_response(404)  # Return 404 if file not found or is directory
			self.end_headers()

