from urllib import request, parse, error
import json


class NeteaseCloudMusic():
    def __init__(self, header=None, proxy=None):
        if proxy is None:
            self.proxy = {}
        if header:
            self.header = header
        else:
            self.header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                "Host": "music.163.com",
            }
        self.proxy_handler = request.ProxyHandler(self.proxy)
        self.opener = request.build_opener(self.proxy_handler)
        request.install_opener(self.opener)

    def search(self, name_str, *, offset=0, limit=5):
        _src_base_url = "http://music.163.com/api/search/get/web?csrf_token="
        _data = {
            "s": name_str,
        }
        _data_cache = parse.urlencode(_data)
        _full_url = _src_base_url + "hlpretag=&hlposttag=&" + _data_cache + f"&type=1&offset={offset}&total=true&limit={limit}"
        _req = request.Request(_full_url, headers=self.header)
        try:
            rs = request.urlopen(_req)
        except error.URLError as e:
            print(type(e))
            raise error.URLError(e.reason)
        else:
            _rs_json = json.loads(rs.read())
            if "abroad" in _rs_json:
                raise error.URLError("Data Encrypted, Check Your IP Address, Search function is only available for China for now")
            else:
                song_iter = _rs_json["result"]["songs"]
        return song_iter

    def lyrics(self, sid):
        _lyrics_base_url = "http://music.163.com/api/song/media"
        _data = {
            "id": sid,
        }
        _data_cache = parse.urlencode(_data)
        _full_url = _lyrics_base_url + "?" + _data_cache
        req = request.Request(_full_url, headers=self.header)
        try:
            rs = request.urlopen(req)
        except error.URLError as e:
            raise error.URLError(e.reason)
        else:
            _rs_json = json.loads(rs.read())
            if "lyric" in _rs_json:
                _lyrics_ori = _rs_json["lyric"]
                _lyrics = self.__lyric_process(_lyrics_ori)
            else:
                _lyrics = "Not Found"
        return _lyrics

    def song(self, sid):
        _base_url = "http://www.hjmin.com/song/url"
        _data = {
            "id": sid,
        }
        _data_cache = parse.urlencode(_data)
        _full_url = _base_url + "?" + _data_cache
        req = request.Request(_full_url, headers=self.header)
        try:
            rs = request.urlopen(req)
        except error.URLError as e:
            raise error.URLError(e.reason)
        else:
            _song_url = self.__song_url_process(rs)
            if not _song_url:
                raise TypeError("Request Not Found")
        return _song_url

    @staticmethod
    def __lyric_process(content):
        _lyrics_list = content.split("\n")
        _lyrics_string = ""
        for i in _lyrics_list:
            if "by:" in i or i == "\n": continue
            if "]" in i: index = i.index("]")
            else: index = 0
            _lyrics_string += i[index+1:]
            _lyrics_string += "\n"
        return _lyrics_string

    @staticmethod
    def __song_url_process(content):
        _song_json = json.loads(content.read())
        if "data" not in _song_json:
            return None
        _song_url = _song_json["data"][0]["url"]
        return _song_url
