from sqlalchemy.sql import sqltypes, schema

from mammon_api.db import BaseModel


class ReplenishmentHistory(BaseModel):
    """Replenishment history table model"""
    __tablename__ = 'replenishment_history'
    datetime = schema.Column(sqltypes.DateTime(timezone=True), nullable=False)
    currency = schema.Column(sqltypes.INTEGER(), nullable=False)

    def __repr__(self):
        return f"{self.id} | Replenishment on {self.currency}RUB at {self.datetime}"


def init_tables():
    """Initializing tables in a database"""
    ReplenishmentHistory.__table__.create(checkfirst=True)


if __name__ != "__main__":
    init_tables()
