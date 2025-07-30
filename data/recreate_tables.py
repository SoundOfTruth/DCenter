import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.database.core import Base, engine # noqa
from src.models import * # noqa


# replaced to alembic
def drop_tables():
    db = Base()
    db.metadata.drop_all(engine)


def create_tables():
    db = Base()
    db.metadata.create_all(engine)
