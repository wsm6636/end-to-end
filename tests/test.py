import stt.task as t
import stt.scheduler as scheduler
import stt.generator_marco as gm


def assert_files(in_path, out_path):
    # with open(in_path, 'r') f1:
    #     with open(out_path, 'r') f2:
    #         for line1, line2  in zip(f1, f2):
    #             assert(line1 == line2)
    pass


def test_simplify():
    res = scheduler.simplify([0.1, 0.2, 0.3, 0.5], 0.1)
    assert(res == [(0, 2), (3, 3)])

def test_task_const():
    t1 = t.Task("t1", 0, 3, 3, 7, 10)
    assert (t1.id is "t1")

print(generate_taskset(10, 1, 1, 100, 70, 1, 100))


