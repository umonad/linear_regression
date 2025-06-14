from p1 import estimate_price, write_csv, read_csv
import matplotlib.pyplot as plt
import csv
import sys
import signal
import os


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)


def siginit():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)


def visualiser_donnees(kms, prices, a, b):
    plt.figure(figsize=(15, 10))
    #                    x, y

    plt.scatter(kms, prices, color="blue", alpha=0.2, s=200)

    km_min = min(kms)
    km_max = max(kms)

    prix_min = estimate_price(km_min, a, b)
    prix_max = estimate_price(km_max, a, b)

    plt.plot(
        [km_min, km_max],
        [prix_min, prix_max],
        color="green",
        linewidth=2,
        label=f"y = {a:.5f}x + {b:.0f}",
    )

    plt.xlabel("Mileage (km)", fontsize=12)
    plt.ylabel("Price (€)", fontsize=12)
    plt.title(
        "Linear Regression: Car Prices based on Mileage",
        fontsize=14,
    )
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


def normalise_z_score(data):
    n = len(data)
    mean = sum(data) / len(data)
    all_ecart = [
        ((i - mean) ** 2) for i in data
    ]  # values - mean to get the deviation from mean
    variance = sum(all_ecart) / n  # sum of deviations from mean / len
    ecartype = variance**0.5  # square root of variance
    # Avoid division by zero
    if ecartype == 0:
        return mean, 0, [0] * n
    normalize = [((i - mean) / ecartype) for i in data]
    return mean, ecartype, normalize


def train_model(epoch, learningRate, kms, prices):
    # We are searching for the model parameters a and b that fit the best
    # y = ax + b  / price = a * km + b   for all x and y / km and price
    # θ1 and θ0 set to zero as specified in the subject
    a_norm, b_norm = 0, 0
    moyen_kms, ecartype_kms, normalise_kms = normalise_z_score(kms)
    moyen_prices, ecartype_prices, normalise_prices = normalise_z_score(prices)
    # Our learning loop
    for _ in range(epoch):
        errora = 0
        errorb = 0
        for km, price in zip(normalise_kms, normalise_prices):
            # tmp_a = learningrate * (1/len(kms or prices) * estimate_price(kms[i],a,b) - prices[i]) *km[i]
            # tmp_b = learningrate * 1/len(kms or prices) * estimate_price(kms[i],a,b) - prices[i]
            prediction = estimate_price(km, a_norm, b_norm)

            error = prediction - price

            errora += error * km
            errorb += error
        errora /= len(kms)
        errorb /= len(kms)

        a_norm -= learningRate * errora
        b_norm -= learningRate * errorb
    # Denormalization of our theta parameters
    a = a_norm * (ecartype_prices / ecartype_kms)
    b = moyen_prices - a * moyen_kms

    return a, b


if __name__ == "__main__":
    # Signal handler
    siginit()
    # HyperParameters:
    a = b = 0
    learningRate = 0.1
    epoch = 100
    kms, prices = 0, 0
    print("""Usage of the programme: prompt :
    - 'start' : take a csv file for the prediction training
    - 'prediction' : take a decimal (x) and return the prediction (y)
    - 'visualisation' : give a graphique visalisation""")
    while KeyboardInterrupt:
        try:
            command = input(">> ").strip().lower()
            if command == "start":
                a = b = 0
                while KeyboardInterrupt:
                    csv_path = input("csv file path >> ")
                    if "csv" not in csv_path:
                        if (
                            csv_path.strip().lower() == "exit"
                            or csv_path.strip().lower() == "quit"
                        ):
                            break
                        print("error : csv file required")
                    else:
                        kms, prices = read_csv(csv_path)
                        if kms and prices:
                            print(
                                f"Model hyperparameters: epoch = {epoch}, learningRate = {learningRate}"
                            )
                            print(
                                f"START: Parameters: a = {a}, b = {b} for training on {csv_path}"
                            )
                            a, b = train_model(epoch, learningRate, kms, prices)
                            print(
                                f"END: Model parameters trained on data from {csv_path}: a = {a:.5f}, b = {b:.0f}"
                            )
                            write_csv([["a", "b"], [a, b]])
                        break
            elif command == "prediction" or command == "p":
                km_input = 0
                if a == 0 and b == 0:
                    print("first 'start' the program with a csv file")
                else:
                    while KeyboardInterrupt:
                        km_input = input("x >>> ").strip().lower()
                        if km_input == "exit" or km_input == "quit":
                            break
                        try:
                            km_input = float(km_input)
                            prix_predit = estimate_price(km_input, a, b)
                            prix_reel = 0
                            for km, price in zip(kms, prices):
                                if km == km_input:
                                    prix_reel = price
                            if prix_reel:
                                erreur = abs(prix_predit - prix_reel)
                                print(
                                    f"Km: {km_input:6.0f} | Real: {prix_reel:4.0f}€ | Predicted: {prix_predit:6.0f}€ | Error: {erreur:6.0f}€"
                                )
                            else:
                                print(
                                    f"Km: {km_input:6.0f} | Predicted: {prix_predit:6.0f}€"
                                )
                        except:
                            print("a decimal number please...")

            elif command == "visualisation" or command == "v":
                if a == 0 and b == 0:
                    print("first 'start' the program with a csv file")
                else:
                    visualiser_donnees(kms, prices, a, b)
            elif command == "quit" or command == "exit":
                break
            else:
                if a and b:
                    print("usage : 'prediction' 'visualisation' 'start'")
                else:
                    print("usage : 'start'")
        except EOFError:
            print("\nNo input detected. Closing...")
            break
        except KeyboardInterrupt:
            print("\nInterruption detected")
            break
    print("see you ;)")


# ERROR:
# Mean absolute deviation: Σ|xi - μ| / n - less used in ML
# ecarts = [abs(i - moy)for i in data] absolute deviation X
# ecartype = sum(ecarts)/len(data) mean absolute deviation X

# CORRECTION:
# Standard deviation: √(Σ(xi - μ)² / n) - measures dispersion


# Other normalization method
# def normalisation_min_max(data):
#     """Normalizes data between 0 and 1"""
#     min_val = min(data)
#     max_val = max(data)

#     if max_val == min_val:
#         return [0.5] * len(data)

#     return [(x - min_val) / (max_val - min_val) for x in data]
