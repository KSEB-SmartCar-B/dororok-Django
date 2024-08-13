from dataclasses import dataclass

@dataclass
class MusicRecommendationParams:
    member_id: int
    genre: []
    lat: float
    lng: float
    region1depth_name: str
    region2depth_name: str
    region3depth_name: str
    sky_condition: str
    precipitation: str
    music_mode: str
    day_part: str
    is_first: int
