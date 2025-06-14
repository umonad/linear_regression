import sys
import csv


def write_csv(data):
    with open("weights.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def read_csv(filepath):
    x_values, y_values = [], []
    try:
        with open(filepath, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            columns = reader.fieldnames
            if len(columns) < 2:
                print("Error: Need at least 2 columns")
                return None, None

            x_col, y_col = columns[0], columns[1]
            print(f"Using columns: x='{x_col}', y='{y_col}'")
            for row in reader:
                x_values.append(float(row[x_col]))
                y_values.append(float(row[y_col]))
        return x_values, y_values
    except:
        print(f"Error reading CSV")
        return None, None


def estimate_price(km, a, b):
    return a * km + b


if __name__ == "__main__":
    if len(sys.argv) == 2:
        a, b = read_csv("poids.csv")
        if a and b:
            print(estimate_price(float(sys.argv[1]), a[0], b[0]))
