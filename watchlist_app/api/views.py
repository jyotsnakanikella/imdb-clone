from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination,WatchListCPagination

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
#filtering based on url(not with dictionary type normal type)
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     #the below __ is given becs it is foreign key
    #     return Review.objects.filter(review_user__username = username)
 #filtering based on dictionary params in url
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username = username)

#new class becs if i got with reviewlist to post also i need to send watchlist
#instead i dont want to send watchlist details in review so new class
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle, AnonRateThrottle]
 
    def get_queryset(self):
        return Review.objects.all()

    #override create feature
    def perform_create(self,serializer):

        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)

        #dont allow same user to write multiple reviews for sam ewatchlist
        review_user = self.request.user
        #arguments came from model
        review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)

        if review_queryset.exists():
            raise ValidationError("You already gave a review for the same show")
        #now sending watchlist here so need to send in post the watchlist again

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist = watchlist, review_user = review_user)


#concrete class
class ReviewList(generics.ListAPIView):
    #for reviews of sepcific movie we need to override default query set
    # queryset =  Review.objects.all()  
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    #anyone can see review irrespective of authenticated user or not
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # #filtering based on
    # filterset_fields = ['review_user__username','active']

    #override querySet
    def get_queryset(self):
        pk = self.kwargs['pk']
        #watchlist : in Rev iew Model we have watchlist use the same
        return Review.objects.filter(watchlist = pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    #if it is get or admin then able to access else no
    permission_classes = [IsReviewUserOrReadOnly]
    #if we do like below there are counted together with the reviewlist and reviewdetail together
    throttle_classes = [ScopedRateThrottle]
    #i can repeat this scope at other classes but they all with same scope will be counted together
    throttle_scope = 'review-detail'

#Using Mixins  
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()   
#     serializer_class = ReviewSerializer
  
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request,*args,**kwargs)  
  
#django-filtering working example  
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    #so it will by default created so dont use other filtering so commenting ordering down
    pagination_class = WatchListCPagination
    #filtering
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','platform__name']
    #searching
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title','platform__name']
    #ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['title','avg_rating']

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)   
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try:
            movies = WatchList.objects.get(pk = pk)
            
        except WatchList.DoesNotExist:
            return Response({'Error':'Movie Not Found'},status = status.HTTP_404_NOT_FOUND)      
        serializer = WatchListSerializer(movies)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(movie,data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST ) 


    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)           
 
#model view set which has all options
# if u want read only modelviewset include readonly class 
#viewsets.ReadOnlyModelViewSet -> for read only 
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

#using viewsets  -> handle list and invidual together
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset,many = True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk = None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk = pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer =StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)  

#     #doubt below need to check
#     # def destroy(self, request, pk):
#     #     stream = StreamPlatformSerializer(pk =)              

  
#class based views 
class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        streams = StreamPlatform.objects.all()
        #normal serializer
        serializer = StreamPlatformSerializer(streams,many=True)
        #serializer when we want to open hyperlinks of respective clicked movie details
        # serializer = StreamPlatformSerializer(streams,many=True,context = {'request':request})
        return Response(serializer.data) 

    def post(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)   

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movies = StreamPlatform.objects.get(pk = pk)
            
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Movie Not Found'},status = status.HTTP_404_NOT_FOUND)      
        serializer = StreamPlatformSerializer(movies)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(movie,data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST ) 


    def delete(self,request,pk):
        movie = StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)                 


# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated]) --> function based views permissions
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)   
#         else:
#             return Response(serializer.errors)     

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.get(pk = pk)
            
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie Not Found'},status = status.HTTP_404_NOT_FOUND)      
#         serializer = MovieSerializer(movies)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(movie,data = request.data) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST ) 

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)           
 
