import numpy
import unreal_engine as ue
class h:
    def begin_play(self):
        self.uobject.get_owner().bind_event('calculateSet',self.he)
    def he(self):
        print(numpy.__version__)
# print(sys.executable)
print("hello")