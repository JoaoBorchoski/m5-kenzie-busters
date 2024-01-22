from django.db import models


class CategoryMovie(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, default=None)
    rating = models.CharField(
        max_length=20, choices=CategoryMovie.choices, default=CategoryMovie.G
    )
    synopsis = models.TextField(null=True, default=None)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )

    movie_order = models.ManyToManyField(
        "users.User", through="movies.MovieOrder", related_name="movie_order"
    )


class MovieOrder(models.Model):
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie")
