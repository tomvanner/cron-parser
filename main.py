import sys
import cron_parser


def main() -> int:
    """Prints a human-readable table explaining the passed cron expression."""
    if len(sys.argv) != 2:
        raise Exception("Please pass the cron expression in a single argument")
    cron = sys.argv[1].strip()
    output_data = cron_parser.parse_cron(cron)
    print(cron_parser.generate_table(output_data))
    return 0


if __name__ == "__main__":
    sys.exit(main())