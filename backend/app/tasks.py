from concurrent.futures import ThreadPoolExecutor
from app.model import MlModel
import time
import matplotlib.pyplot as plt

executor = ThreadPoolExecutor(max_workers=4)
TASKS = {}  # task_id -> Future


def long_processing(file_path, result_path, plot_path):
    model = MlModel()
    model.process_file(file_path, result_path)

    with open(result_path, "w") as f:
        f.write("Processed data\nOK")

    # Генерируем график
    plt.plot([1, 2, 3, 4], [1, 4, 2, 9])
    plt.title("Пример графика")
    plt.savefig(plot_path)

    return True