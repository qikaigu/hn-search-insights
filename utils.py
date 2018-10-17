from datetime import datetime, timedelta


def get_date_range(start, end, fmt):
    start = datetime.strptime(start, fmt)
    end = datetime.strptime(end, fmt)
    diff = (end - start).days

    res = []
    if diff < 0:
        return res

    cur = start
    while cur <= end:
        res.append(datetime.strftime(cur, fmt))
        cur = cur + timedelta(1)

    return res
