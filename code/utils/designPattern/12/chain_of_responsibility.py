from abc import ABCMeta, abstractmethod


class Subject(metaclass=ABCMeta):
    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def set_content(self):
        pass


class RealSubject(Subject):
    def __init__(self, filename):
        self.filename = filename
        f = open(filename, 'r')
        self.content = f.read()
        f.close()

    def get_content(self):
        return self.content

    def set_content(self, content):
        f = open(self.filename, 'w')
        f.write(content)
        f.close()


# subj = RealSubject('test.txt')
# subj.get_content()


"""
虚代理：在读取的时候才去打开文件
"""
class VirtualProxy(Subject):
    def __init__(self, filename):
        self.filename = filename
        self.subj = None

    def get_content(self):
        if not self.subj:
            self.subj = RealSubject(self.filename)
        return self.subj.get_content()

    def set_content(self):
        if not self.subj:
            self.subj = RealSubject(self.filename)
        return self.subj.set_content()


"""
保护代理
"""
class ProtectedProxy(Subject):
    def __init__(self, filename):
        self.subj = RealSubject(filename)
    
    def get_content(self):
        return self.subj.get_content()

    def set_content(self, content):
        raise PermissionError("无写入权限")



