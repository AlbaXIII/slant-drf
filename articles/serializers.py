from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username'),
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')

    def validate_image_size(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Article
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'created_on', 'updated_on', 'publisher', 'subject',
            'title', 'image', 'body',
        ]
