#! /usr/bin/env python3

import threading, cv2, base64, sys, os
import numpy as np

#extract frames from clip
def extract( vidcap, count, image, outputdir='frames' ):
    cv2.imwrite( '{}/frame_{:04d}.jpg'.format( outputdir,  count ), image )
    print( 'Reading frame {}'.format( count ) )
    success, imgage = vidcap.read()
    return success, image
def gray( count, outputdir='frames' ):
    infileName = '{}/frame_{:04d}.jpg'.format( 'frames', count )
    inputFrame = cv2.imread( infileName, cv2.IMREAD_COLOR )
    print( 'Converting frame {}'.format( count ) )
    grayscaleFrame = cv2.cvtColor( inputFrame, cv2.COLOR_BGR2GRAY )
    outFileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
    cv2.imwrite( outFileName, grayscaleFrame )
#producer parts
def produce( vidcap, count, image ):
    sucess, image = extract( vidcap, count, image, outputdir='frames' )
    gray( count )
    return sucess, image
def producer():
    vidcap = cv2.VideoCapture( 'clip.mp4' )
    count = 0
    success, image = vidcap.read()
    while success:
        success, image = produce( vidcap, count, image )
        count += 1        
# main code
if not os.path.exists( 'frames' ):
    print( 'output doesnt exist, creating' )
    os.makedirs( 'frames' )

pro_thread = threading.Thread( target=producer )


pro_thread.start()
