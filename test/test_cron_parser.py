import unittest
import cron_parser
from cron_parser.exceptions import (
    InvalidCronValueError,
    InvalidCronExpressionError
)


class CronParserTest(unittest.TestCase):
    def test_digit_input(self):
        expected = {
            "minute": [5],
            "hour": [1],
            "day_of_month": [6],
            "month": [11],
            "day_of_week": [3],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("5 1 6 11 3 /usr/bin/find")
        )

    def test_all_input(self):
        expected = {
            "minute": [i for i in range(0,60)],
            "hour": [i for i in range(0, 24)],
            "day_of_month": [i for i in range(1, 32)],
            "month": [i for i in range(1, 13)],
            "day_of_week": [i for i in range(1, 8)],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("* * * * * /usr/bin/find")
        )

    def test_range(self):
        expected = {
            "minute": [i for i in range(1,31)],
            "hour": [i for i in range(1, 4)],
            "day_of_month": [i for i in range(1, 14)],
            "month": [i for i in range(1, 3)],
            "day_of_week": [i for i in range(1, 6)],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1-30 1-3 1-13 1-2 1-5 /usr/bin/find")
        )

    def test_list(self):
        expected = {
            "minute": [1,30],
            "hour": [1,3],
            "day_of_month": [1,13],
            "month": [1,2],
            "day_of_week": [1,5],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1,30 1,3 1,13 1,2 1,5 /usr/bin/find")
        )

    def test_list_with_range(self):
        expected = {
            "minute": [1,2,3,4,5,30],
            "hour": [1,3,4,5],
            "day_of_month": [1,2,13],
            "month": [1,2,3,4,5],
            "day_of_week": [1,2,4,5],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1-5,30 1,3-5 1-2,13 1,2-5 1-2,4-5 /usr/bin/find")
        )

    def test_step(self):
        expected = {
            "minute": [0,20,40],
            "hour": [4,8,12,16,20],
            "day_of_month": [10,20,30],
            "month": [4,8,12],
            "day_of_week": [4,5,6,7],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("*/20 4/4 */10 4/4 4/1 /usr/bin/find")
        )

    def test_step_with_range(self):
        expected = {
            "minute": [0,5,10,15,20,25,30],
            "hour": [4,8,12,16],
            "day_of_month": [1,3,5,7],
            "month": [1,2,3],
            "day_of_week": [1,3,5],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("0-30/5 4-16/4 1-7/2 1-3/1 1-5/2 /usr/bin/find")
        )

    def test_weekday(self):
        expected = {
            "minute": [1],
            "hour": [1],
            "day_of_month": ["Nearest weekday to the 6 of the month"],
            "month": [1],
            "day_of_week": [1],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1 1 6W 1 1 /usr/bin/find")
        )

    def test_weekday_names(self):
        expected = {
            "minute": [1],
            "hour": [1],
            "day_of_month": [1],
            "month": [1],
            "day_of_week": [2,6],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1 1 1 1 MON,FRI /usr/bin/find")
        )

    def test_month_names(self):
        expected = {
            "minute": [1],
            "hour": [1],
            "day_of_month": [1],
            "month": [1,2,3],
            "day_of_week": [1],
            "command": ["/usr/bin/find"]
        }
        self.assertEqual(
            expected,
            cron_parser.parse_cron("1 1 1 JAN-MAR 1 /usr/bin/find")
        )

    def test_table_output(self):
        expected = [
            "minute        5",
            "\n",
            "hour          1",
            "\n",
            "day of month  6",
            "\n",
            "month         11",
            "\n",
            "day of week   3",
            "\n",
            "command       /usr/bin/find",
        ]
        cron_data = cron_parser.parse_cron("5 1 6 11 3 /usr/bin/find")
        self.assertEqual(
            "".join(expected),
            cron_parser.generate_table(cron_data)
        )
    
    def test_incomplete_input(self):
        # Parse an argument with only 5 of the 6 required fields
        with self.assertRaises(InvalidCronExpressionError) as cm:
            cron_parser.parse_cron("1 1 6W 1 1")

        self.assertEqual
        (
            "Please parse an argument in the format"
            " <minute> <hour> <day of month> <month> <day of week> <command>",
            str(cm.exception)
        )


if __name__ == '__main__':
    unittest.main()