class MyList(object):

    def __init__(self):
        self.__list = list()
        self.working = 0

    def __len__(self):
        return len(self.__list) + self.working

    def __getitem__(self, i):
        return self.__list[i]

    def __iter__(self):
        return self.__list.__iter__()

    def add(self, elem):
        if elem in self.__list:
            return False
        self.__list.append(elem)
        print(elem, 'added')
        return True

    def remove(self, i):
        print(self.__list.pop(i),'removed')

    # FIFO
    def get(self):
        if len(self.__list):
            self.working += 1
            return self.__list.pop()
        return None

    def clear(self):
        self.__list = list()

    def done(self):
        self.working -= 1
        if self.working < 0:
            self.working = 0

    def __str__(self):
        return repr(self.__list)