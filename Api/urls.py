from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from Api import views


app_name = 'api'

login_api = [  # jwt
    path('jwt_login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('jwt_logout/', views.JWTLogout.as_view()),
    path('test/', views.Test.as_view()),
]


article_api = [
    # path('article/', views.PersonListView.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # path('article/<str:pk>/', views.PersonListView.as_view({
    #     'put': 'update',
    #     'delete': 'destroy'
    # })),
]

urlpatterns = login_api + article_api
