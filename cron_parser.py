from sys import argv

def parse_expression(expression, allowed_chars, allowed_values):
    """
    Parameters:
    expression (string): The day of the month to find the closest weekday to
    allowed_chars (list): The list of characters which the given expression can contain
    allowed_values (list): The list of values which the expression can contain

    Returns:
    A list containing the calculated output
    """

    # Handle weekday expression
    if "W" in expression and "W" in allowed_chars:
        day_of_month = expression.split("W")

        if len(day_of_month) != 2:
            raise Exception("Please enter a weekday expression in the format <day of month>W")

        return parse_weekday(day_of_month[0], allowed_values)

    # Handle step expression
    if "/" in expression and "/" in allowed_chars:
        start, end = expression.split("/")
        return parse_step(start, end, allowed_values)

    # Handle list expression
    if "," in expression and "," in allowed_chars:
        values = expression.split(",")
        return parse_list(values, allowed_values)

    # Handle range expression
    if "-" in expression and "-" in allowed_chars:
        start, end = expression.split("-")
        return parse_range(start, end, allowed_values)

    # Handle "all" expression
    if expression == "*" and "*" in allowed_chars:
        return allowed_values

    # Handle "No specified value" expression
    if expression == "?" and "?" in allowed_chars:
        return ["N/A"]

    # If none of the above match the expression, maybe it is a digit
    try:
        expression = int(expression)
    except ValueError:
        raise Exception("The expression entered is invalid or not yet accounted for")
    
    if expression not in allowed_values:
        raise Exception("Please enter a valid value for the field")

    return [expression]

def parse_weekday(day_of_month, allowed_values):
    """
    Parameters:
    day_of_month (int): The day of the month to find the closest weekday to
    allowed_values (list): The list of values which the output numbers must be in bounds of

    Returns:
    A string containing the weekday which is closest to the entered day of the month
    """
    try:
        day_of_month = int(day_of_month)
    except ValueError:
        raise Exception("Please enter an integer for the day of month part of the weekday expression")

    if day_of_month not in allowed_values:
        raise Exception("Please enter a valid day of the month")
    return ["Nearest weekday to the " + str(day_of_month) + " of the month"]

def parse_list(elements, allowed_values):
    """Generates a list of values from a series of individual values/expressions
    Parameters:
    elements (list): The values the list should contain; each element can be either an integer or a range
    allowed_values (list): The list of values which the output numbers must be in bounds of

    Returns:
    A list of values
    """
    output = []

    for value in elements:
        if "-" in value:
            start_val, end_val = value.split("-")
            output = output + parse_range(start_val, end_val, allowed_values)
            continue
        try:
            value = int(value)
        except ValueError:
            raise Exception("Please enter a list expression with either comma separated integers or ranges")
        
        output.append(value)

    output.sort()

    return output

def parse_range(start, end, allowed_values):
    """Generates a list of values from a start to end inclusive
    Parameters:
    start (int): The value the list should start from
    end (int): The value the list should end with
    allowed_values (list): The list of values which the output numbers must be in bounds of

    Returns:
    A list of values
    """
    try:
        start, end = int(start), int(end)
    except ValueError:
        raise Exception("Please enter a range in the format n-k where n and k are integers")
    
    if end < start:
        raise Exception("Please enter a range where the start value is less than the end value")
    
    # Locate the list indexes of the start and end values
    start_index, end_index = allowed_values.index(start), allowed_values.index(end)

    return [i for i in allowed_values[start_index:end_index + 1]]

def parse_step(start_exp, increment_exp, allowed_values):
    """Generates a list of values in incrementing steps from the start value
    Parameters:
    start_exp (string): A string containing the start expression; either *, - or digit
    increment_exp (int): The increment value
    allowed_values (list): The list of values which the output numbers must be in bounds of

    Returns:
    A list of values
    """
    try:
        increment_exp = int(increment_exp)
    except ValueError:
        raise Exception("Please enter an integer step value")

    # Every n minutes
    if start_exp == "*":
        return [i for i in allowed_values if i % increment_exp == 0]

    # Every n minutes in a range of values, e.g. every 5 minutes between 0-30 minutes
    if "-" in start_exp:
        start, end = start_exp.split("-")
        ranges = parse_range(start, end, allowed_values)

        return ranges[0::increment_exp]

    # Every n minutes from start value
    try:
        start_exp = int(start_exp)
    except ValueError:
        raise Exception("Please enter a start value containing a digit, * or range")
    
    start_index = allowed_values.index(start_exp)

    return [i for i in allowed_values[start_index:] if i % increment_exp == 0]

def parse_cron(cron):
    """Entry point for handling a space separated cron expression
    Parameters:
    cron (string): A string containing the cron expression

    Returns:
    A dictonary containing a list of selected values for each field
    """
    try:
        minute, hour, day_of_month, month, day_of_week, cmd = cron.split()
    except ValueError:
        raise Exception("Please parse an argument in the format <minute> <hour> <day of month> <month> <day of week> <command>")
    
    allowed_values = {
        "minute": [i for i in range(0, 60)],
        "hour": [i for i in range(0, 24)],
        "day_of_month": [i for i in range(1, 32)],
        "month": [i for i in range(1, 13)],
        "day_of_week": [i for i in range(1, 8)]
    }

    allowed_chars = {
        "minute": [",", "-", "*", "/"],
        "hour": [",", "-", "*", "/"],
        "day_of_month": [",", "-", "*", "?", "/", "W"],
        "month": [",", "-", "*", "/"],
        "day_of_week": [",", "-", "*", "?", "/"]
    }

    day_names = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP","OCT", "NOV", "DEC"]

    # Convert any entered day/month names to their numeric equivalent
    dow = names_to_nums(day_of_week, dict(zip(day_names, allowed_values["day_of_week"])))
    m = names_to_nums(month, dict(zip(month_names, allowed_values["month"])))

    # Store each output list in a dictonary
    output = {
        "minute": parse_expression(minute, allowed_chars["minute"], allowed_values["minute"]),
        "hour": parse_expression(hour, allowed_chars["hour"], allowed_values["hour"]),
        "day_of_month": parse_expression(day_of_month, allowed_chars["day_of_month"], allowed_values["day_of_month"]),
        "month": parse_expression(m, allowed_chars["month"], allowed_values["month"]),
        "day_of_week": parse_expression(dow, allowed_chars["day_of_week"], allowed_values["day_of_week"]),
        "command": [cmd]
    }

    return output

def names_to_nums(expression, in_map):
    for name, num in in_map.items():
        expression = expression.replace(name, str(num))
    
    return expression


def main():
    if len(argv) != 2:
        raise Exception("Please pass the cron expression in a single argument")
    
    cron = argv[1].strip()
    output_data = parse_cron(cron)
    print(generate_table(output_data))

def generate_table(data, col_width = 13):
    """Generates a table with the first 14 columns containing the field name and the rest containing the values
    Parameters:
    data (dict): A dictonary containing field value pairs
    col_width (int): The width of the field column

    Returns:
    A string containing the formatted table
    """
    table = ""

    for field, values in data.items():
        filtered_field = field.replace("_", " ")
        table += filtered_field.ljust(col_width) + " " + " ".join(str(i) for i in values)
        table += "\n"
    
    return table

if __name__ == "__main__":
    main()