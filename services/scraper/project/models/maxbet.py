from sqlalchemy.sql import func
from project import db


class MaxbetFlattened(db.Model):
    __table_args__ = dict(schema="flattened")
    __tablename__ = "flattened_maxbet"

    unique_id = db.Column(db.String(128), primary_key=True)
    rec_created_at = db.Column(db.DateTime, nullable=False)
    league_id = db.Column("bet_league_id", db.Integer, nullable=False)
    league_name = db.Column("bet_league_name", db.String(128), nullable=False)
    match_id = db.Column("match_id", db.Integer, nullable=False)
    home_team = db.Column("match_home", db.String(128), nullable=False)
    away_team = db.Column("match_away", db.String(128), nullable=False)
    odds_name = db.Column("odds_name", db.String(128))
    tip_name = db.Column("tip_type", db.String(128), nullable=False)
    tip_description = db.Column("tip_description", db.String(128), nullable=False)
    tip_value = db.Column("tip_value", db.Integer, nullable=False)

    def __init__(self, match_id):
        self.match_id = match_id

    def to_json(self):
        return {"league_name": self.league_name, "home_team": self.home_team, "away_team": self.away_team}
