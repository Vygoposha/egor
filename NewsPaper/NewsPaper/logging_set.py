class LevelFilter(object):

    def __init__(self, level):
        self.level_name = level

    def filter(self, record) -> bool:
        # print(record.levelname)
        # print(self.level_name)
        # print(record.levelname == self.level_name)
        return record.levelname == self.level_name
