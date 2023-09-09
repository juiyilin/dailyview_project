from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from popular import views


app_name = 'api'

login_api = [  # jwt
    path('jwt_login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('jwt_logout/', views.JWTLogout.as_view()),
]

article_api = [
    path('article/', views.ArticleView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('article/<str:pk>/', views.ArticleView.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    path('article/<str:article_id>/detail/', views.ArticleDetailPostView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('article/detail/<str:pk>/', views.ArticleDetailPostView.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
]

urlpatterns = login_api + article_api
urlpatterns += [path('alive/', views.IsAlive.as_view())]
