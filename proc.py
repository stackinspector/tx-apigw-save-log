from datetime import date, datetime, timedelta
import lzma
from api import get_log

def proc(apigw_client, service_id, date_str):
    dt = datetime.combine(date.today(), datetime.min.time()) if date_str is None else (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1))
    hour = 23
    logs = []

    while hour >= 0:
        stop = False
        context = ""
        count = 1
        end = dt.strftime("%Y-%m-%d %H:%M:%S")
        next_dt = dt - timedelta(hours=1)
        start = next_dt.strftime("%Y-%m-%d %H:%M:%S")
        print("hour[{}]: {} to {}".format(hour, start, end))

        while not stop:
            print("req[{}]: context={}".format(count, context))
            log, context = get_log(apigw_client, start, end, service_id, context)
            logs.extend(log)
            count += 1
            stop = context == ""

        hour -= 1
        dt = next_dt

    logs.reverse()
    logs.append("")

    log_bytes = bytes("\n".join(logs), encoding = "utf8")
    log_xz = lzma.compress(log_bytes, preset=lzma.PRESET_EXTREME)

    filename = "{}-{}.xz".format(dt.strftime("%Y%m%d"), service_id)

    return filename, log_xz
