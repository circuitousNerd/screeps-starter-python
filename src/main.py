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

MIN_HARVESTER = 2
MAX_HARVESTER = 10

MIN_BUILDER = 2
MAX_BUILDER = 10


def main():
    """
    Main game logic loop.
    """

    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role is 'harvester':
            Harvester.run_creep(creep)
        elif creep.memory.role is 'builder':
            Builder.run_creep(creep)
        else:
            Creeps.run_creep(creep)

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        last_spawn = spawn.memory.last_spawn
        if spawn.spawning is None and last_spawn is not "harvester":
            # Get the number of our creeps in the room.
            num_harvester_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                      c.memory.role == 'harvester')

            # If there are no creeps, spawn a creep once energy is at 250 or more
            if num_harvester_creeps < MIN_HARVESTER and spawn.room.energyAvailable >= 250:
                console.log('Building a harvester')
                Harvester.create_creep('small', spawn)
            # If there are less than 15 creeps but at least one, wait until all spawns and extensions are full before
            # spawning.
                Harvester.create_creep('small', spawn)

            elif num_harvester_creeps < MAX_HARVESTER and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
                console.log('Building a harvester')
                if spawn.room.energyCapacityAvailable >= 900:
                    Harvester.create_creep('large', spawn)
                # If we have more energy, spawn a bigger creep.
                if spawn.room.energyCapacityAvailable >= 450:
                    Harvester.create_creep('medium', spawn)
                else:
                    Harvester.create_creep('small', spawn)

        if spawn.spawning is None and last_spawn is not "builder":
            num_builder_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and
                                                              c.memory.role == 'builder')
            if num_builder_creeps < MIN_BUILDER and spawn.room.energyAvailable >= 250:
                Builder.create_creep('small', spawn)
            elif num_builder_creeps < MAX_BUILDER and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
                if spawn.room.energyCapacityAvailable >= 900:
                    Builder.create_creep('large', spawn)
                elif spawn.room.energyCapacityAvailable >= 450:
                    Builder.create_creep('medium', spawn)
                else:
                    Builder.create_creep('small', spawn)


module.exports.loop = main
