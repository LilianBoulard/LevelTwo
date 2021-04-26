"""
Inserts default objects into the database.
"""

from .. import Database
from .. import ObjectDBO
from ... import GenericObject
from ... import ArrivalPoint, Empty, Mud, StartingPoint, Trap, Wall


def insert_objects():
    def object_to_dbo_object(generic_object: GenericObject) -> ObjectDBO:
        name = generic_object.name
        effect = generic_object.effect.value
        traversable = generic_object.traversable
        min_instances = generic_object.min_instances
        max_instances = generic_object.max_instances
        object_dbo = ObjectDBO(name=name,
                               effect=effect,
                               traversable=traversable,
                               min_instances=min_instances,
                               max_instances=max_instances)
        return object_dbo

    db = Database()

    # Add objects to the database
    with db.init_session() as session:
        for obj in [ArrivalPoint(), Empty(), Mud(), StartingPoint(), Trap(), Wall()]:
            session.add(object_to_dbo_object(obj))

    for obj in db.get_all_objects():
        print(obj.identifier, obj.name)
