from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer


from django.shortcuts import render
from django.http import HttpResponse
from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


import matplotlib.pyplot as plt
import networkx as nx
import os

def gen_mat(request):
    edges = []
    enzymes = []
    rcount = 1
    species = set()
    react = set()

    with open(file_path,"r") as f:
        for line in f:
            reaction = f'R{rcount}'
            react.add(str(reaction))
            num = line.split()
            edges.append((num[0], str(reaction)))
            species.add(num[0])
            edges.append((num[1], str(reaction)))
            species.add(num[1])
            edges.append((str(reaction), num[3]))
            species.add(num[3])
            enzymes.append((num[2], str(reaction)))

            rcount += 1
    f.close()
    plt.rcParams['figure.figsize'] = (30.0, 22.0)
    G=nx.DiGraph()
    G.add_edges_from(edges + enzymes)
    shells = [react, species]
    pos = nx.shell_layout(G,shells)
    nx.draw_networkx_nodes(G, pos, nodelist=react,node_size=300,node_shape='s',node_color='r')
    nx.draw_networkx_nodes(G, pos, nodelist=species,node_size=900,node_shape='o')
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=1,arrowstyle='->',arrowsize=40)
    nx.draw_networkx_edges(G, pos, edgelist=enzymes,width=1,
                           alpha=0.5, edge_color='g', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    response=HttpResponse(content_type='image/png')
    plt.savefig(response)
    return response



class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'user': 'qianqian'}, template_name='profiles_api/hellopage.html')

    def post(self, request):
        """Creat a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(sefl, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Creat a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!!!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle deleting an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiview(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating,, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
