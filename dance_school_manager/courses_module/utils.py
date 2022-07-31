def get_day_number_by(day_name):
    DAYS_OF_WEEK_TRANSLATION = {
        'Monday': '0',
        'Tuesday': '1',
        'Wednesday': '2',
        'Thursday': '3',
        'Friday': '4',
        'Saturday': '5',
        'Sunday': '6',
    }
    return int(DAYS_OF_WEEK_TRANSLATION[day_name])
