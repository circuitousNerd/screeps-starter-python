# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Creeps(object):

    BODY_TYPE = {
        'small': {
            'components': [WORK, CARRY, MOVE, MOVE],
            'price': 250
        },
        'medium': {
            'components': [WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE],
            'price': 450
        },
        'large': {
            'components': [WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY,
                           MOVE, MOVE, MOVE, MOVE, MOVE, MOVE],
            'price': 900
        }
    }

    @staticmethod
    def create_creep(body, spawn, role):
        console.log(JSON.stringify(role))

        role = role
        creep_name = role + spawn.name + Game.time

        if body in Creeps.BODY_TYPE:
            body_type = Creeps.BODY_TYPE[body]
        else:
            console.log('Invalid body type')

        if not role:
            exit()
        elif body_type['price'] >= spawn.room.energyAvailable:
            console.log(f'Unable to create creep: {body_type}')
        elif (not spawn.spawning) and (spawn.memory.last_spawn is not role):
            spawn.memory.last_spawn = role
            spawn_return = spawn.spawnCreep(body_type['components'], creep_name, {
                'memory': {
                    'role': role
                }
            })
            if spawn_return is OK:
                spawn.memory["last_spawn"] = role
                console.log(f'should be spawning a new creep named: {creep_name} of size {body_type}')

    @staticmethod
    def run_creep(creep):
        creep.say(f'{creep.memory.role}')