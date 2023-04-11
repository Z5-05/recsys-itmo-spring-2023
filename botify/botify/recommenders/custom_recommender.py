from .random import Random
from .recommender import Recommender
import random


class CustomRecommender(Recommender):
    """
    Recommend tracks closest to the previous one.
    Fall back to the random recommender if no
    recommendations found for the track.
    """

    def __init__(self
               , tracks_redis
               , contextual_recommendations_redis
               , custom_recommendations_redis
               , catalog):
        self.tracks_redis = tracks_redis
        self.contextual_recommendations_redis = contextual_recommendations_redis
        self.custom_recommendations_redis = custom_recommendations_redis
        self.fallback = Random(tracks_redis)
        self.catalog = catalog

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        previous_track = self.tracks_redis.get(prev_track)
        if previous_track is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)
        previous_track_obj = self.catalog.from_bytes(previous_track)
        # если все нормально, ищем трек из контекста и из тех, которые нравятся пользователю
        custom_recommendations = self.custom_recommendations_redis.get(user)
        custom_recommendations = set(self.catalog.from_bytes(custom_recommendations))
        if not custom_recommendations:
            custom_recommendations = []
        contextual_recommendations = self.contextual_recommendations_redis.get(previous_track_obj.track)
        contextual_recommendations = set(self.catalog.from_bytes(contextual_recommendations))
        if not contextual_recommendations:
            contextual_recommendations = []
        
        recommendations = contextual_recommendations.intersection(custom_recommendations)
        if not recommendations:
            recommendations = contextual_recommendations.union(custom_recommendations)
        if not recommendations:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        return shuffled[0]
