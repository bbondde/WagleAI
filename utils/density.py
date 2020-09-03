import numpy as np
from scipy.spatial import distance
import cv2


def density_estimator(person_num, boxes):
    matrix_xy = [0] * 9

    for i in range(person_num):
        center_x = (boxes[i].xmin + boxes[i].xmax) / 2
        center_y = (boxes[i].ymin + boxes[i].ymax) / 2
        box_height = abs(boxes[i].ymax - boxes[i].ymin)
        box_width = abs(boxes[i].xmax - boxes[i].xmin)

        social_distance = 200
        human_average_height = 164.25

        socialdst_pixel = (social_distance * box_height) / human_average_height

        mat_xy = np.array([boxes[i].xmin, boxes[i].ymin, boxes[i].xmax, boxes[i].ymax,
                           center_x, center_y, box_width, box_height, socialdst_pixel])
        matrix_xy = np.vstack([matrix_xy, mat_xy])

    matrix_xy = np.delete(matrix_xy, 0, 0)
    density_sum = 0

    all_pair = 0
    violate_pair = 0
    for i in range(person_num-1):
        for j in range(i + 1, person_num):
            center_box_i = matrix_xy[i, 4:6]
            center_box_j = matrix_xy[j, 4:6]

            dst = distance.euclidean(center_box_i, center_box_j)

            min_distance = max(matrix_xy[i][8], matrix_xy[j][8])
            print(min_distance, dst)
            if dst == min(min_distance, dst):
                violate_pair += 1
                break

            #if matrix_xy[i][8] >= matrix_xy[j][8]:
            #    if dst < matrix_xy[i][8]:
            #        violate_pair += 1
            #        continue
            #else:
            #    if dst < matrix_xy[j][8]:
            #        violate_pair += 1
            #        continue

            #all_pair += 1

        #density_rate = violate_pair / all_pair
        #density_sum += density_rate


    print(person_num, violate_pair)
    if not person_num:
        return 0
    average_density = violate_pair / person_num
    #print(average_density)
    return average_density


def show_density(image, person_num, average_density):
    height, width = image.shape[:2]
    location1 = (width - 350, height - 30)
    location2 = (20, height-30)
    font = cv2.FONT_ITALIC
    font_scale = 1
    blue = (255, 0, 0)
    green = (0, 255, 0)
    red = (0, 0, 255)
    thickness = 3

    text1 = "#Person : %d" % person_num
    text2 = "Density : %lf" % average_density

    cv2.putText(image, text1, location2, font, font_scale, blue, thickness)

    if average_density > 0.6:
        cv2.putText(image, text2, location1, font, font_scale, red, thickness)
    else:
        cv2.putText(image, text2, location1, font, font_scale, green, thickness)
    #if average_density > 0.7:
    #    cv2.putText(image, 'Crowded', location, font, font_scale, green, thickness)
    #elif 0.5 <= average_density <= 0.7:
    #    cv2.putText(image, 'Normal', location, font, font_scale, green, thickness)
    #else:
    #    cv2.putText(image, 'Secluded', location, font, font_scale, green, thickness)

    return image

