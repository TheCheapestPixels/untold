# TODO:
#   De-/Serialization of stories and state should not be in Story.

import json
import yaml
from pprint import pprint

from .conditions import eval_condition
from .scripting import eval_script_node, eval_list_node


# Scene nodes --------------------------------------------------------


# FIXME: What does eval_script_node return when the resulting element is empty?
def eval_scene_node(node, state):
    # FIXME: What to do about this debugging code?
    # print("|| Node before scene script evaluation")
    # pprint(node['scene'])
    scene_node = eval_script_node(node['scene'], state)
    # print("|| Node after scene script evaluation")
    # pprint(scene_node)
    result_node = {}
    if 'presentation' in scene_node.keys():
        # FIXME: Presentation evaluation here.
        presentation = eval_script_node(scene_node['presentation'], state)
        result_node['presentation'] = presentation
    if 'actables' in scene_node.keys():
        actables = eval_script_node(
            eval_list_node(scene_node['actables'], state),
            state,
        )
        # FIXME: Presentation evaluation here, too.
        result_node['actables'] = actables
    if 'autoact' in scene_node.keys():
        autoact = eval_script_node(scene_node['autoact'], state)
        result_node['autoact'] = autoact
    # FIXME: Check validity of result_node for mandatory fields.
    return result_node


# Story nodes --------------------------------------------------------


class StoryExited(Exception):
    pass


class NodeNotEvaluatable(Exception):
    def __init__(self, node):
        self.node = node
    def __str__(self):
        return repr(self.node)


def eval_special_node(node, state):
    if node['special'] == 'exit':
        raise StoryExited


node_funcs = {
    'scene': eval_scene_node,
    'special': eval_special_node,
}


# Check the node's keywords against the functions that handle nodes
# with those keywords. Actually, one matching function will be chosen
# at pseudo-random (order of hashing) and its result will be
# returned. Thus each story node should have only exactly one keyword
# that is applicable here.
def eval_story_node(node, state):
    node = eval_script_node(node, state)
    node_func_keys = node_funcs.keys()
    for key in node.keys():
        if key in node_func_keys:
            return node_funcs[key](node, state)
    # Raise exception, as there is no function to handle this node.
    raise NodeNotEvaluatable(node)


# Story management ---------------------------------------------------


class NoSuchMetadata(Exception):
    pass


class Story:
    def __init__(self, story_doc = 'story.json'):
        if type(story_doc) == str:
            self.load(story_doc)
        elif type(story_doc) == dict:
            self.document = story_doc
        else:
            # FIXME: Beautify this.
            # No valid document reference has been provided.
            raise Exception
        # FIXME: Wrap this in a try block, as stories may be malformed.
        self.story = {node['id']: node for node in self.document['story']}

    def load(self, filename = 'story.json'):
        """Load a story. Telling it also requires a state, so start()
        or load_state() it."""
        # Read story
        with open(filename, 'r') as f:
            if filename.endswith('.json'):
                self.document = json.loads(f.read()) # FIXME: Not just f?
            elif filename.endswith('.yaml'):
                self.document = yaml.safe_load(f)
            else:
                raise ValueError # FIXME: More specific? "Wrong file extension"?

    # Session management
    def load_state(self, filename = 'autosave.json'):
        f = open(filename, 'r')
        self.state = json.loads(f.read())
        f.close()

    def save_state(self, filename = 'autosave.json'):
        f = open(filename, 'w')
        f.write(json.dumps(self.state))
        f.close()

    def start(self):
        self.state = {'__history': []}
        self.state['__current_node'] = self.document['start_node']

    # Utility

    def get_state_var(self, field):
        return self.state.get(field, None)

    def set_state_var(self, field, value):
        self.state[field] = value

    def get_metadata(self, field):
        try:
            return self.document[field]
        except KeyError:
            raise NoSuchMetadata

    # Running a session

    # FIXME: Find a better name.
    def eval_current_node(self):
        node_id = self.state['__current_node']
        node = self.story[node_id]
        return eval_story_node(node, self.state)

    def enact(self, action):
        # FIXME: This should also take the user choice, so it'll be
        # easier to actually show actions being rewound/forwarded, not
        # just state changes being made.
        changes = [] # List of tuples of (variable, (before, after))
        if 'set' in action:
            if type(action['set']) == list:
                set_commands = action['set']
            else:
                set_commands = [action['set']]
            for set_command in set_commands:
                var = set_command['var']
                old_val = self.get_state_var(set_command['var'])
                new_val = eval_condition(set_command['val'], self.state)
                self.set_state_var(var, new_val)
                changes.append({'var': var,
                                'from': old_val,
                                'to': new_val})
        # FIXME: 'goto' could be merged into 'set', but syntactic
        # sugar may be nice here?
        if 'goto' in action:
            changes.append({'var': '__current_node',
                            'from': self.state['__current_node'],
                            'to': action['goto']})
            self.state['__current_node'] = action['goto']
        self.state['__history'].append(changes)
