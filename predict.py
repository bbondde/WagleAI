import os
import cv2
import json
import numpy as np
from tqdm import tqdm
from testcase import *
from keras.models import load_model
from utils.bbox import draw_boxes, count_person
from utils.utils import get_yolo_boxes, makedirs
from utils.density import density_estimator, show_density


def predict_main_(args):
    config_path = args.conf
    input_path = args.input
    output_path = args.output

    yolo_config_file_exit('pass') \
        if os.path.exists(config_path) \
        else yolo_config_file_exit('fail')

    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    makedirs(output_path)
    yolo_create_exit('pass') \
        if os.path.isdir(output_path) \
        else yolo_create_exit('fail')

    ###############################
    #   Set some parameter
    ###############################

    net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    ###############################
    #   Load the model
    ###############################

    yolo_model_exit('pass') \
        if os.path.isfile(config['train']['saved_weights_name']) \
        else yolo_model_exit('fail')

    infer_model = load_model(config['train']['saved_weights_name'],
                             compile=False)

    ###############################
    #   Predict bounding boxes 
    ###############################
    if 'webcam' in input_path:  # do detection on the first webcam
        video_reader = cv2.VideoCapture(0)

        yolo_webcam_exit('pass') \
            if video_reader.isOpened() \
            else yolo_webcam_exit('fail')

        # the main loop
        batch_size = 1
        images = []
        while True:
            ret_val, image = video_reader.read()
            if ret_val:
                images += [image]

            if (len(images) == batch_size) or \
                    (ret_val is False and len(images) > 0):
                batch_boxes = get_yolo_boxes(infer_model, images, net_h, net_w,
                                             config['model']['anchors'],
                                             obj_thresh, nms_thresh)

                for i in range(len(images)):
                    draw_boxes(images[i], batch_boxes[i],
                               config['model']['labels'], obj_thresh)

                    person, use_boxes = count_person(batch_boxes[i],
                                                     config['model']['labels'],
                                                     obj_thresh)
                    average_density = density_estimator(person, use_boxes)
                    show_density(image[i], average_density)

                    cv2.imshow('video with bboxes', images[i])
                images = []
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()

        try:
            yolo_process_exit('pass')
        except RuntimeError as e:
            yolo_process_exit('fail')

    elif input_path[-4:] == '.mp4':  # do detection on a video
        yolo_video_file_exit('pass') \
            if os.path.isfile(input_path) \
            else yolo_video_file_exit('fail')

        video_out = output_path + input_path.split('/')[-1]
        video_reader = cv2.VideoCapture(input_path)

        nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

        video_writer = cv2.VideoWriter(video_out,
                                       cv2.VideoWriter_fourcc(*'MPEG'),
                                       50.0, (frame_w, frame_h))
        # the main loop
        batch_size = 1
        images = []
        start_point = 0
        show_window = True
        save_window = True
        for i in tqdm(range(nb_frames)):
            _, image = video_reader.read()

            if (float(i+1)/nb_frames) > start_point/100.:
                images += [image]

                if (i % batch_size == 0) or \
                        (i == (nb_frames-1) and len(images) > 0):
                    # predict the bounding boxes
                    batch_boxes = get_yolo_boxes(infer_model, images, net_h,
                                                 net_w,
                                                 config['model']['anchors'],
                                                 obj_thresh, nms_thresh)

                    for j in range(len(images)):
                        # draw bounding boxes on the image using labels

                        if show_window:
                            draw_boxes(images[j], batch_boxes[j],
                                       config['model']['labels'], obj_thresh)

                        person, use_boxes = count_person(batch_boxes[j],
                                                         config['model'][
                                                             'labels'],
                                                         obj_thresh)
                        average_density = density_estimator(person, use_boxes)
                        show_density(images[j], person, average_density)

                        # show the video with detection bounding boxes          
                        if show_window:
                            cv2.imshow('video with bboxes', images[j])

                        # write result to the output video
                        if save_window:
                            video_writer.write(images[j])
                    images = []
                if show_window and cv2.waitKey(1) == 27:
                    break  # esc to quit

        if show_window:
            cv2.destroyAllWindows()

        yolo_release_exit('pass') \
            if not video_reader.release() \
            else yolo_release_exit('fail')

        yolo_release_exit('pass') \
            if not video_writer.release() \
            else yolo_release_exit('fail')

        try:
            yolo_process_exit('pass')
        except RuntimeError as e:
            yolo_process_exit('fail')


    else:  # do detection on an image or a set of images
        image_paths = []
        yolo_image_file_exit('pass') \
            if os.path.isfile(input_path) \
            else yolo_image_file_exit('fail')

        if os.path.isdir(input_path): 
            for inp_file in os.listdir(input_path):
                image_paths += [input_path + inp_file]
        else:
            image_paths += [input_path]

        image_paths = [inp_file for inp_file in image_paths if
                       (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]

        # the main loop
        for image_path in image_paths:
            yolo_path_exit('pass') \
                if os.path.isfile(image_path) \
                else yolo_path_exit('fail')

            image = cv2.imread(image_path)

            # predict the bounding boxes
            boxes = get_yolo_boxes(infer_model, [image], net_h, net_w,
                                   config['model']['anchors'], obj_thresh,
                                   nms_thresh)[0]

            # draw bounding boxes on the image using labels
            draw_boxes(image, boxes, config['model']['labels'], obj_thresh)

            # print the number of predicted boxes
            person, use_boxes = count_person(boxes,
                                             config['model']['labels'],
                                             obj_thresh)
            average_density = density_estimator(person, use_boxes)
            show_density(image, person, average_density)

            cv2.imshow('video with bboxes', image)
            cv2.waitKey(3000)
     
            # write the image with bounding boxes to file
            yolo_save_exit('pass') \
                if cv2.imwrite(output_path + image_path.split('/')[-1],
                               np.uint8(image)) \
                else yolo_save_exit('fail')

            try:
                yolo_process_exit('pass')
            except RuntimeError as e:
                yolo_process_exit('fail')

"""if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Predict with a trained yolo model')
    argparser.add_argument('-c', '--conf', help='path to configuration file')
    argparser.add_argument('-i', '--input',
                           help='path to an image, a directory of images, a video, or webcam')
    argparser.add_argument('-o', '--output',
                           default='output/', help='path to output directory')
    
    args = argparser.parse_args()
    _main_(args)
    """
