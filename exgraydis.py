#! /usr/bin/env python3

import threading, cv2, base64, queue, sys, os
import numpy as np

# extract the frames from clip
def extractFrames( fileName, outputdir = 'frames' ):
    count = 0 # initializing frame count
    vidcap = cv2.VideoCapture( fileName ) # open video files
    # create the output directory if it doesnt exists
    if not os.path.exists( outputdir ):
        print(' output doesnt not exit, creating' )
        os.makedirs( outputdir )
    success, image = vidcap.read() # read first image
    print( 'Reading Frame {} {}'.format( count, success ) )
    while success:
        cv2.imwrite( '{}/frame_{:04d}.jpg'.format( outputdir, count), image  )
        success, image = vidcap.read()
        print( 'Reading frame {}'.format( count ) )
        count += 1
    print( 'Frame extraction completed' )

# convert images to grayscale
def toGray( outputdir, outputBuffer ):
    count = 0 #initialize frame count
    inFileName = '{}/frame_{:04d}.jpg'.format( outputdir, count ) # get next frame file name
    inputFrame = cv2.imread( inFileName, cv2.IMREAD_COLOR ) # load next file

    while inputFrame is not None:
        print( 'Converting frame {}'.format( count ) )
        grayscaleFrame = cv2.cvtColor( inputFrame, cv2.COLOR_BGR2GRAY ) # convert to gray
        outFileName = '{}/grayscale_{:04d}.jpg'.format( outputdir, count )
        cv2.imwrite( outFileName, grayscaleFrame )
        count += 1
        
        # put to output
        sucess, jpgImage = cv2.imencode( '.jpg', cv2.imread( outFileName, cv2.IMREAD_COLOR ) )
        jpgAsText = base64.b64encode( jpgImage )
        outputBuffer.put( jpgAsText  )

        inFileName = '{}/frame_{:04d}.jpg'.format( outputdir, count ) # get next frame file name
        inputFrame = cv2.imread( inFileName, cv2.IMREAD_COLOR ) # load next file
    print( 'Frame to grayscale completed' )

# display grayed clip
def display( inputBuffer ):
    count = 0 # initialize buffer
    while not inputBuffer.empty():
        frameAsText = inputBuffer.get()
        jpgRawImage = base64.b64decode( frameAsText )
        jpgImage = np.asarray( bytearray( jpgRawImage ), dtype=np.uint8 )
        img = cv2.imdecode( jpgImage, cv2.IMREAD_UNCHANGED )
        print( 'Diplaying frame {}'.format( count ) )
        cv2.imshow( 'Video', img )
        if cv2.waitKey( 24 ) and 0xFF == ord( 'q' ):
            break
        count += 1
    print( 'Finished dispay' )
    cv2.destroyAllWindows() # cleanup time


filename = 'clip.mp4'

# Threading main
exQueue = queue.Queue()
extractFrames( filename )
toGray( 'frames', exQueue )
display( exQueue )



        


        
        
