from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movies.models import Movie, CategoryMovie, MovieOrder


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    synopsis = serializers.CharField(required=False)
    rating = serializers.ChoiceField(
        choices=CategoryMovie.choices, default=CategoryMovie.G
    )
    duration = serializers.CharField(required=False)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, object):
        return object.user.email

    def create(self, validated_data: dict):
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)

    title = serializers.SerializerMethodField()
    buyed_by = serializers.SerializerMethodField()

    def get_buyed_by(self, object):
        return object.user.email

    def get_title(self, object):
        return object.movie.title

    def create(self, validated_data: dict):
        return MovieOrder.objects.create(**validated_data)
