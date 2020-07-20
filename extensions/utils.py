from . import jalali
from django.utils import timezone

def persian_number_converter(somestr):
    numbers = {
        "1":"۱",
        "0":"۰",
        "2":"۲",
        "3":"۳",
        "4":"۴",
        "5":"۵",
        "6":"۶",
        "7":"۷",
        "8":"۸",
        "9":"۹",
    }


    #in dictionary if we wnat to access to key and value so we need to use "imtems"
    for e, p in numbers.items():
        somestr = somestr.replace(e, p)
    return somestr

def jalali_converter(time):
    af_month = ["حمل", "ثور", "جوزا", "سرطان", "اسد", "سنبله", "میزان", "عقرب", "قوس", "جدی", "دلو", "حوت"]
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    #i wnna enumerate the above line but because time_to_tuple is a tuple it means that is is immutable 
    # so i need to change to a list first
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(af_month):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f"{time_to_list[2]},{time_to_list[1]},{time_to_list[0]}, ساعت {time.hour}:{time.minute}"
    return persian_number_converter(output)