#! /usr/bin/env python3

class ChaoXingYunPan:
	import requests as __requests

	def encryptByAES(data, key):
		"""
		Encrypt data with key by AES, data and key all bytes.
		"""
		import base64
		import Crypto.Cipher.AES
		import Crypto.Util.Padding

		if not isinstance(data, bytes):
			data = data.encode()
		if not isinstance(key, bytes):
			key = key.encode()

		padded = Crypto.Util.Padding.pad(data, Crypto.Cipher.AES.block_size, "pkcs7")
		aesCipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv=key)
		encrypted = aesCipher.encrypt(padded)
		base64ed = base64.b64encode(encrypted)
		return base64ed

	def login(self, uname, password):
		"""
		Please run initVariables() after login.
		"""
		key = "u2oh6Vu^HWe4_AES"

		self.session.post("https://passport2.chaoxing.com/fanyalogin", data={
			"fid": "-1",
			"uname": ChaoXingYunPan.encryptByAES(uname, key),
			"password": ChaoXingYunPan.encryptByAES(password, key),
			"refer": "https://i.chaoxing.com",
			"t": "true",
			"forbidotherlogin": "0",
			"validate": "",
			"doubleFactorLogin": "0",
			"independentId": "0",
			"independentNameId": "0"
			}).close()

	def initVariables(self):
		import re
		import bs4

		response = self.session.get("https://i.chaoxing.com/")
		response.close()
		soup = bs4.BeautifulSoup(response.content.decode("utf-8"), "html.parser")
		yunpanUrl = soup.select("a[name=\"云盘\"]")[0]["dataurl"]

		response = self.session.get(yunpanUrl)
		response.close()
		rootDirSearchResult = re.search("rootdir = \"(.*?)\"", response.content.decode())
		self.__rootDir = rootDirSearchResult.groups()[-1]
		currentPuidSearchResult = re.search("currentPuid = \"(.*?)\"", response.content.decode())
		self.__currentPuid = currentPuidSearchResult.groups()[-1]
		encstrSearchResult = re.search("encstr = \"(.*?)\"", response.content.decode())
		self.__encstr = encstrSearchResult.groups()[-1]

	def getFileInfo(self, path="/", cacheReuseSeconds=30):
		"""
		Return `path` info, or None if file not found.
		Re-request if the cache time exceeded `cacheReuseSeconds`.
		"""
		import time
		import PathSplit

		if not isinstance(path, list):
			path = PathSplit.PathSplit.pathSplit(path)

		# Update root directory
		if time.time() - self.pathInfoCache["cacheTime"] > cacheReuseSeconds:
			self.pathInfoCache["list"] = self.fetchDirectoryInfo()
			self.pathInfoCache["cacheTime"] = time.time()

		targetFile = self.pathInfoCache
		for i in path:
			for j in targetFile["list"]:
				if j["name"] == i:
					if j["type"] == 2 and time.time() - j["cacheTime"] > cacheReuseSeconds:
						j["list"] = self.fetchDirectoryInfo(j["id"])
					targetFile = j
					break
			else:
				return None
		return targetFile

	def fetchDirectoryInfo(self, fileId=0):
		response = self.session.get("https://pan-yz.cldisk.com/opt/listres", params={
			"enc": self.__encstr,
			"parentId": fileId
			})
		response.close()
		responseJson = response.json()
		files = []
		for i in responseJson["list"]:
			file = {
					"type": i["type"],
					"name": i["name"],
					"id": i["id"],
					"cacheTime": 0,
					"preview": i["preview"]
					}
			files.append(file)
		return files

	def __init__(self, config):
		self.session = self.__requests.session()
		self.session.headers["User-Agent"] = config["user-agent"]

		self.pathInfoCache = {
				"cacheTime": 0,
				"type": 2,
				"fileId": 0,
				"list": []
				}

