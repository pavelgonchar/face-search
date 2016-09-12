import skimage.io
from skimage.transform import resize
import tensorflow as tf
import numpy as np
import sys
import csv
import argparse
writer = csv.writer(sys.stdout)
from vggface import Model as vggface

def run(args):
    images = tf.placeholder("float", [None, 224, 224, 3])

    m = vggface()
    m.build(images)
    fc7 = m.relu7

    init_op = tf.group(tf.initialize_all_variables(),
                       tf.initialize_local_variables())

    with tf.Session() as sess:
        sess.run(init_op)

        input = skimage.io.imread(args.input) / 255.0
        input = resize(input, (224, 224))
        input = np.expand_dims(input, 0)

        output = sess.run(fc7, feed_dict={images: input})

        writer.writerow(output[0])


def parse_args():
    parser = argparse.ArgumentParser(description='Options ')
    parser.add_argument('--input', type=str, default='mr_bean.jpg')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    run(args)
