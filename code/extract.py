import tensorflow as tf
from tensorflow.python.framework import ops, dtypes
import numpy as np
import glob
import sys
import csv
from vggface import Model as vggface

filenames = sorted(glob.glob("../images/*/*/*.jpg"))
print("%s images found" % len(filenames))

batch_size = 1
num_epochs = 1


def read_my_file_format(filename_queue, randomize=True):
    reader = tf.WholeFileReader()
    file_contents = tf.read_file(filename_queue[0])
    uint8image = tf.image.decode_jpeg(file_contents, channels=3)
    uint8image = tf.expand_dims(uint8image, 0)
    uint8image = tf.image.resize_bilinear(uint8image, (224, 224))
    uint8image = tf.reshape(uint8image, (224, 224, 3))
    uint8image = tf.random_crop(uint8image, (224, 224, 3))

    if randomize:
        uint8image = tf.image.random_brightness(uint8image, max_delta=0.4)
        uint8image = tf.image.random_contrast(uint8image, lower=0.6, upper=1.4)
        uint8image = tf.image.random_hue(uint8image, max_delta=0.04)
        uint8image = tf.image.random_saturation(
            uint8image, lower=0.6, upper=1.4)

    float_image = tf.div(tf.cast(uint8image, tf.float32), 255)
    return float_image, filename_queue[1]


def input_pipeline(filenames, batch_size, num_epochs=None):
    filenames_tensor = ops.convert_to_tensor(filenames, dtype=dtypes.string)
    labels_tensor = ops.convert_to_tensor(filenames, dtype=dtypes.string)

    filename_queue = tf.train.slice_input_producer([filenames_tensor, labels_tensor],
                                                   num_epochs=num_epochs,
                                                   shuffle=False)
    example, label = read_my_file_format(filename_queue, randomize=True)
    example_batch, label_batch = tf.train.batch(
        [example, label], batch_size=batch_size, capacity=batch_size)

    return example_batch, label_batch


images, labels = input_pipeline(filenames, batch_size, num_epochs=num_epochs)

m = vggface()
m.build(images)
fc7 = m.relu7

init_op = tf.group(tf.initialize_all_variables(),
                       tf.initialize_local_variables())

sess = tf.Session()

sess.run(init_op)

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

try:
    while not coord.should_stop():
        fc7_, labels_ = sess.run([fc7, labels])

        for i in range(batch_size):
            row = [str(labels_[i])] + list(fc7_[i])
            with open('../data/features.csv', 'ab') as f:
                writer = csv.writer(f)
                writer.writerow(row)

except tf.errors.OutOfRangeError:
    print('Done')
finally:
    coord.request_stop()

coord.join(threads)
sess.close()
