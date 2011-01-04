from piston.emitters import Emitter
from duct_tape.emitters import CSVEmitter

Emitter.register('csv', CSVEmitter, 'text/csv; charset=utf-8')

