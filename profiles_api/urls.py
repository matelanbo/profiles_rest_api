from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from profiles_api import views

app_name = 'profiles_api'
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('profile2', views.UserProfileViewSet2)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiview.as_view()),
    path('', include(router.urls)),
    path('imagetest/', views.gen_mat, name='image'),
    ]
