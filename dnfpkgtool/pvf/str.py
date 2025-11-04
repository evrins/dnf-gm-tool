from zhconv import convert


class Str:
    """处理*.str文件"""

    def __init__(self, content_text):
        self.text = convert(content_text, 'zh-cn')
        lines = filter(lambda x: '>' in x, self.text.split('\n'))
        self.strDict = {}
        for line in lines:
            key, value = line.split('>', 1)
            self.strDict[key] = value
        # print(len(self.strDict.keys()))

    def __getitem__(self, key):
        res = self.strDict.get(key)
        if res is not None:
            # print(key,res)
            return res.replace('\r', '')
        else:
            return 'None'

    def __repr__(self):
        return 'Str object. <' + str(self.strDict.items())[:100] + '...>'

    __str__ = __repr__
