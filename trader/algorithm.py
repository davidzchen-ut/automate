historical_past_small_emas = []
historical_past_big_emas = []
historical_macds = []
historical_signal_lines = []

CURRENT = 0
SMALL_EMA_VAL = 12
BIG_EMA_VAL = 26
SIGNAL_LINE_VAL = 9

def initialize(closing_day_averages):
    closing_day_averages = [float(i) for i in closing_day_averages] 
    generate_initial_signal_lines(closing_day_averages)
    print(historical_past_small_emas)
    print(historical_past_big_emas)
    print(historical_macds)
    print(historical_signal_lines)

def fast_forward(value):
    previous = historical_macds[len(historical_macds) - 1] - historical_signal_lines[len(historical_signal_lines) - 1]
    generate_next_day_values(value)
    current = historical_macds[len(historical_macds) - 1] - historical_signal_lines[len(historical_signal_lines) - 1]
    should_buy = (previous < 0) and (current > 0)
    should_sell = (previous > 0) and (current < 0)
    do_nothing = not should_buy and not should_sell
    return should_buy, should_sell, do_nothing

def generate_next_day_values(closing_price):
    historical_past_small_emas.append(generate_next_ema(historical_past_small_emas[len(historical_past_small_emas)-1], closing_price, SMALL_EMA_VAL))
    historical_past_big_emas.append(generate_next_ema(historical_past_big_emas[len(historical_past_big_emas)-1], closing_price, BIG_EMA_VAL))
    historical_macds.append(generate_next_macd(historical_past_small_emas[len(historical_past_small_emas)-1], historical_past_big_emas[len(historical_past_big_emas)-1]))
    historical_signal_lines.append(generate_next_signal_lines(historical_signal_lines[len(historical_signal_lines)-1], historical_macds[len(historical_macds)-1], SIGNAL_LINE_VAL))

def generate_initial_signal_lines(closing_day_averages):
    generate_current_ema(closing_day_averages, len(closing_day_averages), CURRENT, SMALL_EMA_VAL, historical_past_small_emas)
    generate_current_ema(closing_day_averages, len(closing_day_averages), CURRENT, BIG_EMA_VAL, historical_past_big_emas)
    generate_current_macd(historical_past_small_emas, historical_past_big_emas, historical_macds)
    generate_current_ema(historical_macds[::-1], len(historical_macds), CURRENT, SIGNAL_LINE_VAL, historical_signal_lines)

def generate_next_signal_lines(historical_macds, closing_price, num_of_days):
    return generate_next_ema(historical_macds, closing_price, num_of_days)

def generate_current_macd(small_emas, big_emas, macds):
    size = len(big_emas)
    for i in range(size):
        print("small: " + str(small_emas[i+(BIG_EMA_VAL-SMALL_EMA_VAL)]))
        print("large: " + str(big_emas[i]))
        macds.append(generate_next_macd(small_emas[i+(BIG_EMA_VAL-SMALL_EMA_VAL)], big_emas[i]))

def generate_next_macd(small_emas, big_emas):
    return small_emas - big_emas 

def generate_initial_ema(closing_day_averages, days_previous, num_of_days):
    initial_ima = generate_ima(closing_day_averages, days_previous, num_of_days)
    return initial_ima
    
def generate_next_ema(initial_ema, closing_price, num_of_days):
    multiplier = (2 / (num_of_days + 1))
    ema = ((closing_price - initial_ema) * multiplier + initial_ema)
    return ema

def generate_current_ema(closing_day_averages, from_index, to_index, num_of_days, passed_array):
    ema = generate_initial_ema(closing_day_averages, from_index - num_of_days, num_of_days)
    passed_array.append(ema)
    if (from_index - to_index - num_of_days > 0):
        for i in range(from_index - to_index - num_of_days):
            ema = generate_next_ema(ema, closing_day_averages[from_index - num_of_days - i - 1], num_of_days)
            passed_array.append(ema)

def generate_ima(closing_day_averages, days_previous, num_of_days):
    total_sum = sum(closing_day_averages[days_previous : days_previous + num_of_days])
    ima = total_sum / num_of_days
    return ima
