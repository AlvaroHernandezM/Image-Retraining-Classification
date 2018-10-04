import os
from os import listdir
from os.path import join
import tensorflow as tf


FOLDER_SINGLE_PREDICTION = 'static/img/single_prediction/'
FILE_OUTPUT_LABELS = 'core/models/output_labels.txt'
FILE_OUTPUT_GRAPH = 'core/models/output_graph.pb'


def classification():
    images = __get_images(FOLDER_SINGLE_PREDICTION)
    ext_img = ''
    for image in images:
        filename = image.split('.')[0]
        ext_img = image.split('.')[1]
        print (filename)
    image_data = tf.gfile.FastGFile(filename + '.' + ext_img, 'rb').read()
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(FILE_OUTPUT_LABELS)]

    with tf.gfile.FastGFile(FILE_OUTPUT_GRAPH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})

    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    respond = {}
    i = 1
    for node_id in top_k:
        human_string = label_lines[node_id]
        respond['class-' + str(i)] = human_string
        score = predictions[0][node_id]
        respond['score-' + str(i)] = '%.5f' % (score)
        i = i + 1
    respond['success'] = True
    return respond


def __get_images(folder):
    return [join(folder, file) for file in listdir(folder)]


if __name__ == '__main__':
    print(train())
    print(classification())
