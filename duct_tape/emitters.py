from piston.emitters import Emitter

class CSVEmitter(Emitter):
    def render(self,request):
        rows = self.construct()
        return "\n".join([
            ','.join([str(col) for col in row]) for row in rows])
#Emitter registered in duct_tape/__init__.py
