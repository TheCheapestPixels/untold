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
choice_test_story = \
{'start_node': 'start',
 'story': [{'id': 'start',
            'scene': {'presentation': {'text': 'Start node'},
                      'autoact': {'goto': 'loop',
                                  'set': [{'var': 'counter',
                                          'val': 1,
                                           },
                                          {'var': 'special_numbers',
                                           'val': {'op': 'select-m-from-set',
                                                   'varl': 3,
                                                   'varr': [1, 2, 3, 4, 5, 6, 7, 8, 9]},
                                           }
                                          ],
                                  },
                      }
            },
           {'id': 'loop',
            'scene': {'case': [{'cond': {'op': '<',
                                         'varl': {'op': 'get',
                                                  'var': 'counter'},
                                         'varr': 10,
                                         },
                                'presentation': {'case': [{'cond': {'op': 'in',
                                                                    'varl': {'op': 'get',
                                                                             'var': 'counter'},
                                                                    'varr': {'op': 'get',
                                                                             'var': 'special_numbers'}},
                                                           'text': 'Loop node, special numbers hit.',
                                                           },
                                                          {'cond': True,
                                                           'text': 'Loop node, special numbers not hit.',
                                                           },
                                                          ],
                                                 },
                                'autoact': {'goto': 'loop',
                                            'set': {'var': 'counter',
                                                    'val': {'op': '+',
                                                            'varl': 1,
                                                            'varr': {'op': 'get',
                                                                     'var': 'counter'}},
                                                    },
                                            },
                                },
                               {'cond': True,
                                'presentation': {'text': 'End of Loop node'},
                                'autoact': {'goto': 'exit'},
                                },
                               ],
                      },
            },
           {'id': 'exit',
            'special': 'exit',
            },
           ],
 }

lab = \
{'author': '',
 'title': 'Mean Lab',
 'start_node': 'start',
 'story': [{'id': 'start',
            'scene': {'presentation': {'text': "The lab's doors slam shut behind you."},
                      'autoact': {'goto': 'room2',
                                  'set': [{'var': 'balls', 
                                           'val': {'op': 'select-m-from-set',
                                                   'varl': 3,
                                                   'varr': [1, 2, 3, 4, 5, 6, 7, 8, 9]}},
                                          {'var': 'balls_found',
                                           'val': 0}]}}},
           {'id': 'room1',
            'scene': {'presentation': {'text': "Room 1."},
                      'actables': [{'text': 'Go north',
                                    'result': {'goto': 'room4'}}]}},
           {'id': 'room2',
            'scene': {'presentation': {'text': "Room 2."},
                      'actables': [{'text': 'Go north',
                                    'result': {'goto': 'room5'}},
                                   {'text': 'Go west',
                                    'result': {'goto': 'room3'}},
                                   ]}},
           {'id': 'room3',
            'scene': {'presentation': {'text': "Room 3."},
                      'actables': [{'text': 'Go north',
                                    'result': {'goto': 'room6'}},
                                   {'text': 'Go east',
                                    'result': {'goto': 'room2'}},
                                   ]}},
           {'id': 'room4',
            'scene': {'presentation': {'text': "Room 4."},
                      'actables': [{'text': 'Go north',
                                    'result': {'goto': 'room7'}},
                                   {'text': 'Go south',
                                    'result': {'goto': 'room1'}},
                                   {'text': 'Go west',
                                    'result': {'goto': 'room5'}},
                                   ]}},
           {'id': 'room5',
            'scene': {'presentation': {'text': "Room 5."},
                      'actables': [{'text': 'Go south',
                                    'result': {'goto': 'room2'}},
                                   {'text': 'Go east',
                                    'result': {'goto': 'room4'}},
                                   {'text': 'Go west',
                                    'result': {'goto': 'room6'}},
                                   ]}},
           {'id': 'room6',
            'scene': {'presentation': {'text': "Room 6."},
                      'actables': [{'text': 'Go east',
                                    'result': {'goto': 'room5'}},
                                   {'text': 'Go south',
                                    'result': {'goto': 'room3'}},
                                   ]}},
           {'id': 'room7',
            'scene': {'presentation': {'text': "Room 7."},
                      'actables': [{'text': 'Go west',
                                    'result': {'goto': 'room8'}},
                                   {'text': 'Go south',
                                    'result': {'goto': 'room4'}},
                                   ]}},
           {'id': 'room8',
            'scene': {'presentation': {'text': "Room 8."},
                      'actables': [{'text': 'Go east',
                                    'result': {'goto': 'room7'}},
                                   {'text': 'Go west',
                                    'result': {'goto': 'room9'}},
                                   ]}},
           {'id': 'room9',
            'scene': {'presentation': {'text': "Room 9."},
                      'actables': [{'text': 'Go east',
                                    'result': {'goto': 'room8'}},
                                   ]}},
           {'id': 'end',
            'special': 'exit'}
           ],
}
#--------------------------------------------------------------------

import json

if __name__ == '__main__':
    story = lab
    f = open('story.json', 'w')
    f.write(json.dumps(story))
    f.write('\n')
    print('Wrote story.')
    f.close()

