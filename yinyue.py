"""爬去百度音乐"""

import requests
from fake_useragent import UserAgent
import pprint
import os
class Music:
    def __init__(self):
        self.url1 = 'http://music.taihe.com/artist'
        self.url = 'http://play.taihe.com/data/music/songlink'
        self.data = {
            'songIds': '242078437,100575177',
            'hq': '0',
            'type': 'm4a, mp3',
            'rate': '',
            'pt': '0',
            'flag': '-1',
            's2p': '-1',
            'prerate': '-1',
            'bwt': '-1',
            'dur': '-1',
            'bat': '-1',
            'bp': '-1',
            'pos': '-1',
            'auto': '-1',
        }
        self.headers = {'User-Agent':UserAgent().random}
        name = input('请输入歌手姓名：')
    def post_music(self):
        reponse = requests.post(url=self.url,data=self.data,headers=self.headers).json()
        pprint.pprint(reponse['data']['songList'])
        musics = reponse['data']['songList']
        music_names = []
        music_urls = []
        for music in musics:
            music_name = music['songName']
            music_url = music['songLink']
            # music_names.append(music_name)
            # music_urls.append(music_url)
            self.get_music(music_url,music_name)
    def get_music(self,music_url,music_name):
        reponse = requests.get(url=music_url).content
        filename = './music/'
        if not os.path.exists(filename):
            os.makedirs(filename)
        filename =filename + '{}.mp4'.format(music_name)
        with open(filename,'wb') as f:
            f.write(reponse)

    def run(self):
        self.post_music()

Music().run()



