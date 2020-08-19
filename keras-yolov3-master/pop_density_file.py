# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:23:03 2020

@author: imaging_jpc
"""
import numpy as np
import argparse
import pickle
from scipy.spatial import distance

def _main_(args):
    
    input_file   = args.input
    #output_path  = args.output        
#def pop_density_file(input_file):
    
    with open(input_file,'rb') as file:
    #with open('C:/Users/imaging_jpc/keras-yolo3/output_results/content/keras-yolo3/output_results/results_MP_SEL_B015461.p','rb') as file:    
      v_boxes = pickle.load(file)  
      v_labels = pickle.load(file) 
      v_scores = pickle.load(file) 
      # print(v_boxes[1].ymin, v_boxes[1].xmin, v_boxes[1].ymax, v_boxes[1].xmax)
      # print(v_labels)
      # print(v_scores)
      matrix_xy = [0,0,0,0,0,0,0,0,0,0]
      h_n = len(v_labels)
      if h_n>1:
          for i in range(0,h_n):
              # print(i)
              x1 = (v_boxes[i].xmin + v_boxes[i].xmax)/2
              y1 = (v_boxes[i].ymin + v_boxes[i].ymax)/2
              h_tall = abs(v_boxes[i].ymax - v_boxes[i].ymin)
              h_width = abs(v_boxes[i].xmax - v_boxes[i].xmin) 
              socialdst_pixels = (200*h_tall)/164.25 #우리나라 사람 평균신장 164.25
              h_diag = np.sqrt(h_tall**2+h_width**2)
              socialdst_pixels1 = (200*h_diag)/164.25          
              mat_xy = np.array([v_boxes[i].ymin, v_boxes[i].xmin, v_boxes[i].ymax, v_boxes[i].xmax,x1,y1,h_tall,socialdst_pixels,h_diag,socialdst_pixels1])
              matrix_xy = np.vstack([matrix_xy,mat_xy])
              
          # print(matrix_xy)
          matrix_xy = np.delete(matrix_xy,0,0)
          # print(matrix_xy)
          all_pair = 0
          violate_pair = 0
          for i in range(0,h_n):
              print('i=',i)
              for j in range(i+1,h_n):
                  print('j=',j)
                  centeri = matrix_xy[i,4:6]
                  centerj = matrix_xy[j,4:6]
                  # print(centeri)
                  # print(centerj)
                  dst = distance.euclidean(centeri, centerj)
                  # print(dst)
                  # dst가 i열과  j열의 기준 socialdst_pixels 보다 작은 경우를  체크한다. 전체 pair 중에서 몇 퍼센트인지도 계산.
                  all_pair = all_pair+1
                  if matrix_xy[i,7] >= matrix_xy[j,7]:
                      if dst < matrix_xy[i,7]:
                          violate_pair = violate_pair+1
                  elif matrix_xy[j,7] > matrix_xy[i,7]:
                      if dst < matrix_xy[i,7]:
                          violate_pair = violate_pair+1  
                          
          print("social distance violate =", violate_pair,"/total person pair=", all_pair) 
          print("total number of person =", h_n)              
          
          
          # 그림파일이 하나인지 여러개를 평균낼걸지 결정해야 한다. 그냥 실시간이 나을듯.
          return matrix_xy
      
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Predict with a trained yolo model')
    #argparser.add_argument('-c', '--conf', help='path to configuration file')
    argparser.add_argument('-i', '--input', help='path to an image, a directory of images, a video, or webcam')    
    #argparser.add_argument('-o', '--output', default='output/', help='path to output directory')   
    
    args = argparser.parse_args()
    _main_(args)
