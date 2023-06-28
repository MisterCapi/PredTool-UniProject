from abc import ABC, abstractmethod


class Stats(ABC):
    def __init__(self, total_games, win_rate):
        self.total_games = total_games
        self.win_rate = win_rate

    def __repr__(self):
        return f"{type(self).__name__}(total_games={self.total_games}, win_rate={self.win_rate})"


class HeroPlayerStats(Stats):
    def __init__(self, total_games, win_rate):
        super().__init__(total_games, win_rate)


class OverallPlayerStats(Stats):
    def __init__(self, mmr_rating, total_games, average_kda, kda_ratio, favourite_role, win_rate):
        super().__init__(total_games, win_rate)
        self.mmr_rating = mmr_rating
        self.average_kda = average_kda
        self.kda_ratio = kda_ratio
        self.favourite_role = favourite_role

    def __repr__(self):
        return f"{type(self).__name__}(mmr_rating={self.mmr_rating}, total_games={self.total_games}, " \
               f"average_kda={self.average_kda}, kda_ratio={self.kda_ratio}, " \
               f"favourite_role='{self.favourite_role}', win_rate={self.win_rate})"
