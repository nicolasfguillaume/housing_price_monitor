# -*- coding: utf-8 -*-
import utils

# Best practices:
# Using a test class instead of test functions
# Specific setup and teardown functions for specific test functions
# Running only some tests (and not all of them)
# Testing that an exception was raised in a test

def setup():
    # setup here..
    # run this function before each test
    pass


def teardown():
    # teardown here..
    # run this function after each test
    pass


def test_model_total_count():
    m = model.Model()
    assert m.total_count() == 0

    m.incr_gram_count(('h',))
    m.incr_gram_count(('e',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('o',))

    assert m.total_count() == (5 + 4)
    assert m.total_count(include_smoothing=False) == 5
    # nose.tools._eq_(a, b)   # same as assert but with more explicit message