#!/usr/bin/python
# -*- coding: utf-8 -*-

from picamera.array import PiRGBArray
import picamera
import time
import cv2
import os
import pygame
import freetype
import json
import base64
from subprocess import Popen,PIPE
from PIL import Image
import requests
api_key="PMtVOYm8rLXArqGRd9wLnuJDVTvP9r57"
api_secret="F-xhhsUSE-OfQWQDbaFB60gQze1b6ZTe"
outer_id="xiangyinfa"
path='./data/log'


face_cascade = cv2.CascadeClassifier( '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml' )


def compareItoT(image_file,face_token):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/compare" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "image_file1=@{image_file}" -F \
        "face_token2={face_token}"'
        .format(api_key=api_key,api_secret=api_secret,image_file=image_file,face_token=face_token),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    return result 

if __name__ == '__main__':

    with picamera.PiCamera() as camera:

        #设置分辨率
        camera.resolution = ( 320, 240 )
        camera.framerate = 40

        #打开摄像头进行预览
        camera.start_preview()

        rawCapture = PiRGBArray( camera, size=( 320, 240 ) )

        for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):

            image = frame.array

            count = 0
            gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
            faces = face_cascade.detectMultiScale( gray ,scaleFactor=1.1, minNeighbors=5,minSize=(30, 30))
            for ( x, y, w, h ) in faces:
                    ###使用以上4个值调用内置函数rectangle()画出一个四边型。
                    img= cv2.rectangle( image, ( x, y ),( x + w, y + h ), ( 255, 255, 0 ), 1 )

                    #获取存储图片路径
                    path= os.getcwd()+'/images/'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+".jpg"

                    f=cv2.resize(image[y:y+h,x:x+w],(400,400))
                    #cv2.imwrite(path,f,[int(cv2.IMWRITE_JPEG_QUALITY), 20])
                    
                    cv2.imwrite(path, f ,[int(cv2.IMWRITE_JPEG_QUALITY), 20])

                    result=compareItoT(image_file=path,face_token='a28f5dd69cb13d821d14bc3e955ffa57')
                    os.remove(path)
                    
                    s= json.loads(result)
                    
                    if len(result)==47:
                        print "并发情况"
                        #cv2.putText(img,"no", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
                    else:
                        if len(result)==341:
                            print "相似度"+str(s ["confidence"])
                            if s ["confidence"] >= 80.00:
                                cv2.putText(img,"xiangyinfa", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)

                            else:
                                cv2.putText(img,"no", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
                        #else:
                         #       print ""
                               # cv2.putText(img,"no", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
                    


            cv2.imshow( "Frame", image )

            cv2.waitKey( 1 )

            rawCapture.truncate( 0 );

