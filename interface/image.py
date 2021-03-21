from interface import Element
from config import *
import os


class Image(Element):

    def __init__(self, settings):
        super().__init__(settings)
        path = gip(settings['path'])
        self.images = {i[:-4]: ldi(path + '/' + i) for i in os.listdir(path)}
        self.animation = 'idle'

    def show(self, surf):
        surf.blit(self.images[self.animation], self.position)
