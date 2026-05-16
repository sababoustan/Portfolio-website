from rest_framework import serializers
from comments.models import Comment


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "body", "created_at"]
        

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "body",
            "created_at",
            "replies",
            "is_active",
            ]