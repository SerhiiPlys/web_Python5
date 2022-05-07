import json
import pickle
from abc import abstractmethod, ABC



class SerializationInterface(ABC):
    
    @abstractmethod
    def serialize_to_file(self):
        pass


class Kls_json(SerializationInterface):

    def serialize_to_file(self):
        filename = "reserv.json"    
        with open(filename, "wb") as file: 
            json.dump(self, file)


class Kls_pickle(SerializationInterface):

    def serialize_to_file(self):
        filename = "reserv.pic"    
        with open(filename, "wb") as file: 
            pickle.dump(self, file)


class Meta(type):
    child_number = 0

    def __new__(*args, **kwargs):
        print(f'New Meta child')
        return type.__new__(*args)

    def __init__(*args, **kwargs):
        Meta.child_number += 1

 

class Cls1(metaclass=Meta):

    class_number = Meta.child_number

    def __init__(self, data):
        self.data = data

 
class Cls2(metaclass=Meta):

    class_number = Meta.child_number

    def __init__(self, data):
        self.data = data

 

assert (Cls1.class_number, Cls2.class_number) == (0, 1)

a, b = Cls1(''), Cls2('')

assert (a.class_number, b.class_number) == (0, 1)
