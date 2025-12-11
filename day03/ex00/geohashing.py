import sys
import antigravity

def check_date_format(date):
    parts = date.split('-')
    if len(parts) != 3:
        print("Error: invalid date format (expected YYYY-MM-DD)")
        return (False)
    if not all(p.isdigit() for p in parts):
        print("Error: invalid date format (expected YYYY-MM-DD)")
        return (False)
    if [len(p) for p in parts] != [4, 2, 2]:
        print("Error: invalid date format (expected YYYY-MM-DD)")
        return (False)
    return (True)

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: geohashing.py lattitude longitude YYYY-MM-DD DOW_OPEN")
        sys.exit(1)

    date, dow = sys.argv[3], sys.argv[4]

    if not check_date_format(date):
        sys.exit(1)
    
    lattitude = 0.0;
    longitude = 0.0;

    try:
        lattitude = float(sys.argv[1])
    except ValueError:
        print("Error: Latitude must be a number")
        sys.exit(1)

    try:
        longitude = float(sys.argv[2])
    except ValueError:
        print("Error: Longitude must be a number")
        sys.exit(1)

    antigravity.geohash(lattitude, longitude, '-'.join((date, dow)).encode())
