import time
from datetime import datetime
import argparse


# convert utc timestamp to local datetime
def utctimestamp_to_local_datetime(utc_ts):
    try:
        return datetime.fromtimestamp(float(utc_ts) - time.altzone)
    except:
        return None


# convert utc timestamp to local datetime
# local datetime to utc timestamp
def datetime_to_utctimestamp(dt):
    t = time.gmtime(time.mktime(dt.timetuple()))
    return time.mktime(t)


def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def local_timestamp_to_utctimstamp(s):
    dt = datetime.fromtimestamp(float(s))
    return datetime_to_utctimestamp(dt)


def timestr_to_timestamp(s):
    dt = parseTime2(s)
    if not dt:
        print("Failed to format [%s]" % s)
    return datetime_to_timestamp(dt)


def local_timestamp_to_datetime(s):
    return datetime.fromtimestamp(float(s))


# parse time string to local datetime
def parseTime2(s):
    s = s.strip('"')
    s = s.strip("'")
    try:
        return datetime.strptime(s, '%Y%m%d%H%M%S')
    except:
        pass

    try:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    except:
        pass

    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
    except:
        pass

    try:
        return datetime.strptime(s, '%Y-%m-%d')
    except:
        pass

    try:
        return datetime.strptime(s, '%Y%m%d')
    except:
        pass

    return None


# from local time string to utc timestamp
def timestr_to_utctimestamp(s):
    return datetime_to_utctimestamp(parseTime2(s))


def utc_timestamp_to_local_timestamp(s):
    return datetime_to_timestamp(utctimestamp_to_local_datetime(s))


def timestamp_to_datetime(s):
    return datetime.fromtimestamp(float(s))


g_action_map = {
    ('time_str', 'utc_timestamp'): timestr_to_utctimestamp,
    ('time_str', 'local_timestamp'): timestr_to_timestamp,
    ('time_str', 'local_datetime'): parseTime2,
    ('utc_timestamp', 'local_datetime'): utctimestamp_to_local_datetime,
    ('utc_timestamp', 'local_timestamp'): utc_timestamp_to_local_timestamp,
    ('local_timestamp', 'utc_timestamp'): local_timestamp_to_utctimstamp,
    ('local_timestamp', 'datetime'): local_timestamp_to_datetime,
    ('timestamp', 'datetime'): timestamp_to_datetime,
}


def help_msg():
    msg = ['tools.py [-h] -f format1 -t format2 -s str\n\nSupport transformation list:']
    for k in g_action_map.keys():
        msg.append('\t%s ==> %s' % (k[0], k[1]))
    return '\n'.join(msg)


def help():
    """
    python2.7 tools.py -s '1562490000.0'  -f utc_timestamp -t local_datetime 
    2019-07-08 01:00:00
    
    python2.7 tools.py -s '2019-07-08 01:00:00'  -f time_str -t local_timestamp
    1562518800.0
    
    python2.7 tools.py -s '2019-07-08 01:00:00'  -f time_str -t utc_timestamp  
    1562490000.0
    
    python2.7 tools.py -s '2019-07-08 01:00:00'  -f time_str -t local_datetime
    2019-07-08 01:00:00
    
    python2.7 tools.py -s 1562518800.0  -f local_timestamp -t utc_timestamp
    1562490000.0
    """
    print(help_msg())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage=help_msg())
    parser.add_argument('-f', '--from', dest='from_', type=str, required=True,
                        choices=('time_str', 'timestamp', 'utc_timestamp', 'local_timestamp'))
    parser.add_argument('-t', '--to', dest='to_', type=str, required=True,
                        choices=('utc_timestamp', 'local_timestamp', 'local_datetime', 'datetime'))
    parser.add_argument('-s', '--str', type=str, required=True, help='the string to be converted')
    args = parser.parse_args()

    key = args.from_, args.to_

    if key not in g_action_map:
        print("Do not support (from: %s, to: %s)" % key)
        help()
        exit(1)

    print(g_action_map[key](args.str))
