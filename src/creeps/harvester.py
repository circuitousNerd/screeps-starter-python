from creeps.creeps import Creeps
from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Harvester(Creeps):

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
    def create_creep(body, spawn):

        creep_name = 'harvester' + spawn.name + Game.time
        role = 'harvester'

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
            if spawn_return == OK:
                spawn.memory["last_spawn"] = role
                console.log(f'should be spawning a new creep named: {creep_name} of size {body_type}')


    @staticmethod
    def run_creep(creep):
        """
        Runs a creep as a generic harvester.
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
            # If we have a saved target, use it
            if creep.memory.target:
                target = Game.getObjectById(creep.memory.target)
            else:
                # Get a random new target.
                target = _(creep.room.find(FIND_STRUCTURES)) \
                    .filter(lambda s: ((s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION)
                                       and s.energy < s.energyCapacity) or s.structureType == STRUCTURE_CONTROLLER) \
                    .sample()
                creep.memory.target = target.id

            # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
            if target.energyCapacity:
                is_close = creep.pos.isNearTo(target)
            else:
                is_close = creep.pos.inRangeTo(target, 3)

            if is_close:
                # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
                if target.energyCapacity:
                    result = creep.transfer(target, RESOURCE_ENERGY)
                    if result == OK or result == ERR_FULL:
                        del creep.memory.target
                    else:
                        print("[{}] Unknown result from creep.transfer({}, {}): {}".format(
                            creep.name, target, RESOURCE_ENERGY, result))
                else:
                    result = creep.upgradeController(target)
                    if result != OK:
                        print("[{}] Unknown result from creep.upgradeController({}): {}".format(
                            creep.name, target, result))
                    # Let the creeps get a little bit closer than required to the controller, to make room for other creeps.
                    if not creep.pos.inRangeTo(target, 2):
                        creep.moveTo(target)
            else:
                creep.moveTo(target)
