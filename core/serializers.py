from swampdragon.serializers.model_serializer import ModelSerializer
# from .models import GameComment

class GameCommentSerializer(ModelSerializer):
    class Meta:
        model = 'core.GameComment'
        # model = GameComment
        publish_fields = ('comment', 'command' )
        update_fields = ('comment', 'command' )