#!/usr/bin/env python

# Node
# * id: id
# * 
#
# Story (Node)
# * story: Scene
# * actable: [Interactions]
# * autoact: {Consequences}
#
# Scene
# * text: textual description
#
# Consequences
# * set
#   * var: variable_name
#   * val: value
# * goto: Node.id
#
# Script
# * case
#   * cond
#     * Preconditions
#
# Interactions
# * text: textual description
# * result: Consequences
# * Script


import argparse
import json


test_story = {
 'author': 'TheCheapestPixels',
 'title': 'Test case',
 'start_node': 'start',
 'story': [{'id': 'start',
            'case': [{'cond': True,
                      'scene': {'text': 'Testing boolean node'},
                      'autoact': {'goto': 'test_2'},},],},
           {'id': 'test_2',
            'case': [{'cond': {'op': '==',
                               'varl': {'var': 'var1'},
                               'varr': None},
                      'scene': {'text': 'Testing var for absence'},
                      'autoact': {'goto': 'test_3',
                                  'set': {'var': 'var1',
                                          'val': 1},},},],},
           {'id': 'test_3',
            'case': [{'cond': {'op': '==',
                               'varl': {'var': 'var1'},
                               'varr': 1},
                      'scene': {'text': 'Testing var for value'},
                      'autoact': {'goto': 'test_4',},},],},
           {'id': 'test_4',
            'scene': {'case': [{'cond': {'op': '==',
                                         'varl': {'var': 'var1'},
                                         'varr': 1},
                                'text': 'Testing case-in-scene/autoact.'},
                               {'cond': True,
                                'text': 'case-in-scene/autoact failed.'},],},
            'autoact': {'case': [{'cond': {'op': '==',
                                           'varl': {'var': 'var1'},
                                           'varr': 1},
                                  'goto': 'unweighted_choice',},
                                 {'cond': True,
                                  'goto': 'broken',},],},},
           {'id': 'unweighted_choice',
            'scene': {'choice': [{'text': 'Unweighted choice chose foo'},
                                 {'text': 'Unweighted choice chose bar'},
                                 {'text': 'Unweighted choice chose baz'},],},
            'autoact': {'goto': 'weighted_choice'},},
           {'id': 'weighted_choice',
            'choice': [{'weight': 1,
                        'scene': {'text': 'Weighted choice chose foo'},
                        'autoact': {'goto': 'done'},},
                       {'weight': 2,
                        'scene': {'text': 'Weighted choice chose bar'},
                        'autoact': {'goto': 'done'},},
                       {'weight': 3,
                        'scene': {'text': 'Weighted choice chose baz'},
                        'autoact': {'goto': 'done'},},],},
           {'id': 'done',
            'special': 'exit',},],}

# FIXME: This is broken right now.
battle_story = {
 'author': 'TheCheapestPixels',
 'title': 'After the Storm',
 'start_node': 'start',
 'story': [{'id': 'start',
            'scene': {'text': 'As the clouds finally part, the sun reveals this morning\'s vibrant green of the rolling hills to be buried under the blood and body parts of the battlefield.',
                     },
            'autoact': {'goto': 'field',
                       },
           },
           {'id': 'field',
            'case': [{'cond': {'var': 'warrior_on_field',
                               'val': None,
                              },
                      'scene': {'text': 'A fallen warrior lies face-down on the ground.',
                               },
                      'actable': [{'text': 'Search warrior',
                                   'result': {'goto': 'field',
                                              'set': {'var': 'warrior_on_field',
                                                      'val': 'examined',
                                                     },
                                             },
                                  },
                                  {'text': 'Leave battlefield',
                                   'result': {'goto': 'forest'}
                                  },
                                 ],
                     },
                     {'cond': {'var': 'warrior_on_field',
                               'val': 'examined',
                              },
                      'scene': {'text': 'The fallen warrior stares blankly into the sky, an amulet on his chest glittering in the sunlight.',
                               },
                      'actable': [{'text': 'Take amulet',
                                   'result': {'goto': 'field',
                                              'set': {'var': 'warrior_on_field',
                                                      'val': 'plundered',
                                                     },
                                             },
                                  },
                                  {'text': 'Leave battlefield',
                                   'result': {'goto': 'forest'}
                                  },
                                 ]
                     },
                     {'cond': {'var': 'warrior_on_field',
                               'val': 'plundered'},
                      'scene': {'text': 'The fallen warrior that you have looted stares blankly into the sky, beyond accusation.',
                               },
                      'actable': [{'text': 'Leave battlefield',
                                   'result': {'goto': 'forest'}
                                  },
                                 ],
                     },
                    ],
           },
           {'id': 'forest',
            'scene': {'text': 'A well-trodden path stretches between dense trees under a dark canopy. In the distance, a villager gathers firewood.',
                     },
            'actable': [{'text': 'Away from the battlefield.',
                         'result': {'goto': 'villager'
                                   },
                        },
                        {'text': 'Towards the battlefield.',
                         'result': {'goto': 'field'},
                        },
                       ],
           },
           {'id': 'villager',
            'case': [{'cond': {'var': 'warrior_on_field',
                               'val': 'plundered'},
                      'scene': {'text': 'The old woman interrupts her work and turns around to greet you, a tired smile on her face, but as soon as she sees the dead soldier\'s amulet on your chest, she breaks into tears.'},
                     },
                     {'cond': True,
                      'scene': {'text': 'The old woman interrupts her work and turns around, a tired smile on her face. "Hello young man, what brings you this way?"' },
                      'actable': [{'text': 'Nothing.',
                                   'result': {'goto': 'roll_credits'}, # FIXME
                                  },
                                  {'text': 'I bring news from the battlefield.',
                                   'result': {'goto': 'forest'}, # FIXME
                                   'if': {'var': 'warrior_on_field',# FIXME
                                          'val': 'examined'}
                                  },
                                 ],
                     },
                    ],
           },
           {'id': 'roll_credits',
            'special': 'exit'},
          ],
}

new_story_format_story = {
    'author': 'TheCheapestPixels',
    'title': 'Labyrinth of foobarbaz',
    'start_node': 'start',
    'story': [{'id': 'start',
               'scene': {'presentation': {'text': 'This is the anteroom. There are three doors.'},
                         'actables': [{'text': 'Door foo',
                                       'result': {'goto': 'foo'}},
                                      {'text': 'Door bar',
                                       'result': {'goto': 'bar'}},
                                      {'text': 'Door baz',
                                       'result': {'goto': 'baz'}},
                                      ]}},
              {'id': 'foo',
               'scene': {'presentation': {'text': 'This is room foo. There are three doors'},
                         'actables': [{'text': 'Door bar',
                                       'result': {'goto': 'bar'}},
                                      {'text': 'Door baz',
                                       'result': {'goto': 'baz'}},
                                      {'text': 'Door exit',
                                       'result': {'goto': 'exit'}},
                                      ]}},
              {'id': 'bar',
               'scene': {'presentation': {'text': 'This is room bar. There are three doors'},
                         'actables': [{'text': 'Door foo',
                                       'result': {'goto': 'foo'}},
                                      {'text': 'Door baz',
                                       'result': {'goto': 'baz'}},
                                      {'text': 'Door exit',
                                       'result': {'goto': 'exit'}},
                                      ]}},
              {'id': 'baz',
               'scene': {'presentation': {'text': 'This is room baz. There are three doors'},
                         'actables': [{'text': 'Door foo',
                                       'result': {'goto': 'foo'}},
                                      {'text': 'Door bar',
                                       'result': {'goto': 'bar'}},
                                      {'text': 'Door exit',
                                       'result': {'goto': 'exit'}},
                                      ]}},
              {'id': 'exit',
               'special': 'exit'}]}
#--------------------------------------------------------------------
choice_test_story = {'start_node': 'start',
                     'story': [{'id': 'start',
                                'scene': {'presentation': {'text': 'Start node'},
                                          'autoact': {'goto': 'loop',
                                                      'set': {'var': 'counter',
                                                              'val': 0,
                                                              },
                                                      },
                                          }
                                },
                               {'id': 'loop',
                                'scene': {'case': [{'cond': {'op': '==',
                                                             'varl': {'var': 'counter'},
                                                             'varr': 0,
                                                             },
                                                    'presentation': {'text': 'Loop node'},
                                                    'autoact': {'goto': 'loop',
                                                                'set': {'var': 'counter',
                                                                        'val': 5,
                                                                        },
                                                                },
                                                    },
                                                   {'cond': {'op': '==',
                                                             'varl': {'var': 'counter'},
                                                             'varr': 5,
                                                             },
                                                    'presentation': {'text': 'End of Loop node'},
                                                    'autoact': {'goto': 'exit'},
                                                    },
                                                   ],
                                          },
                                },
                               {'id': 'exit',
                                'special': 'exit',
                                }],
                     }
#--------------------------------------------------------------------

if __name__ == '__main__':
    stories = {
        'test': test_story,
        'battle': battle_story,
        'newformat': new_story_format_story,
        'choicetest': choice_test_story,
    }
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'stories',
        type=str,
        nargs='+',
        help='Stories to write. At least one of: test, battle, newformat, choicetest',
    )
    args = parser.parse_args()

    for story_name in args.stories:
        if story_name not in stories:
            print("\"{}\" is not a known story!".format(story_name))
            continue
        story = stories[story_name]
        f = open('{}.json'.format(story_name), 'w')
        f.write(json.dumps(story))
        f.write('\n')
        print("Wrote story \"{}\".".format(story_name))
        f.close()
