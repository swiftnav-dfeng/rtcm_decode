from datetime import datetime, timedelta

# return UTC
# tow - milliseconds
def gps_utc(week, tow, leap_seconds):
    gps_start = datetime(year=1980, month=1, day=6, hour=0, minute=0, second=0)

    #since rollover april 2019
    week_offset = 2048
    week_total = week_offset + week
    total_days = week_total * 7
    total_microseconds  = tow * 1000

    return gps_start + timedelta(days=total_days, seconds=leap_seconds, microseconds=total_microseconds)

# return UTC
# tow - milliseconds
def glo_utc(na, dow, epoch_time):
    glo_start = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
    delta = timedelta(days=na-1, hours=-3, microseconds=epoch_time*1000)


    return glo_start + delta

# return UTC
# tow - milliseconds
def gal_utc(week, tow, leap_seconds):
    gal_start = datetime(year=1999, month=8, day=22, hour=0, minute=0, second=0)

    # rollover after 4096 weeks
    week_offset = 0
    week_total = week_offset + week
    total_days = week_total * 7
    total_microseconds  = tow * 1000

    return gal_start + timedelta(days=total_days, seconds=leap_seconds, microseconds=total_microseconds)

# return UTC
# tow - milliseconds
def bds_utc(week, tow, leap_seconds):
    bds_start = datetime(year=2006, month=1, day=1, hour=0, minute=0, second=0)

    # rollover after 4096 weeks
    week_offset = 0
    week_total = week_offset + week
    total_days = week_total * 7
    total_microseconds  = tow * 1000

    # BDS is 14 seconds behind GPS
    delta_seconds = leap_seconds + 14

    return bds_start + timedelta(days=total_days, seconds=delta_seconds, microseconds=total_microseconds)


if __name__ == "__main__":

    # results should be Apr 22, 2022, 19:46:32 UTC
    leap_seconds = -18

    gps_week = 158
    gps_tow = 503210000
    print(f'GPS {gps_utc(gps_week,gps_tow,leap_seconds)} UTC')

    glo_na = 843
    glo_dow = 5
    glo_epoch_time = 81992000
    print(f'GLO {glo_utc(glo_na,glo_dow,glo_epoch_time)} UTC')

    gal_week = 1182
    gal_tow = 503210000
    print(f'GAL {gal_utc(gal_week,gal_tow,leap_seconds)} UTC')

    bds_week = 850
    bds_tow = 503196000
    print(f'BDS {bds_utc(bds_week,bds_tow,leap_seconds)} UTC')
