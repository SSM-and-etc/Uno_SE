from uno.utils import *

def test_cycleiterator():
    it = CycleIterator([a for a in range(10)])

    assert it.current() == 0
    assert next(it) == 1
    assert it.look_next() == 2
    assert next(it) == 2
    it.reverse()
    assert next(it) == 1
    assert it.current() == 1