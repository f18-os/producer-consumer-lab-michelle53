#! /usr/bin/env python3

import threading, cv2, base64, sys, os
import numpy as np

# extract frames from clip
def extract( vidcap, count, image, outputdir='frames' ):
    cv2.imwrite( '{}/frame_{:04d}.jpg'.format( outputdir,  count ), image )
    print( 'Reading frame {}'.format( count ) )
    success, imgage = vidcap.read()
    return success, image
# convert to grayscale
def gray( count, outputdir='frames' ):
    infileName = '{}/frame_{:04d}.jpg'.format( 'frames', count )
    inputFrame = cv2.imread( infileName, cv2.IMREAD_COLOR )
    print( 'Converting frame {}'.format( count ) )
    grayscaleFrame = cv2.cvtColor( inputFrame, cv2.COLOR_BGR2GRAY )
    outFileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
    cv2.imwrite( outFileName, grayscaleFrame )
# display the grayscaled framed
# producer parts
def produce( vidcap, count, image ):
    sucess, image = extract( vidcap, count, image, outputdir='frames' )
    return sucess, image
def producer( sema ):
    vidcap = cv2.VideoCapture( 'clip.mp4' )
    count = 0
    success, image = vidcap.read()
    sema.aquire()
    while success:
        sema.aquire()
        success, image = produce( vidcap, count, image )
        count += 1
        sema.release()
def produce2( count ):
    gray( count )
def producer2( sema ):
    count = 0
    while True:
        produce2( vcount )
        count += 1
# main code
if not os.path.exists( 'frames' ):
    print( 'output doesnt exist, creating' )
    os.makedirs( 'frames' )

    
sema = threading.Semaphore( 2 )
pro_thread = threading.Thread( target=producer, args=( sema )  )
#pro_2thread = threading.Thread( target=producer2, args=sema )

pro_thread.start()
#pro_2thread.start()

pro_thread.join()
#pro_2thread.join()
