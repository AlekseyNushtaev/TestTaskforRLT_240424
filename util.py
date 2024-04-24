import asyncio

from motor.motor_asyncio import AsyncIOMotorCollection

from datetime import datetime, timedelta
import calendar


async def find_data(dt_from: str,
                    dt_upto: str,
                    group_type: str,
                    collection: AsyncIOMotorCollection):
    """Функция для выполнения запроса в БД за выбранный период"""

    dt_from = datetime.strptime(dt_from, '%Y-%m-%dT%H:%M:%S')
    dt_upto = datetime.strptime(dt_upto, '%Y-%m-%dT%H:%M:%S')
    lst = [dt_from]

    if group_type == "month":
        days_in_month = calendar.monthrange(dt_from.year, dt_from.month)[1]
        date = datetime(dt_from.year, dt_from.month, 1, 0, 0, 0) + timedelta(days=days_in_month)
        while date <= dt_upto:
            lst.append(date)
            days_in_month = calendar.monthrange(date.year, date.month)[1]
            date = date + timedelta(days=days_in_month)

    elif group_type == "day":
        date = datetime(dt_from.year, dt_from.month, dt_from.day, 0, 0, 0) + timedelta(days=1)
        while date <= dt_upto:
            lst.append(date)
            date = date + timedelta(days=1)

    elif group_type == "hour":
        date = datetime(dt_from.year, dt_from.month, dt_from.day, dt_from.hour, 0, 0) + timedelta(hours=1)
        while date <= dt_upto:
            lst.append(date)
            date = date + timedelta(hours=1)

    lst.append(dt_upto + timedelta(seconds=1))

    coros = []
    for i in range(1, len(lst)):
        document = collection.find({"dt": {"$gte": lst[i - 1], "$lt": lst[i], }})
        items = document.to_list(length=105000)
        coros.append(items)
    res = await asyncio.gather(*coros)

    dataset = []
    for items in res:
        data = sum([item["value"] for item in items])
        dataset.append(data)

    labels = list(map(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'), lst[:-1]))

    return {"dataset": dataset, "labels": labels}
