import pandas as pd
import numpy as np

data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")

X = data['embedding'].to_list()
numpy_array = np.fromstring(X[0], sep=',')
print(numpy_array)