from dataclasses import dataclass


@dataclass
class FilmRatingDomain:
    count_likes: int = 0
    count_dislikes: int = 0
    total: int = 0
    summary: int = 0
