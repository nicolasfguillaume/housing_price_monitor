# -*- coding: utf-8 -*-
from nose.tools import eq_

import utils
from monitor import Monitor

# Best practices:
# Using a test class instead of test functions
# Specific setup and teardown functions for specific test functions
# Running only some tests (and not all of them)
# Testing that an exception was raised in a test

# docker exec -ti housingpricemonitor_worker_1 /bin/sh
# puis: nosetests

search_data = {'city': 'test', 'frequency': 5, 'browser': 'chrome', 'ratio_max': 20000, 
    'urls': {'pap': 'https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-jusqu-a-125000-euros-a-partir-de-9-m2'}}
 

def setup():
    # setup here..
    # run this function before each test
    pass


def teardown():
    # teardown here..
    # run this function after each test
    pass


def test_model_total_count():
    a = 1
    b = 1

    assert True
    # _eq_(a, b)   # same as assert but with more explicit message


def test_parser_pap():
    search = Monitor(search_data) 
    posts = search.check_posts(search_data['urls']['city'], save_to_cache_option=False)
    print(posts)

    assert True
    # nose.tools._eq_(a, b)


