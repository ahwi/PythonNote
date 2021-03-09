from random import randrange

from tombola import Tombola


@Tombola.register
class TomboList(list):

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend  # Tombolist.load与list.extend一样 

    def loaded(self): # loaded方法不能采用load方法的那种方式，因为list类型没有实现loaded方法所需的__bool__方法。而内置的bool函数不需要__bool__方法，因为它还可以使用__len__方法
        return bool(self) 
    
    def inspect(self):
        return tuple(sorted(self))

# Tombola.register