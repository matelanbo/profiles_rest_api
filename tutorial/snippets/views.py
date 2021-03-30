from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from snippets import serializers

from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import networkx as nx
import os

#class SnippetHighlight(generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    renderer_classes = (renderers.StaticHTMLRenderer,)

#    def get(self, request, *args, **kwargs):
#        snippet = self.get_object()
#        return Response(snippet.highlighted)

class SnippetHighlight(APIView):
    """Test API View"""
#    serializer_class = serializers.HelloSerializer
#    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        edges = []
        enzymes = []
        rcount = 1
        species = set()
        react = set()
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'React_N_Real00988.txt')
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

#    def get(self, request, *args, **kwargs):
#        p = args[0]

#        return Response({'user': kwargs['pk']}, template_name='snippets/hellopage.html')

#@api_view(['GET'])
#def api_root(request, format=None):
#    return Response({
#        'users': reverse('user-list', request=request, format=format),
#        'snippets': reverse('snippet-list', request=request, format=format)
#    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
