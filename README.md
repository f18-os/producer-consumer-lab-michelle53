# Producer Consumer Lab

For this lab you will implement a trivial producer-consumer system using
python threads where all coordination is managed by counting and binary
semaphores for a system of two producers and two consumers. The producers and
consumers will form a simple rendering pipeline using multiple threads. One
thread will read frames from a file, a second thread will take those frames
and convert them to grayscale, and the third thread will display those
frames. The threads will run concurrently.

## File List
### ExtractFrames.py
Extracts a series of frames from the video contained in 'clip.mp4' and saves 
them as jpeg images in sequentially numbered files with the pattern
'frame_xxxx.jpg'.

### ConvertToGrayscale.py
Loads a series for frams from sequentially numbered files with the pattern
'frame_xxxx.jpg', converts the grames to grayscale, and saves them as jpeg
images with the file names 'grayscale_xxxx.jpg'

### DisplayFrames.py
Loads a series of frames sequently from files with the names
'grayscale_xxxx.jpg' and displays them with a 42ms delay.

### ExtractAndDisplay.py
Loads a series of framss from a video contained in 'clip.mp4' and displays 
them with a 42ms delay

## Requirements
* Extract frames from a video file, convert them to grayscale, and display
them in sequence
* You must have three functions
  * One function to extract the frames
  * One function to convert the frames to grayscale
  * One function to display the frames at the original framerate (24fps)
* The functions must each execute within their own python thread
  * The threads will execute concurrently
  * The order threads execute in may not be the same from run to run
* Threads will need to signal that they have completed their task
* Threads must process all frames of the video exactly once
* Frames will be communicated between threads using producer/consumer idioms
  * Producer/consumer quesues will be bounded at ten frames

Note: You may have ancillary objects and method in order to make you're code easer to understand and implement.

## My work
* I understood this lab to require the usage of semaphores as a form of queue
  and that is what I used for this lab. The threads follow producer consumer
  in which extracting frames is the producer and both the converting to
  grayscale and displaying are consumers. The threads run almost
  synchroniously but at the times the extraction and converting finish way
  first before the displaying. The script has to be manually killed to stop the 
  script but all threads display that it is finished.

* To run it we need to just do the following:
~~~
python3 displayGray.py
~~~
