import datetime
from typing import Optional
from pydantic import BaseModel, validator


class Base(BaseModel):
    count300: Optional[int] = 0
    count100: Optional[int] = 0
    count50: Optional[int] = 0

    playcount: Optional[int] = 0
    ranked_score: Optional[int] = 0
    total_score: Optional[int] = 0

    pp_rank: Optional[int] = 0
    pp_country_rank: Optional[int] = 0
    level: Optional[float] = 0.0
    pp_raw: Optional[float] = 0.0

    pp: Optional[int] = 0
    better_level: Optional[int] = 0

    accuracy: Optional[float] = 0.0
    better_accuracy: Optional[float] = 0.0

    count_rank_ss: Optional[int] = 0
    count_rank_ssh: Optional[int] = 0

    count_rank_s: Optional[int] = 0
    count_rank_sh: Optional[int] = 0

    count_rank_a: Optional[int] = 0

    total_seconds_played: Optional[int] = 0
    total_playtime: Optional[datetime.timedelta] = datetime.timedelta(seconds=0)

    class Config:
        validate_assignment = True

    @validator('level', 'pp_raw', 'accuracy')
    def float_validator(cls, v):
        if v is None:
            return 0.0
        return v

    @validator(
        'total_seconds_played', 'count300', 'count100', 'count50', 'playcount', 'ranked_score', 'total_score',
        'pp_rank', 'pp_country_rank', 'count_rank_ss', 'count_rank_ssh', 'count_rank_s', 'count_rank_sh', 'count_rank_a'
    )
    def int_validator(cls, v):
        if v is None:
            return 0
        return v
