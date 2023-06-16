# Time to Time converting tool
## what is time-time
`time-time` is a convertor for translating time string to timestamp , or reverse.
You may see many timestamp in your code, or your applications, but you cannot figure out what time it ’s representing. use time-time, it may save your time.


## Compatibility
It's compatible with `Python 3+`

## Uage
```
$ python3 time-time.py -s '1562490000.0'  -f utc_timestamp -t local_datetime
2019-07-08 01:00:00

$ python3 time-time.py -s '2023-03-02 16:00:00' -f time_str -t local_timestamp 
1677744000.0
```

