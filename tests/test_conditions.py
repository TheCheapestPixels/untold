# TODO:
#   Invalid operator
#   Missing arguments for operator


from untold.story import eval_condition
from tests.util import run_through_story


def test_const_1():
    cond_node = {'const': True}
    state = {}
    assert eval_condition(cond_node, state)


def test_const_2():
    cond_node = {'const': False}
    state = {}
    assert not eval_condition(cond_node, state)


def test_const_3():
    cond_node = {'const': 'foo'}
    state = {}
    assert eval_condition(cond_node, state) == 'foo'


def test_const_4():
    cond_node = {'const': 1}
    state = {}
    assert eval_condition(cond_node, state) == 1


def test_var_1():
    cond_node = {'var': 'foo'}
    state = {'foo': 1}
    assert eval_condition(cond_node, state) == 1


def test_op_eq_1():
    cond_node = {'op': '==',
                 'varl': {'var': 'foo'},
                 'varr': 23}
    state = {'foo': 23}
    assert eval_condition(cond_node, state)


def test_op_eq_2():
    cond_node = {'op': '==',
                 'varl': {'var': 'foo'},
                 'varr': {'const': 23}}
    state = {'foo': 23}
    assert eval_condition(cond_node, state)


# Absence 1
def test_op_eq_3():
    cond_node = {'op': '==',
                 'varl': {'var': 'foo'},
                 'varr': {'const': None}}
    state = {}
    assert eval_condition(cond_node, state)


# Absence 2
def test_op_eq_4():
    cond_node = {'op': '==',
                 'varl': {'var': 'foo'},
                 'varr': None}
    state = {}
    assert eval_condition(cond_node, state)


def test_op_eq_5():
    cond_node = {'op': '==',
                 'varl': {'var': 'foo'},
                 'varr': {'const': None}}
    state = {'foo': 23}
    assert not eval_condition(cond_node, state)


# (foo == True) == (bar == False)
def test_nesting_1():
    cond_node= {'op': '==',
                'varl': {'op': '==',
                         'varl': {'var': 'foo'},
                         'varr': {'const': True}},
                'varr': {'op': '==',
                         'varl': {'var': 'bar'},
                         'varr': {'const': False}}}
    state = {'foo': True,
             'bar': False}
    assert eval_condition(cond_node, state)


def test_nesting_2():
    cond_node= {'op': '==',
                'varl': {'op': '==',
                         'varl': {'var': 'foo'},
                         'varr': {'const': True}},
                'varr': {'op': '==',
                         'varl': {'var': 'bar'},
                         'varr': {'const': False}}}
    state = {'foo': False,
             'bar': True}
    assert eval_condition(cond_node, state)


def test_nesting_3():
    cond_node= {'op': '==',
                'varl': {'op': '==',
                         'varl': {'var': 'foo'},
                         'varr': {'const': True}},
                'varr': {'op': '==',
                         'varl': {'var': 'bar'},
                         'varr': {'const': False}}}
    state = {'foo': True,
             'bar': True}
    assert not eval_condition(cond_node, state)


def test_story_format_1():
    story_doc = {'start_node': 'start',
                 'story': [{'id': 'start',
                            'scene': {'presentation': 'text',
                                      'autoact': {'set': {'var': 'foo',
                                                          'val': {'op': '==',
                                                                  'varl': 23,
                                                                  'varr': 23}},
                                                  'goto': 'end'}}},
                           {'id': 'end',
                            'special': 'exit'}]}
    s = run_through_story(story_doc)
    assert s.get_state_var('foo')
