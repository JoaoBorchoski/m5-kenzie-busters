from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from users.permissions import MyCustomPermission

from movies.models import Movie
from movies.serializers import MovieSerializer, MovieOrderSerializer

from django.forms.models import model_to_dict


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermission]

    def get(self, req):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, req, view=True)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, req):
        serializer = MovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieViewDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermission]

    def get(self, req, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response("message: id not found", status.HTTP_404_NOT_FOUND)

    def delete(self, req, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()
            return Response(None, status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response("message: id not found", status.HTTP_404_NOT_FOUND)


class MovieOrderViewDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieOrderSerializer(data=req.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=req.user, movie=movie)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Movie.DoesNotExist:
            return Response("message: id not found", status.HTTP_404_NOT_FOUND)
