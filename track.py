import json
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image


class Tracker():

    def __init__(self, json_save_pth):
        self.save_pth = json_save_pth
        self.tracking_metrics = {}
    
    def log_metrics(self, epoch, metric_names:list, metric_values:list):
        epoch_dict = {}
        for name, value in zip(metric_names, metric_values):
            epoch_dict[name] = value
        self.tracking_metrics[str(epoch)] = epoch_dict
    
    def save_metrics(self, save_path=None):
        if not save_path:
            save_path = self.save_pth
        with open(save_path, 'w') as f:
            json.dump(self.tracking_metrics, f)

    def load_metrics(self, load_path):
        with open(load_path, 'r') as f:
            data = json.load(f)
        return data
    
    def graph_metrics(self, metrics:dict):
        metric_names = list(next(iter(metrics.values())).keys())
        epochs = sorted([int(e) for e in metrics.keys()])
        str_epochs = [str(e) for e in epochs]
        images = []
        for name in metric_names:
            values = [metrics[epoch][name] for epoch in str_epochs]
            plt.figure()
            plt.plot(epochs, values, marker='o')
            plt.xlabel('Epoch')
            plt.ylabel(name)
            plt.title(f'{name} Over Epochs')
            plt.grid(True)
            buf = BytesIO()
            plt.show()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)
            images.append(img)
            plt.close()
        return images


if __name__ == "__main__":
    t = Tracker("metrics.json")
    for epoch in range(5):
        metric_names = ["loss", "accuracy"]
        metric_values = [1.0 / (epoch + 1), 0.5 + 0.1 * epoch]
        t.log_metrics(epoch, metric_names, metric_values)
    t.save_metrics()
    loaded_metrics = t.load_metrics("metrics.json")
    imgs = t.graph_metrics(loaded_metrics)
