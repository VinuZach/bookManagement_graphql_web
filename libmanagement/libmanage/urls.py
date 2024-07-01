from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .schema import *


urlpatterns = [
    path('author', csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema_link)))

]