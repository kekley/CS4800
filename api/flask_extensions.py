from flask_sqlalchemy import SQLAlchemy
from pusher import Pusher

from constants import (
    PUSHER_APP_ID, 
    PUSHER_KEY, 
    PUSHER_CLUSTER, 
    PUSHER_SECRET
)

db = SQLAlchemy()

pusher = Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET,
    cluster=PUSHER_CLUSTER,
    ssl=True
)