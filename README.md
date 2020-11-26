# Netease-Cloud-Music-Python-api

A python Netease Cloud Music api

## **Documentary**

- **api reference**
	  - class NeteaseCloudMusic(object)
			- A netease cloud music class, used for creating the instance
			- 
			- **Method**
				- Instance Method
					- def \_\_init\_\_(self, header=None, proxy=None)
						- used to init some properities, you can specify the request header and proxy server
						- return None
					- def search(self, name_str, *, offset=0, limit=5)
						- Search songs from ncm
						- **Arguments**
							- name_attr: the song name you wanna search
							- offset: the actual page number, default -> 0
							- limit: the number of result you wanna get
						- return dict -> Result (will be formatted in next version)
					- def lyrics(self, sid)
 						- Get song lyrics by using song id
						- **Arguments**
							- sid: Song id
							- return str -> formatted song lyrics
					- def song(self, sid)
						- Get song direct link (mp3 file link)
						- **Arguments**
							- sid: Song id
						- return str -> Song direct url

          
