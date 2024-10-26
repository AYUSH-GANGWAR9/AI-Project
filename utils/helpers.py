# helpers.py

def log_metrics(metrics):
    """ Log the metrics for monitoring and debugging. """
    print("Metrics Report:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

def calculate_average(values):
    """ Calculate the average of a list of values. """
    if not values:
        return 0
    return sum(values) / len(values)

def save_results_to_file(results, filename):
    """ Save simulation results to a specified file. """
    with open(filename, 'w') as file:
        for result in results:
            file.write(f"{result}\n")
    print(f"Results saved to {filename}")
