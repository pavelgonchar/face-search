import numpy as np
import tensorflow as tf
import sys
import csv
import glob
import math
import click
writer = csv.writer(sys.stdout)

input_csv = np.array(sys.stdin.readline().split(',')).astype('float32')
input_csv = input_csv[0:1000]

input_features = tf.placeholder(
    tf.float32, shape=[None, 1000], name="input_features")
features_batch = tf.placeholder(
    tf.float32, shape=[None, 1000], name="features_batch")

similarity = tf.reduce_sum(tf.square(tf.nn.l2_normalize(
    input_features, 1) - tf.nn.l2_normalize(features_batch, 1)), reduction_indices=1, keep_dims=False)

with tf.Session() as sess:

    labels_filenames = sorted(glob.glob("../db/labels*.npy"))
    features_filenames = sorted(glob.glob("../db/features*.npy"))

    results = []
    with click.progressbar(range(len(labels_filenames)), file=sys.stderr) as bar:
        for c in bar:
            data_labels = np.load(labels_filenames[c])
            data_features = np.load(features_filenames[c])[:,0:1000]

            tile_input_csv = np.tile(input_csv, (len(data_features), 1))
            similarity_ = sess.run(similarity, feed_dict={
                                   input_features: tile_input_csv, features_batch: data_features})
            for i in range(len(data_features)):
                row = [str(data_labels[i])] + [str(similarity_[i])]
                results.append(row)

    results = sorted(results, key=lambda results: float(results[1]))[0:20]
    writer.writerows(results)
