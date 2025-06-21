import unittest
import egg_interpreter


class TestEggInterpreter(unittest.TestCase):

    def setUp(self):
        # Reset global_env, arrays, functions before each test
        egg_interpreter.global_env.clear()
        egg_interpreter.arrays.clear()
        egg_interpreter.functions.clear()
        egg_interpreter.call_stack.clear()

    # Existing tests with slight cleanup
    def test_eval_expr_literals(self):
        self.assertEqual(egg_interpreter.eval_expr("10"), 10)
        self.assertEqual(egg_interpreter.eval_expr("5 crack 7"), 12)  # 5 + 7
        self.assertEqual(egg_interpreter.eval_expr("8 scramble 3"), 5)  # 8 - 3

    def test_eval_expr_variable(self):
        egg_interpreter.global_env['x'] = 42
        self.assertEqual(egg_interpreter.eval_expr("x"), 42)

    def test_carton_fill_and_access(self):
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

    # New tests added below

    def test_yolk_assignment_and_eval(self):
        egg_interpreter.yolk('a', 7)
        self.assertEqual(egg_interpreter.eval_expr('a'), 7)
        egg_interpreter.yolk('b', 'hello')
        self.assertEqual(egg_interpreter.eval_expr('"hello"'), 'hello')
        self.assertEqual(egg_interpreter.eval_expr('b'), 'hello')

    def test_eval_expr_array_access(self):
        egg_interpreter.arrays['carton'] = [5, 10, 15]
        self.assertEqual(egg_interpreter.eval_expr('carton at 1'), 10)

    def test_eval_expr_function_call_len(self):
        egg_interpreter.yolk('text', 'testing')
        self.assertEqual(egg_interpreter.eval_expr('len(text)'), 7)

    def test_eval_expr_function_call_random(self):
        # Just test it returns an int in range
        val = egg_interpreter.eval_expr('random(1,3)')
        self.assertIn(val, [1, 2, 3])

    def test_boil_comparisons(self):
        egg_interpreter.yolk('x', 10)
        egg_interpreter.boil('x', '>', '5', 'check')
        self.assertTrue(egg_interpreter.current_env().get('check'))
        egg_interpreter.boil('x', '==', '10', 'check_eq')
        self.assertTrue(egg_interpreter.current_env().get('check_eq'))
        egg_interpreter.boil('x', '<', '5', 'check_lt')
        self.assertFalse(egg_interpreter.current_env().get('check_lt'))

    def test_hatch_output_string_and_var(self):
        import io
        import sys
        egg_interpreter.yolk('msg', 'hello world')
        captured_output = io.StringIO()
        sys.stdout = captured_output
        egg_interpreter.hatch('"a literal string"')
        egg_interpreter.hatch('msg')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip().split('\n')
        self.assertEqual(output[0], 'a literal string')
        self.assertEqual(output[1], 'hello world')

    def test_handle_if_block_true_and_false(self):
        code_true = [
            "if 1",
            "hatch \"true branch\"",
            "else",
            "hatch \"false branch\"",
            "endif"
        ]
        code_false = [
            "if 0",
            "hatch \"true branch\"",
            "else",
            "hatch \"false branch\"",
            "endif"
        ]

        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # True condition: should print true branch only
        egg_interpreter.run_egglang('\n'.join(code_true))
        output_true = captured_output.getvalue().strip().split('\n')

        captured_output.truncate(0)
        captured_output.seek(0)

        # False condition: should print false branch only
        egg_interpreter.run_egglang('\n'.join(code_false))
        output_false = captured_output.getvalue().strip().split('\n')

        sys.stdout = sys.__stdout__

        self.assertIn('true branch', output_true)
        self.assertNotIn('false branch', output_true)
        self.assertIn('false branch', output_false)
        self.assertNotIn('true branch', output_false)

    def test_shellmatch_basic(self):
        code = [
            "yolk choice = \"apple\"",
            "shellmatch choice",
            "case \"apple\":",
            "hatch \"fruit is apple\"",
            "case \"banana\":",
            "hatch \"fruit is banana\"",
            "default:",
            "hatch \"fruit unknown\"",
            "endshell"
        ]
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        egg_interpreter.run_egglang('\n'.join(code))
        output = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__

        self.assertIn("fruit is apple", output)

    def test_function_def_and_call(self):
        code = [
            "fun greet",
            "hatch \"Hello from function\"",
            "lay",
            "crackup greet"
        ]
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        egg_interpreter.run_egglang('\n'.join(code))
        output = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__

        self.assertIn("Hello from function", output)


if __name__ == '__main__':
    unittest.main()
