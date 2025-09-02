import sys


if len(sys.argv) < 3:
    print("Usage: python test.py <name1> <name2>")
else:
    encryption_key = sys.argv[1]
    time_sleep = int(sys.argv[2])
    print(f"Hello {encryption_key} and {time_sleep}")
