import threading, cv2, base64, sys, os
import numpy as np

# First thread = extract frames from file
# extract frames from clip
def extract( vidcap, count, image, outputdir='frames' ):
    cv2.imwrite( '{}/frame_{:04d}.jpg'.format( outputdir, count ), image )
    print( 'Reading frame {}'.format( count ) )
    success, image = vidcap.read()
    return success, image
# producer for extract
fill_sema = threading.Semaphore( 0 )
empty_sema = threading.Semaphore( 10 )
def produce( vidcap, count, image ):
    success, image = extract( vidcap, count, image, outputdir='frames' )
    return success, image
def producer( ):
    vidcap = cv2.VideoCapture( 'clip.mp4' )
    count = 0
    success, image = vidcap.read()
    while True:
        success, image = produce( vidcap, count, image )
        empty_sema.acquire()
        count += 1
        fill_sema.release()
# producer for gray conversion
def gray( count, outputdir='frames' ):
    infileName = '{}/frame_{:04d}.jpg'.format( 'frames', count )
    inputFrame = cv2.imread( infileName, cv2.IMREAD_COLOR )
    print( 'Converting frame {}'.format( count ) )
    grayscaleFrame = cv2.cvtColor( inputFrame, cv2.COLOR_BGR2GRAY )
    outfileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
    cv2.imwrite( outfileName, grayscaleFrame )
def consume( count ):
    gray( count )
def consumer( ):
    count = 0
    while True:
        fill_sema.acquire()
        empty_sema.release()
        consume( count )
        count += 1
# main code
if not os.path.exists( 'frames' ):
    print( 'output directory does not exists, creating' )
    os.makedirs( 'frames' )
 
pro_thread = threading.Thread( target=producer )
con_thread = threading.Thread( target=consumer )

pro_thread.start()
con_thread.start()

#pro_thread.join()
#con_thread.join()
