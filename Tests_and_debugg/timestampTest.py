from datetime import datetime

timestamp = 1694873473.913011
date_time = datetime.fromtimestamp(timestamp)

print("Date time object:", date_time)

d = date_time.strftime("%H:%M:%S:%f")
print(d)
