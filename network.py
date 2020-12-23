import requests


class Network:

    def __init__(self):
        self.path = 'https://serene-harbor-23068.herokuapp.com/'

    def get(self):
        test = requests.get(self.path + '?mode=read')
        return test.text[:-2]

    def send(self, value):
        requests.get(self.path + '?mode=write&data=' + value)
