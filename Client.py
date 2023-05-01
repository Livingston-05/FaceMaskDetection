""" usage :
python3 Client.py -i image.jpg
"""
import socket
import numpy as np
import cv2
import pickle
import struct
import time
import os
from os import listdir
from os.path import isfile, join
import sys
import argparse as arg
import glob
from detect_mask_image import suppress_qt_warnings


# def Arg_Parse():
#     Arg_Par = arg.ArgumentParser()
#     Arg_Par.add_argument("-i", "--image", help="path of the image")
#     arg_list = vars(Arg_Par.parse_args())
#     return arg_list


if __name__ == "__main__":
    suppress_qt_warnings()
    # if len(sys.argv) == 1:
    #     print("Please Provide an argument !!!")
    #     sys.exit(0)
    # Arg_list = Arg_Parse()
    # if Arg_list["image"] != None:
    # image = cv2.imread(Arg_list["image"])
    directory = os.getcwd()
    while(1):
        path=input("Enter the folder name:")
        
        path = os.path.join(directory, path)
        isExist = os.path.exists(path)
        
        if isExist:
            onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
            images = np.empty(len(onlyfiles), dtype=object)
            for n in range(0, len(onlyfiles)):
                images[n] = cv2.imread( join(path,onlyfiles[n]) )
            HOST = "localhost"
            TCP_IP = socket.gethostbyname(HOST)  # Domain name resolution
            TCP_PORT = 4445
            CHUNK_SIZE = 4 * 1024
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            # socket for sending and receiving images
            Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("\n[*] Connecting to server @ ip = {} and port = {}".format(TCP_IP, TCP_PORT))
            Client_Socket.connect((TCP_IP, TCP_PORT))
            print("\n[*] Client connected successfully !")
            for n in range(0, len(onlyfiles)):
                result, frame = cv2.imencode(".jpeg", images[n], encode_param)
            # Returns the bytes object of the serialized object.
                data = pickle.dumps(frame, 0)
                size = len(data)
            # print("\n[*] Sending a packet size of: ",size)
                Client_Socket.sendall(struct.pack("l", size) + data)

                print("\n[*] Image is sent successfully ")

                data = b""
                # struct_size is 8 bytes
                struct_size = struct.calcsize("l")
                # print("\n[*] Struct Size: ",struct_size)
                img_size = Client_Socket.recv(struct_size)
                # print(img_size.hex())
                # struct.unpack retrun a tuple
                img_size = struct.unpack("l", img_size)[0]

                while len(data) < img_size:
                    data += Client_Socket.recv(CHUNK_SIZE)

                frame_data = data[:img_size]
                data = data[img_size:]
                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow("Image", frame)
                
                # time.sleep(10)
                cv2.waitKey(0)

        else:
            print("Folder not found")
            
        cv2.destroyAllWindows()
        
        path = input("Do you want to exit(y/n)?: ")
        if(path=="y" or path=="Y" or path=="yes" or path=="Yes" or path=="YES"):
            # print("Byeeee, Thank you lol, give full marks")
            print("Byeeeeee!!")
            break
