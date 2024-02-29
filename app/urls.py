
from django.urls import path
from .views import get_user,signin,signout,ai

urlpatterns = [
    path("get_user",get_user.GetUser, name="get_user"),
    path('login', signin.LoginAPI.as_view(), name='login'),
    path('logout', signout.LogoutAPI.as_view(), name='login'),
    path('posts', ai.PostListCreateAPIView.as_view(), name='post-list-create'),

]

