from roguelike.interfaces import IRoomGameAction, IGameObjectWithPosition, IRoom


class RemoveAction(IRoomGameAction):

    def __init__(self, object: IGameObjectWithPosition):
        self.object = object

    def room_handler(self, room: IRoom):
        room.remove_object(self.object)
