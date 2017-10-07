historical_past_small_emas = []
historical_past_big_emas = []
historical_macds = []
historical_signal_lines = []

CURRENT = 0
SMALL_EMA_VAL = 12
BIG_EMA_VAL = 26
SIGNAL_LINE_VAL = 9

def initialize():
    closing_day_averages = [459.99,448.85,446.06,450.81,442.8,448.97,444.57,441.4,430.47,420.05,431.14,425.66,430.58,431.72,437.87,428.43,428.35,432.5,443.66,455.72,454.49,452.08,452.73,461.91,463.58,461.14,452.08,442.66,428.91,429.79,431.99,427.72,423.2,426.21,426.98,435.69,434.33,429.8,419.85,426.24,402.8,392.05,390.53,398.67,406.13,405.46,408.38,417.2,430.12,442.78,439.29,445.52,449.98,460.71,458.66,463.84,456.77,452.97,454.74,443.86,428.85,434.58,433.26,442.93,439.66,441.35]
    closing_day_averages = closing_day_averages[::-1]
    generate_initial_signal_lines(closing_day_averages)
    print(historical_past_small_emas)
    print(historical_past_big_emas)
    print(historical_macds)
    print(historical_signal_lines)


def fast_forward(list_of_closing_prices):
    size = len(list_of_closing_prices)
    for i in range(size):
        generate_next_day_valeus(list_of_closing_prices[size-i-1])

def generate_next_day_values(closing_price):
    historical_past_small_emas.append(generate_next_ema(historical_past_small_emas[0], closing_price, SMALL_EMA_VAL))
    historical_past_big_emas.append(generate_next_ema(historical_past_big_emas[0], closing_price, BIG_EMA_VAL))
    historical_macds.append(generate_next_macd(historical_past_small_emas[0], historical_past_big_emas[0]))
    historical_signal_lines.append(generate_next_signal_lines(historical_macds, closing_price, SIGNAL_LINE_VAL))

def generate_initial_signal_lines(closing_day_averages):
    generate_current_ema(closing_day_averages, len(closing_day_averages), CURRENT, SMALL_EMA_VAL, historical_past_small_emas)
    generate_current_ema(closing_day_averages, len(closing_day_averages), CURRENT, BIG_EMA_VAL, historical_past_big_emas)
    generate_current_macd(historical_past_small_emas, historical_past_big_emas, historical_macds)
    generate_current_ema(historical_macds[::-1], len(historical_macds), CURRENT, SIGNAL_LINE_VAL, historical_signal_lines)

def generate_next_signal_lines(historical_macds, closing_price, num_of_days):
    generate_next_ema(historical_macds, closing_price, num_of_days)

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

initialize()
