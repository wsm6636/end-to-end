import stt.scheduler as s

s1 = s.Scheduler("s1", [], True)


def test_simplify():
    ret = s1.simplify([])
    assert (ret == [])
    ret = s1.simplify([.1])
    assert (ret == [(0, 0)])
    ret = s1.simplify([.1, .2])
    assert (ret == [(0, 1)])
    ret = s1.simplify([.1, .3])
    assert (ret == [(0, 0), (1, 1)])
    ret = s1.simplify([.1, .2, .3, .5])
    assert (ret == [(0, 2), (3, 3)])
