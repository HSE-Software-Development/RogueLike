from roguelike.interfaces import IRoomGameAction, IGameObjectWithPosition, IRoom


class CreateAction(IRoomGameAction):

    def __init__(self, object: IGameObjectWithPosition):
        self.object = object

    def room_handler(self, room: IRoom):
        room.add_object(self.object)
