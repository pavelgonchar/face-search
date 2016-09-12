import numpy as np
import glob

filenames = sorted(glob.glob("../data/features.csv.*"))

for file in filenames:
    data_labels = np.genfromtxt(file, delimiter=',', usecols=(0), dtype='str')

    np.save('../db/' + file.split('/')
            [-1].replace('features', 'labels') + '.npy', data_labels)

    data_features = np.genfromtxt(file, delimiter=',')
    data_features = np.delete(data_features, [0], 1)

    np.save('../db/' + file.split('/')[-1] + '.npy', data_features)
