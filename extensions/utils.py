from . import jalali

def jalali_converter(time):
    af_month = ["حمل", "ثور", "جوزا", "سرطان", "اسد", "سنبله", "میزان", "عقرب", "قوس", "جدی", "دلو", "حوت"]
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
    return output