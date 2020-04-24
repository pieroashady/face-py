import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import json
from time import sleep

def get_encoded_faces():
    base_dir = 'dataset/'
    encoded = {}

    for subdirs in os.listdir(base_dir):
        for f in os.listdir(base_dir + subdirs):
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(base_dir + subdirs + "/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    # for dirpath, dnames, fnames in os.walk("./dataset"):
    #     # for dirnames in dnames:
    #         # dir_names = os.listdir(dirnames)
    #         for f in fnames:
    #             if f.endswith(".jpg") or f.endswith(".png"):
    #                 face = fr.load_image_file("dataset/" + f)
    #                 encoding = fr.face_encodings(face)[0]
    #                 encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    base_dir = 'dataset/'
    """
    encode a face given the file name
    """
    for subdirs in os.listdir(base_dir):
        for f in os.listdir(base_dir + subdirs):
            face = fr.load_image_file(base_dir + subdirs + "/" + img)
            encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im):
    """
    will find all of the faces in a given image and label
    them if it knows what they are
    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    # img = img[:,:,::-1]
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            name = "Unknown"

        face_names.append(name)
        
        for names in face_names:
            name = name
    return name