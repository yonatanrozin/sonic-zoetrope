import wave, struct, time
from PIL import Image, ImageDraw

print("HI")

# Create a new PNG file of the waveform of the audio file with starting point and length in seconds
def toPNG(start, length):
    timeStart = time.time() #to measure elapsed time 

    wm = wave.open("wavTest_mono.wav", mode = "r") #open .wav file in read mode

    frames = int(length * wm.getframerate()) #convert starting time and duration to sample numbers
    startFrame = int(start * wm.getframerate()) 

    #set pointer to starting sample
    wm.rewind()
    wm.setpos(startFrame) 

    #read and unpack data into an empty list
    frameData = []
    for x in range(frames):
        frameData.append(struct.unpack("<h", wm.readframes(1))[0])
    
    #set image width and height according to sample count and min/max values
    minFrame = min(frameData)
    maxFrame = max(frameData)
    img = Image.new("1", (frames, -minFrame+maxFrame+5000)) 
    draw = ImageDraw.Draw(img) #an object for drawing lines onto an image


    for frame in range(len(frameData)): 
        try:
            #draw a white line 1px wide from vertical sample position to the top of the image
            draw.line([(frame, frameData[frame]-minFrame),(frame, 0)], 255) 
        except:
            #or print any problematic arguments
            print(frame, frameData[frame]) 

    sizeRatio = img.width/img.height
    newHeight = int(20000 * sizeRatio)

    print(img.width, img.height)
    #compress and save the PNG file
    img.resize((int(img.width*2), int(img.height/4))).save("image.png", "PNG") 
    # img.resize((20000, newHeight)).save("image.png", "PNG") 

    #report elapsed time
    print("Completed in", format(time.time()-timeStart, ".2f"), "secs.")

    wm.close()



toPNG(82, 1)
