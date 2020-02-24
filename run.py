#!\bin\python3
# Runs whatever is the latest thing being developed

import app
import matplotlib.pyplot as plt


dataset = app.GeneratedDataset(
    size=3,
    generator_options={}
)
dataset.load_or_generate_and_save()
dataset.check_dataset_visually()
