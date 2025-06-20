import unittest
import egg_interpreter

class TestEggInterpreter(unittest.TestCase):

    def test_eval_expr_literals(self):
        self.assertEqual(egg_interpreter.eval_expr("10"), 10)
        self.assertEqual(egg_interpreter.eval_expr("5 crack 7"), 12)  # 5 + 7
        self.assertEqual(egg_interpreter.eval_expr("8 scramble 3"), 5)  # 8 - 3

    def test_eval_expr_variable(self):
        egg_interpreter.global_env['x'] = 42
        self.assertEqual(egg_interpreter.eval_expr("x"), 42)

    def test_carton_fill_and_access(self):
        egg_interpreter.arrays.clear()
        egg_interpreter.arrays['nest'] = [0, 0, 0]
        egg_interpreter.fill_carton('nest', 0, 10)
        val = egg_interpreter.get_carton_value('nest', 0)
        self.assertEqual(val, 10)

    def test_eggtools_len(self):
        self.assertEqual(egg_interpreter.eggtools_call('len', ['hello']), 5)
        self.assertEqual(egg_interpreter.eggtools_call('len', [[1, 2, 3]]), 3)

    def test_eggtools_random(self):
        for _ in range(10):
            r = egg_interpreter.eggtools_call('random', [1, 5])
            self.assertTrue(1 <= r <= 5)

    def test_eggtools_eggtime(self):
        t = egg_interpreter.eggtools_call('eggtime', [])
        self.assertTrue(isinstance(t, str) and len(t) > 0)

if __name__ == '__main__':
    unittest.main()
