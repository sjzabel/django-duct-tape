from piston.emitters import Emitter
from duct_tape.api.emitters import CSVEmitter, ExtJSONEmitter

Emitter.register('csv', CSVEmitter, 'text/csv; charset=utf-8')
#Emitter.register('json', ExtJSONEmitter, 'application/json; charset=utf-8')

