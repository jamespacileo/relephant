from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter, BaseRouter
from core.models import GameComment
from core.serializers import GameCommentSerializer
from swampdragon.pubsub_providers.data_publisher import publish_data
import time

class GameCommentRouter(ModelRouter):
    route_name = 'game-comment'
    serializer_class = GameCommentSerializer
    model = GameComment

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    # def send_command(self, value):


# def add_comment(self, value):


route_handler.register(GameCommentRouter)

direction_map = {
    "up": "up",
    "down": "bottom",
    "left": "left",
    "right": "right"
}

class GameRouter(BaseRouter):

    route_name = "game"
    valid_verbs = ["send_command", "subscribe"]
    # serializer_class = GameCommentSerializer
    # model = GameComment
    position = [10, 6]
    bounds = [19, 14]
    comments = []
    last_comments = []

    last_command_timestamp = [time.time() * 1000, 0]

    def __init__(self, *args, **kwargs):
        # self.position = [0, 0]
        # self.bounds = [19, 14]
        # self.comments = []
        # self.last_comments = []

        # self.last_command_timestamp = time.time() * 1000
        return super(GameRouter, self).__init__(*args, **kwargs)
    

    def send_command(self, comment, command=None, player=None):
        # self.position[0] += 1
        # self.position[1] += 1

        print(self.position)

        self.comments.append(comment)
        self.last_comments.append(comment)

        print(self.last_command_timestamp[0])
        now_timestamp = time.time() * 1000
        if not self.last_command_timestamp[0]:
            self.last_command_timestamp[0] = now_timestamp

        print(now_timestamp, self.last_command_timestamp[0], (now_timestamp - self.last_command_timestamp[0]))

        if command and ((now_timestamp - self.last_command_timestamp[0]) > 1500):
            print("triggered!")
            
            self.last_command_timestamp[0] = now_timestamp

            self.move_player(command)

            direction = direction_map[command]
            publish_data("global", {
                'type': "move",
                'position': self.position,
                'direction': direction
            })

        self.send({
            'position': self.position,
            'last_comment': comment,
            'last_command': command

        })
        publish_data("global", {
            "type": "comment",
            'position': self.position,
            'comment': comment,
            'command': command,
            "player": player
        })

    def move_player(self, direction):
        if direction == "up":
            if self.position[1] > 0:
                self.position[1] -= 1
            return
        if direction == "down":
            if self.position[1] < self.bounds[1]:
                self.position[1] += 1
            return
        if direction == "left":
            if self.position[0] > 0:
                self.position[0] -= 1
            return
        if direction == "right":
            if self.position[0] < self.bounds[0]:
                self.position[0] += 1
            return



    def get_subscription_channels(self, **kwargs):
        return ["global"]

    # def get_object(self, **kwargs):
    #     return self.model.objects.get(pk=kwargs['id'])

    # def get_query_set(self, **kwargs):
    #     return self.model.objects.all()


    # def subscribe(self, **kwargs):
    #     client_channel = kwargs.pop('channel')
    #     # server_channels = self.get_subscription_channels(**kwargs)
    #     self.send(
    #         data='subscribed',
    #         channel_setup=self.make_channel_data(client_channel, ["game"], "subscribe"),
    #         **kwargs)
    #     self.connection.pub_sub.subscribe(["game"], self.connection)


route_handler.register(GameRouter)