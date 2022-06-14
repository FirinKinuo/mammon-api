from fastapi.routing import APIRouter

from mammon_api.db.replenishment import ReplenishmentHistory
from .schemas import Replenishment, ReplenishmentDate

router = APIRouter(
    prefix="/replenishments",
    tags=["replenishments"]
)


@router.post(
    path="",
    response_model=list[Replenishment],
    name="Read all replenishments by date"
)
async def read_replenishments_by_date(datetime_: ReplenishmentDate) -> list[Replenishment]:
    replenishments = ReplenishmentHistory.get_pool_by_datetime(
        start_datetime=datetime_.start,
        end_datetime=datetime_.end)
    return [Replenishment(id=r.id, datetime=r.datetime, currency=r.currency) for r in replenishments]
