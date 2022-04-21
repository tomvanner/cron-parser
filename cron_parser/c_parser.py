from typing import List
from .exceptions import (
    ValidationError,
    InvalidCronValueError,
    InvalidCronExpressionError,
)
from .config import (
    ALLOWED_VALUES,
    ALLOWED_CHARS,
    DAY_NAMES,
    MONTH_NAMES
)


def get_expression_values(
    expression: str,
    allowed_chars: List[str],
    allowed_values: List[str]
) -> List[str]:
    """Get all possible values for the given attribute subexpression. E.g.
        get_attribute_values('1-3', [',', '-', '*', '/'], [1,2,3,4,5,6,7])
        would return [1,2,3].

    Arguments:
        expression -- The cron subexpression part to parse. E.g. */15.
        allowed_chars -- A list of allowed subexpression chars for the
            given attribute. E.g. [',', '-', '*', '/'] for hour.
        allowed_values -- A list of allowed values for the given attribute.
            E.g. [1,2,3,4,5,6,7] for day of the week.

    Raises:
        InvalidCronExpressionError: Raised if the input expression is invalid.

    Returns:
        A list of all possible values for the expression.
    """

    # Handle weekday expression
    if "W" in expression and "W" in allowed_chars:
        day_of_month = expression.split("W")
        if len(day_of_month) != 2:
            raise InvalidCronExpressionError(
                "Please enter a weekday expression in the format"
                " <day of month>W"
            )
        return [get_nearest_weekday(day_of_month[0], allowed_values)]

    # Handle step expression
    if "/" in expression and "/" in allowed_chars:
        start, end = expression.split("/")
        return parse_step(start, end, allowed_values)

    # Handle list expression
    if "," in expression and "," in allowed_chars:
        values = expression.split(",")
        return expand_list_values(values, allowed_values)

    # Handle range expression
    if "-" in expression and "-" in allowed_chars:
        start, end = expression.split("-")
        return generate_range(start, end, allowed_values)

    # Handle "all" expression
    if expression == "*" and "*" in allowed_chars:
        return allowed_values

    # Handle "No specified value" expression
    if expression == "?" and "?" in allowed_chars:
        return ["N/A"]

    # If none of the above match the expression, maybe it is an integer
    try:
        expression = int(expression)
    except ValueError:
        raise InvalidCronExpressionError(
            "The expression entered is invalid or not yet accounted for"
        )
    if expression not in allowed_values:
        raise InvalidCronExpressionError(
            "Please enter a valid value for the field"
        )
        
    return [expression]


def get_nearest_weekday(day_of_month: int, allowed_values: List[str]) -> str:
    """Get nearest weekday for the day of the month.

    Arguments:
        day_of_month -- The day of the month to find the closest weekday to.
        allowed_values -- A list of allowed values for the given attribute.

    Raises:
        Exception: _description_

    Returns:
        A string containing the the nearest weekday.
    """
    try:
        day_of_month = int(day_of_month)
    except ValueError:
        raise InvalidCronValueError(
            "Please enter an integer for the day of month part of"
            " the weekday expression"
        )
    if day_of_month not in allowed_values:
        raise InvalidCronValueError("Please enter a valid day of the month")
    
    return f"Nearest weekday to the {str(day_of_month)} of the month"


def expand_list_values(elements: List[str], allowed_values: List[str]) -> List[int]:
    """Get list of expanded values for the given cron list expression.

    Arguments:
        elements -- A list of integer values or a list of ranges.
            E.g. [1,2,3,4] or [1,2,3-5].
        allowed_values -- A list of allowed output values.

    Raises:
        InvalidCronValueError: Raised if any of the passed list elements
            are not integers/cannot be parsed.

    Returns:
        A list of expanded values.
    """
    output = []
    for value in elements:
        if "-" in value:
            start_val, end_val = value.split("-")
            output = output + generate_range(start_val, end_val, allowed_values)
            continue
        try:
            value = int(value)
        except ValueError:
            raise InvalidCronValueError(
                "Please enter a list expression with either comma"
                " separated integers or ranges"
            )
        output.append(value)
    output.sort()
    return output


def generate_range(start: int, end: int, allowed_values: List[str]) -> List[int]:
    """Generate a list of values from start to end inclusive.

    Arguments:
        start -- The start of the range.
        end -- The end of the range.
        allowed_values -- List of allowed output values.

    Raises:
        InvalidCronExpressionError: Raised if the range is in an incorrect
            format, or if the range bounds are invalid.

    Returns:
        A list containing every value between start and end inclusive.
    """
    try:
        start, end = int(start), int(end)
    except ValueError:
        raise InvalidCronExpressionError(
            "Please enter a range in the format n-k where"
            " n and k are integers"
        )
    
    if end < start:
        raise InvalidCronValueError(
            "Please enter a range where the start value is less"
            " than the end value"
        )
    
    # Locate the list indexes of the start and end values
    start_index, end_index = allowed_values.index(start), allowed_values.index(end)
    return [i for i in allowed_values[start_index:end_index + 1]]


def parse_step(
    start_exp: str,
    increment: int,
    allowed_values: List[str]
) -> List[int]:
    """Generate list of values in incremental steps from start value.

    Arguments:
        start_exp -- A string containing the start expression;
            either *, - or a digit.
        increment -- The value to increment by.
        allowed_values -- List of allowed output values.

    Raises:
        InvalidCronValueError

    Returns:
        A list containing all of the incremented step values.
    """
    try:
        increment_val = int(increment)
    except ValueError:
        raise InvalidCronValueError("Please enter an integer increment step value")

    # Increments of n where n_i is every allowed_values element
    if start_exp == "*":
        return [i for i in allowed_values if i % increment_val == 0]

    # Every n in a range of values, e.g. every 5 minutes between 0-30 minutes
    if "-" in start_exp:
        start, end = start_exp.split("-")
        ranges = generate_range(start, end, allowed_values)
        return ranges[0::increment_val]

    # Every n from start value
    try:
        start_exp = int(start_exp)
    except ValueError:
        raise InvalidCronValueError(
            "Please enter a step start value containing a digit, * or range"
        )
    try:
        start_index = allowed_values.index(start_exp)
        return [i for i in allowed_values[start_index:] if i % increment_val == 0]
    except ValueError:
        raise InvalidCronValueError(
            "The step start expression is not in the allowed values"
        )


def parse_cron(cron_exp: str) -> dict:
    """Entry point for parsing a space separated cron expression.

    Arguments:
        cron_exp -- A string containing the cron expression.

    Raises:
        ValidationError: Raised if any part of the cron expression is invalid.

    Returns:
        A dict containing a list of values for each attribute i.e.
        minute, hour, day of month, month, day of week.
    """
    try:
        minute, hour, day_of_month, month, day_of_week, cmd = cron_exp.split()
    except ValueError:
        raise InvalidCronExpressionError(
            "Please parse an argument in the format"
            " <minute> <hour> <day of month> <month> <day of week> <command>"
        )

    # Convert any entered day/month names to their numeric equivalent
    day_of_week_num = names_to_nums(
        day_of_week,
        dict(zip(DAY_NAMES, ALLOWED_VALUES["day_of_week"]))
    )
    month_num = names_to_nums(
        month,
        dict(zip(MONTH_NAMES, ALLOWED_VALUES["month"]))
    )

    # Store each output list in a dictonary
    output = {
        "minute": get_expression_values(
            minute,
            ALLOWED_CHARS["minute"],
            ALLOWED_VALUES["minute"]
        ),
        "hour": get_expression_values(
            hour,
            ALLOWED_CHARS["hour"],
            ALLOWED_VALUES["hour"]
        ),
        "day_of_month": get_expression_values(
            day_of_month,
            ALLOWED_CHARS["day_of_month"],
            ALLOWED_VALUES["day_of_month"]
        ),
        "month": get_expression_values(
            month_num,
            ALLOWED_CHARS["month"],
            ALLOWED_VALUES["month"]
        ),
        "day_of_week": get_expression_values(
            day_of_week_num,
            ALLOWED_CHARS["day_of_week"],
            ALLOWED_VALUES["day_of_week"]
        ),
        "command": [cmd]
    }
    return output


def names_to_nums(expression, in_map):
    """Converts any verbose day/month names to their associated numbers."""
    for name, num in in_map.items():
        expression = expression.replace(name, str(num))
    return expression


def generate_table(data: dict, col_width: int = 13) -> str:
    """Generate a table with the first 14 columns containing the key/field name
        with the remaining space containing its values. E.g.
        minute: 0 15 30 45  
        hour: 0  
        day of month: 1 15  
        month: 1 2 3 4 5 6 7 8 9 10 11 12  
        day of week: 1 2 3 4 5  
        command: /usr/bin/find

    Arguments:
        data -- A dict containing the key-value pairs to display.

    Keyword Arguments:
        col_width -- How many spaces wide the column should be. (default: {13})

    Returns:
        A string containing the formatted table
    """
    table = []
    num_fields = len(data)
    for i, (field, values) in enumerate(data.items()):
        filtered_field = field.replace("_", " ")
        table.append(f"{filtered_field.ljust(col_width)} {' '.join(str(i) for i in values)}")
        if i != num_fields - 1:
            table.append("\n")
    return "".join(table)

