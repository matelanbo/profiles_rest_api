from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, ReactionNetworks
from django.contrib.auth.models import User


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippetss = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-highlight', read_only=True)
#    newtest = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-highlight', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippetss')


class ReactionNetworksSerializer(serializers.ModelSerializer):
#    snippetss = serializers.HyperlinkedRelatedField(many=True, view_name='reactions', read_only=True)
#    newtest = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-highlight', read_only=True)
    network_image = serializers.HyperlinkedIdentityField(view_name='snippet-highlight')
    network_text = serializers.HyperlinkedIdentityField(view_name='readreaction')
    class Meta:
        model = ReactionNetworks
        fields = ('network', 'network_image', 'network_text')
