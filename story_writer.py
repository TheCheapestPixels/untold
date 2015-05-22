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

case_test = [
 {'id': 'start',
  'case': [{'cond': True,
            'scene': {'text': 'Testing boolean node'},
            'autoact': {'goto': 'test_2'},
           },
          ],
 },
 {'id': 'test_2',
  'case': [{'cond': {'var': 'var1',
                     'val': None},
            'scene': {'text': 'Testing var for absence'},
            'autoact': {'goto': 'test_3',
                        'set': {'var': 'var1',
                                'val': 1},
                       },
           },
          ],
 },
 {'id': 'test_3',
  'case': [{'cond': {'var': 'var1',
                     'val': 1},
            'scene': {'text': 'Testing var for value'},
            'autoact': {'goto': 'test_4',
                       },
           },
          ],
 },
 {'id': 'test_4',
  'scene': {'case': [{'cond': {'var': 'var1',
                               'val': 1,
                              },
                      'text': 'Testing case-in-scene/autoact.'
                     },
                     {'cond': True,
                      'text': 'case-in-scene/autoact failed.'
                     },
                    ],
           },
  'autoact': {'case': [{'cond': {'var': 'var1',
                                 'val': 1,
                                },
                        'goto': 'done',
                       },
                       {'cond': True,
                        'goto': 'broken',
                       },
                      ],
             },
 },
 {'id': 'done',
  'special': 'exit',
 }
 ]

battle_story = [
{'id': 'start',
 'scene': {'text': 'As the clouds finally part, the sun reveals this mornings vibrant green of the rolling hills to be buried under the blood and body parts of the battlefield.',
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
           'scene': {'text': 'The old woman interrupts her work and turns around to greet you, a tired smile on her face, but as soon as she sees the dead soldiers amulet on your chest, she breaks into tears.'},
          },
          {'cond': 'else',
           'scene': {'text': 'The old woman interrupts her work and turns around, a tired smile on her face. "Hello, young man, what brings you this way?"' },
           'actable': [{'text': 'Nothing.',
                        'result': {'goto': 'forest'},
                       },
                       {'text': 'I bring news from the battlefield.',
                        'result': {'goto': 'forest'},
                        'if': {'var': 'warrior_on_field',# FIXME
                               'val': 'examined'}
                       },
                      ]
          },
         ],
},
]

# FIXME
# 'cond': 'else'
# 'actable' is a Script

#--------------------------------------------------------------------
import json

story = case_test

f = open('story.json', 'w')
for story_node in story:
    f.write(json.dumps(story_node))
    f.write('\n')
    print('Wrote node %s' % (story_node['id'], ))
f.close()

