import os
import sys

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.insert(0, BASE_DIR)

import tensorflow as tf

from models.tensorflow_model import Model
from constants import TENSORFLOW_SAVES_DIR

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main(saves_dir=TENSORFLOW_SAVES_DIR):
    os.makedirs(saves_dir, exist_ok=True)
    # save our initial model at first
    model = Model()
    saver = tf.train.Saver()
    save_path = os.path.join(os.path.abspath(saves_dir), 'usual_model')
    saver.save(model.sess, save_path)

    # get constant graph
    constant_graph = tf.graph_util.convert_variables_to_constants(
        model.sess,
        tf.get_default_graph().as_graph_def(),
        [model.output.name.split(':')[0]]
    )

    # save constant graph
    frozen_save_path = os.path.join(saves_dir, 'constant_graph.pb')
    with tf.gfile.GFile(frozen_save_path, "wb") as f:
        f.write(constant_graph.SerializeToString())


if __name__ == '__main__':
    main()
