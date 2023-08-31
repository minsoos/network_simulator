import random
def transform_time(step, time_beg, time_end):
    beg_list = time_beg.split(":")
    end_list = time_end.split(":")
    sec_beg = int(beg_list[0])*60 + int(beg_list[1])
    sec_end = int(end_list[0])*60 + int(end_list[1])
    intervals = (sec_end-sec_beg)/100
    time_aux = sec_beg+int(intervals*(step + random.random()))
    hour = str(time_aux//60)
    minute = str(time_aux%60)
    if len(hour) == 1:
        hour = "0"+hour
    if len(minute) == 1:
        minute = "0"+minute
    real_time = hour+":"+minute
    return real_time