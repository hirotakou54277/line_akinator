import enum

from tanakinator.models import UserStatus
from tanakinator import db


class GameState(enum.Enum):
    PENDING     = 'pending'
    ASKING      = 'asking'
    GUESSING    = 'guessing'
    RESUMING    = 'resuming'
    BEGGING     = 'begging'
    REGISTERING = 'registering'
    CONFIRMING  = 'confirming'
    TRAINING    = 'training'
    FEATURING   = 'featuring'
    LABELING    = 'labeling'
    UPDATING    = 'updating'


def get_game_status(user_id):
    status = db.session.query(UserStatus).filter_by(user_id=user_id).first()
    return GameState(status.status) if status else GameState.PENDING

def get_feature_table():
    result = {
        "S1": {"Q1": 1.0, "Q2": 0.0, "Q3": 1.0},
        "S2": {"Q1": 1.0, "Q2": 1.0, "Q3": 0.0},
        "S3": {"Q1": 0.0, "Q2": 1.0, "Q3": 0.0},
        "S4": {"Q1": 1.0, "Q2": 0.0, "Q3": 0.0},
    }
    return result
