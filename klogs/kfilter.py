from abc import ABC, abstractmethod


class kFilter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def filter(self, msg):
        pass

class kWordFilter(kFilter):
    def __init__(self, exclude : str):
        self.exclude = exclude

    def filter(self, msg):
        if self.exclude in msg:
            return True
        else:
            return False
