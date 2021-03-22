from interface import Element


class TabWidget(Element):

    def __init__(self, settings):
        super().__init__(settings)
        self.base = settings['base']
        self.tabs = settings['tabs']
        self.tab = 'login'

    def change_tab(self, name):
        self.tab = name

    def get_elements(self):
        return list(self.base.values()) + list(self.tabs[self.tab].values())

    def get(self, name):
        for tab in list(self.tabs.keys()):
            if name in self.tabs[tab]:
                return self.tabs[tab][name]

    def mouse_down(self, pos):
        [i.mouse_down(pos) for i in self.get_elements()]

    def mouse_motion(self, pos):
        [i.mouse_motion(pos) for i in self.get_elements()]

    def key_down(self, key):
        [i.key_down(key) for i in self.get_elements()]

    def show(self, surf):
        [i.show(surf) for i in self.get_elements()]
