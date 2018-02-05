from creeps.creeps import Creeps
from creeps.harvester import Harvester
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


class Builder(Harvester):

    @staticmethod
    def create_creep(body, spawn):

        role = 'builder'
        creep_name = role + spawn.name + Game.time

        if body in Harvester.BODY_TYPE:
            body_type = Harvester.BODY_TYPE[body]
        else:
            console.log('Invalid body type')

        if body_type['price'] >= spawn.room.energyAvailable:
            console.log(f'Unable to create harvester: {body_type}')
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
        """
        Runs a creep as a generic builder.
        :param creep: The creep to run
        """

        Creeps.run_creep(creep)
        # If we're full, stop filling up and remove the saved source
        if creep.memory.filling and _.sum(creep.carry) >= creep.carryCapacity:
            creep.memory.filling = False
            del creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not creep.memory.filling and creep.carry.energy <= 0:
            creep.memory.filling = True
            del creep.memory.target

        if creep.memory.filling:
            # If we have a saved source, use it
            if creep.memory.source:
                source = Game.getObjectById(creep.memory.source)
            else:
                # Get a random new source and save it
                source = _.sample(creep.room.find(FIND_SOURCES))
                creep.memory.source = source.id

            # If we're near the source, harvest it - otherwise, move to it.
            if creep.pos.isNearTo(source):
                result = creep.harvest(source)
                if result != OK:
                    print("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
            else:
                creep.moveTo(source)
        else:
            # If we have a saved source, use it
            if creep.memory.construction_site:
                construction_site = Game.getObjectById(creep.memory.construction_site)
            else:
                # Get a random new source and save it
                construction_site = _.sample(creep.room.find(FIND_CONSTRUCTION_SITES))
                creep.memory.construction_site = construction_site.id

            # If we're near the construction_site, build it - otherwise, move to it.
            if creep.pos.isNearTo(construction_site):
                result = creep.build(construction_site)
                if result != OK:
                    print("[{}] Unknown result from creep.build({}): {}".format(creep.name, construction_site, result))
            else:
                creep.moveTo(construction_site)


