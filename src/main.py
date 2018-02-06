from creeps.creeps import Creeps
from creeps.harvester import Harvester
from creeps.builder import Builder
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


def creep_size_selector(spawn, CreepRole, role):
    # Get the number of our creeps in the room.
    num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                        c.memory.role == role)

    # If there are no creeps, spawn a creep once energy is at 250 or more
    if num_creeps < CreepRole.MIN_CREEP and spawn.room.energyAvailable >= 250:
        console.log(f'Building a {role}')
        CreepRole.create_creep('small', spawn, role)
    # If there are less than 15 creeps but at least one, wait until all spawns and extensions are full before
    # spawning.
    elif num_creeps < CreepRole.MAX_CREEP and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
        console.log(f'Building a {role}')
        if spawn.room.energyCapacityAvailable >= 900:
            Creeps.create_creep('large', spawn, role)
        # If we have more energy, spawn a bigger creep.
        if spawn.room.energyCapacityAvailable >= 450:
            Creeps.create_creep('medium', spawn, role)
        else:
            Creeps.create_creep('small', spawn, role)


def main():
    """
    Main game logic loop.
    """

    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role is 'harvester' or creep.memory.role is 'controller_harvester':
            Harvester.run_creep(creep)
        elif creep.memory.role is 'builder':
            Builder.run_creep(creep)
        else:
            Creeps.run_creep(creep)

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]

        last_spawn = spawn.memory.last_spawn
        if spawn.spawning is None and (last_spawn is not "harvester" and last_spawn is not "controller_harvester"):
            creep_size_selector(spawn, Harvester, 'harvester')

        if spawn.spawning is None and last_spawn is not "controller_harvester" and last_spawn is not "builder":
            creep_size_selector(spawn, Harvester, 'controller_harvester')

        if spawn.spawning is None and last_spawn is not "builder":
            creep_size_selector(spawn, Builder, 'builder')


module.exports.loop = main
