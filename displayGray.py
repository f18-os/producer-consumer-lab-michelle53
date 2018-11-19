import threading, cv2, base64, sys, os
import numpy as np

alive = True
# First thread = extract frames from file
# extract frames from clip
def extract( vidcap, count, image, outputdir='frames' ):
    cv2.imwrite( '{}/frame_{:04d}.jpg'.format( outputdir, count ), image )
    print( 'Reading frame {}'.format( count ) )
    success, image = vidcap.read()
    return success, image
# producer for extract
fill_sema = threading.Semaphore( 0 ) # to fill semaphore
empty_sema = threading.Semaphore( 10 ) # to emtpy semaphore
def produce( vidcap, count, image ):
    success, image = extract( vidcap, count, image, outputdir='frames' )
    return success, image
def producer( ):
    vidcap = cv2.VideoCapture( 'clip.mp4' )
    count = 0
    success, image = vidcap.read()
    while alive: 
        if success: # keep reading only if we are allowed
            success, image = produce( vidcap, count, image )
        empty_sema.acquire()
        count += 1
        fill_sema.release()
    print('Finished extraction')
# consumer for gray conversion
def gray( count, outputdir='frames' ):
    infileName = '{}/frame_{:04d}.jpg'.format( 'frames', count )
    inputFrame = cv2.imread( infileName, cv2.IMREAD_COLOR )
    if inputFrame is None: # then stop converting
        return 0
    print( 'Converting frame {}'.format( count ) )
    grayscaleFrame = cv2.cvtColor( inputFrame, cv2.COLOR_BGR2GRAY )
    outfileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
    cv2.imwrite( outfileName, grayscaleFrame )
    return 1
def consume( count ):
    return gray( count )
def consumer( ):
    count = 0
    go_on = 1
    while alive:
        fill_sema.acquire()
        empty_sema.release()
        if go_on:
            go_on = consume( count )
            count += 1
    print( 'finished conversion' )
#consumer for display
def display( count, outputdir='frames' ):
    infileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
    try:
        sucess, jpgImage = cv2.imencode( '.jpg', cv2.imread( infileName, cv2.IMREAD_COLOR ) )
    except:
        return 0
    if not sucess:
        return 0
    jpgAsText = base64.b64encode( jpgImage )
    jpgRawImage = base64.b64decode( jpgAsText )
    jpgImage = np.asarray( bytearray( jpgRawImage ), dtype=np.uint8 )
    img = cv2.imdecode( jpgImage, cv2.IMREAD_UNCHANGED )
    print( 'Displaying frame {}'.format( count ) )
    cv2.imshow( 'Video', img )
    if cv2.waitKey( 24 ) and 0xFF == ord( 'q' ): # delay of 24 milliseconds
        return
    return 1
def consume2( count ):
    return display( count )
def consumer2():
    count = 0
    sucess = 1
    while True:
        fill_sema.acquire()
        empty_sema.release()
        if sucess: # only display if we have stuff to display
            sucess = consume2( count )
        else: # nothing to display then end window
            print( 'finished displaying' )
            cv2.destroyAllWindows()
            alive = False
            sys.exit()
        count += 1
# main code
if not os.path.exists( 'frames' ):
    print( 'output directory does not exists, creating' )
    os.makedirs( 'frames' )
 
pro_thread = threading.Thread( target=producer )
con_thread = threading.Thread( target=consumer )
con2_thread = threading.Thread( target=consumer2 )


threads = [ pro_thread, con_thread, con2_thread ]
for thread in threads: # start threads
    thread.start()
#for thread in threads:
#    thread.join()
