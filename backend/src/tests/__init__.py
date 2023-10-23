"""Entrypoint for all backend unit tests."""
import unittest
from . import test_migration


def run_unit_tests(tests=None):
    """Запуск тестов. -t Запуск конкретных тестов"""

    if isinstance(tests, type(None)):
        tests = []

    cases_to_run = ['test_{}'.format(case) for case in tests]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    if not cases_to_run:
        for case_name, case in globals().items():
            if not case_name.startswith('test_'):
                continue
            print('case_name:', case_name)
            suite.addTests(loader.loadTestsFromModule(case))

    for case_name in cases_to_run:
        suite.addTests(
            loader.loadTestsFromModule(globals()[case_name])
        )
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
