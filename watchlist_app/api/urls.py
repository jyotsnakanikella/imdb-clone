# from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.models import StreamPlatform
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (ReviewDetail, ReviewList,ReviewCreate,
                                    WatchListAV, StreamPlatformVS,
                                    WatchDetailAV,StreamPlatformAV,
                                    StreamPlatformDetailAV,UserReview,WatchListGV)

# urlpatterns = [
#     path('list/',movie_list,name='movie-list'),
#     path('<int:pk>',movie_details,name='movie-details'),
# ]

#Routers will helpto combine urls
router = DefaultRouter()
router.register('stream', StreamPlatformVS,basename = 'streamplatform')

urlpatterns = [
    path('list/',WatchListAV.as_view(),name='watch-list'),
    path('<int:pk>',WatchDetailAV.as_view(),name='watch-details'),
    path('list2/',WatchListGV.as_view(),name='watch-list2'),
    path('',include(router.urls)),
    #now will combine both using above 
    # path('stream/',StreamPlatformAV.as_view(),name='stream'),
    # path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='stream-details'),


    path('<int:pk>/review-create',ReviewCreate.as_view(),name = 'review-create'),
    path('<int:pk>/reviews',ReviewList.as_view(),name = 'review-list'),
    path('reviews/<int:pk>',ReviewDetail.as_view(),name = 'review-details'),
    path('reviews/<str:username>/',UserReview.as_view(),name = 'user-review-detail'),
    #we have query params so no need to give string username parameter as above url
    path('reviews/',UserReview.as_view(),name = 'user-review-detail'),
    # path('review/',ReviewList.as_view(),name = 'review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name = 'review-details'),
]
