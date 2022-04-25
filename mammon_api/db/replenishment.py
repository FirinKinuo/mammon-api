from sqlalchemy.sql import sqltypes, schema

from mammon_api.db import BaseModel, session


class ReplenishmentHistory(BaseModel):
    """Replenishment history table model"""
    __tablename__ = 'replenishment_history'
    datetime = schema.Column(sqltypes.DateTime(timezone=True), nullable=False)
    currency = schema.Column(sqltypes.INTEGER(), nullable=False)

    def __repr__(self):
        return f"{self.id} | Replenishment on {self.currency}RUB at {self.datetime}"

    @classmethod
    def get_pool_by_datetime(cls, start_datetime: datetime, end_datetime: datetime) -> list['ReplenishmentHistory']:
        return session.query(cls).filter(start_datetime <= ReplenishmentHistory.datetime,
                                         end_datetime >= ReplenishmentHistory.datetime).order_by(cls.id.desc()).all()


def init_tables():
    """Initializing tables in a database"""
    ReplenishmentHistory.__table__.create(checkfirst=True)


if __name__ != "__main__":
    init_tables()
