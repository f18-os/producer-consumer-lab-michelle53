import threading, cv2, base64, sys, os, queue
import numpy as np
from threading import Thread, Lock

mutex = Lock()
fill_sema = threading.Semaphore( 0 )
empty_sema = threading.Semaphore( 10 )
alive = True
# extract frames from video
def extract( vidcap, count, image, outputBuffer ):
    mutex.acquire()
    success, jpgImage = cv2.imencode( '.jpg', image )
    outputBuffer.put( base64.b64encode( jpgImage ) )
    print( 'Reading frame {} {}'.format( count, success ) )
    success, image = vidcap.read()
    mutex.release()
    return success, image, ( count + 1 )
# produce extracted frames
def producer( outputBuffer ):
    count = 0
    vidcap = cv2.VideoCapture( 'clip.mp4' )
    success, image = vidcap.read()
    while True:
        if success:
            success,image, count = extract( vidcap, count, image, outputBuffer )
        empty_sema.acquire()
        fill_sema.release()
    print( 'All extraction complete' )

# COnvert to gray
def gray( count, inputBuffer, outputBuffer ):
    jpgImage = np.asarray( bytearray( base64.b64decode( inputBuffer.get() ) ), dtype=np.uint8 )
    gray = cv2.cvtColor( cv2.imdecode( jpgImage, cv2.IMREAD_UNCHANGED ), cv2.COLOR_BGR2GRAY )
    success, gray = cv2.imencode( '.jpg', gray )
    print( 'converting frame {}'.format( count ) )
    outputBuffer.put( base64.b64encode( gray ) )
    return ( count + 1 )
def consumer( inputBuffer, outputBuffer ):
    count = 0
    while True:
        fill_sema.acquire()
        empty_sema.release()
        count = gray( count, inputBuffer, outputBuffer )
# display the gray frames
def display( count, inputBuffer ):
    mutex.acquire()
    jpgRawImage = base64.b64decode( inputBuffer.get() )
    jpgImage = np.asarray( bytearray( jpgRawImage ), dtype=np.uint8 )
    img = cv2.imdecode( jpgImage, cv2.IMREAD_UNCHANGED )
    print( 'display frame {}'.format( count ) )
    cv2.imshow( 'Video', img )
    if cv2.waitKey( 47 ) and 0xFF == ord( 'q' ):
        return count
    mutex.release()
    return ( count + 1 )
def consumer2( inputBuffer ):
    global alive
    count = 0
    while alive:
        fill_sema.acquire()
        empty_sema.release()
        count = display( count, inputBuffer )
        if inputBuffer.empty():
            alive = False
            break
    print( 'finished displaying' )
    cv2.destroyAllWindows()
# QUEUE
extractionQueue = queue.Queue()
grayQueue       = queue.Queue()
# threads
pro_thread = threading.Thread( target=producer, args=( extractionQueue,  ) )
con_thread = threading.Thread( target=consumer, args=( extractionQueue, grayQueue, ) )
con2_thread = threading.Thread( target=consumer2, args=( grayQueue, ) )
pro_thread.start()
con_thread.start()
con2_thread.start()

#pro_thread.join()
#con_thread.join()
