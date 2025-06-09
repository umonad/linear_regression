import sys

# prediction model
def estimate_price(km, a, b):
    return a * km + b

if __name__ == "__main__":
    estimate_price(sys.argv[1], sys.argv[2], sys.argv[3])
