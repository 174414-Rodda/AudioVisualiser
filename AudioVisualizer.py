import numpy as np              #Importing numpy for Fast Fourier transform(FFT)
import pygame_gui               #Pygame module for getting the file input
import multiprocessing          #To create a seperate process. Multiyhreading can also be used.
import pygame                   #Importing pygame
from pydub import AudioSegment  #Audiosegment to get the samples
from pydub.playback import play #To play the actual song
from random import randint      #For generating random integers between 0 and 255 for changing colors

"""
    Author : Raghava KV
    Objective: To Visualize the Audio
    Limitations: 
        - No Gracefull killing of the mulitprocess
        - No Quit Botton Either
"""
def songplayer(sound):
    """
    Input:  An audio segment type object named sound
    Objective : To play the given audiosegment object
    """
    play(sound)                 #Using play method from pydub.playback

def drawbars(board,data,COLOR):
    """

    Objective : To draw the vertical bars(Power Bars) for the given input.
    Input: 
        board: A main pygame surface object
        data : A tuple that contains the scaled data points for visualizing
        COLOR : A constant tuple of (R,G,B)
    """
    x = 0                      #Counter
    BARW,BARH = 45,10          #Bar Width and Bar Height
    DIFF = 15                  #Gap Between the vertical boxes
    BOTTOM =325                #Starting Point for the Base 
    CUTOFF = 250               #Cutoff to reduce the height of the given bar 
    while x<len(data):         #Loop to print the powerbands for the given records
        bar_x,bar_y = 150+(x*50),((data[x]))+CUTOFF#Finding the Ending Points until which the printing should happen
                                                   #Incrementing the bar_x for each iteration for each column

        tempy = BOTTOM         #Setting tempy to Bottom. Tempy holds the current y cordinate to print the rect

        while tempy>bar_y:     #Printing a column
            pygame.draw.rect(board,COLOR,(bar_x,tempy,BARW,BARH))#Drawing the Actual rectangle
            tempy-=DIFF        #Decrementing the tempy by DIFF value

        x+=1                   #Incrementing the Counter

def songanalizer(song):
    """
        Objective: For a given audiosegment object finding the FFT values for every 25 ms and storing them as a tuple.
        Output: Returns a list of tuples for every 25 ms of the audio segmetn
        Input:
            song: An audiosegment object
        Output:
            alldata: List of tuple for every 25ms of the song 
    """
    temp = 0                   #Count to access the slice
    newfinal = [0]*10          #Just creating a list of 0 with size 10
    alldata = []               #Declaring a list that holds final output
    temp1 = [0]*10             #Another temp list of size 10
    x = 0                      #Counter
    while(temp<len(song)-25):  #Taking each slice and performing the rfft and dividing into the scaling them and multiplying with 100
        a1 = song[temp:temp+25]#Taking the necessary slice of the audiosegment
        temp+=25               #Incrementing the count
        mono = a1.split_to_mono()[0]#Reducing the stero channel to mono
        values = mono.get_array_of_samples()#Getting the samples
        fft = np.fft.rfft(values,1024) #Applying the RFFT. Reduces the number of samples by half
        fft = fft[0:511]       #Just accessing the first 512 
        freq = np.array(np.abs(fft),dtype=int)#Casting them to int
        #Applying the formula found on the internet
        newfinal[0] = freq[0]
        newfinal[1] = freq[1]
        newfinal[2] = freq[2] + freq[3]
        newfinal[3] = np.sum(freq[4:7])
        newfinal[4] = np.sum(freq[8:16])
        newfinal[5] = np.sum(freq[17:32])
        newfinal[6] = np.sum(freq[33:65])
        newfinal[7] = np.sum(freq[66:131])
        newfinal[8] = np.sum(freq[132:263])
        newfinal[9] = np.sum(freq[264:511])
        #Basically getting 10 bands 
        newfinal = newfinal/np.max(newfinal)# Scaling them
        newfinal *=100                      #Multiplying by 100
        alldata.append(tuple(newfinal))     #Appending them to the alldata
    return alldata
#Main Method#
pygame.init()                  #Initialising the pygame
WIDTH,HEIGHT = 750,500         #Declaring the width and height of the screen
x = 0                          #Counter to maintain the number of 25 ms passed
playing = False                #A boolean which a file is given as input and it is played
board = pygame.display.set_mode((WIDTH,HEIGHT))#Creating a pygame surface
board.fill((0,0,0))            #Filling the surface with black
pygame.display.set_caption("AudioVisualizer")#Setting the title to AudioVisualizer
clock = pygame.time.Clock()    #Creating a clock object to maintain the speed of execution
manager = pygame_gui.UIManager((800, 600))#Creating a manager for pygame gui to get the file input from the user
filebutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,0), (100, 50)),text='Open',manager=manager)#Declaring a button that takes a filepath as input

while True:#Main game loop
    """
    NOTE:
        -This App runs at 40 FPS approximatly 1 iteration for every 25ms
        -Instead of clock.tick(), more CPU intensive clock.tick_busy_loop is used.
            - To get the better timing accuracy
    """
    board.fill((0,0,0))#Filling with black
    time_delta = clock.tick_busy_loop(40) / 1000.0#Finding the time elapsed

    for event in pygame.event.get():#Getting all the events and checking for them
        '''
        Intentionally commented as the program is unable to kill its own sub process
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()
        '''
        if(pygame.mouse.get_pressed()==(1,0,0)):#Checking for the left mouse click
            COLOR = ((randint(0,255),randint(0,255),randint(0,255)))#Creating a random color

        if event.type == pygame_gui.UI_BUTTON_PRESSED:#Cheking the pygamegui button click
            if event.ui_element == filebutton:  #Checking if the file button is clicked
 
                file_selection = pygame_gui.windows.UIFileDialog(rect=pygame.Rect(0, 0, 300, 300),  window_title='Load Image...',
                                                    initial_file_path='./',
                                                    allow_picking_directories=True,
                                                    allow_existing_files_only=True,manager=manager)
                                                #Creating the file selection UI
            if event.ui_element == file_selection.ok_button:#If clicked on OK button
                    filename = str(file_selection.current_file_path)#Getting the file path
                    extension = filename.split('.')[-1]     #Splitting based on . to check the extention
                    if('mp3' in extension):                 #Checking if MP3 is there or not
                        print("The File is:",filename)      #Printing the file Name
                        song = AudioSegment.from_file(filename)#Obtaing the audiosegment object of the given file
                        alldata = songanalizer(song)        #Getting the data points
                        process = multiprocessing.Process(target=songplayer,args=(song,))#Declaring a multiprocess that call the song player
                                                                                         # and takes the audiosegment named song as arugument
                        process.start()                     #Statring the process
                        playing = True                      #Setting playing to true

                    else:           #If there is no .mp3 then throwing an error and quitting the program
                        print("Kindly Give Mp3 Format!!!!")
                        pygame.display.quit()
                        pygame.quit()
                        exit()


        manager.process_events(event)           #pygame gui event processing

    manager.update(time_delta)                  #Updating the pygamegui surface
    manager.draw_ui(board)                      #Drawing the  UI on the main surface,board

    if(playing):                    #If playing is set to true then the counter is incremanted
        x+=1
        try:                        #Index out of bound error will raise because of the lack of perfect sync for every 25ms
                                    #Exiting the program in that case
            drawbars(board,alldata[x],COLOR)   #Calling the drawbars to visualize the bars
        except:
            pygame.display.quit()   #Shutting down the display
            pygame.quit()           #Exiting the pygame
            exit()                  #Exit the program
    
    pygame.display.update()         #Updating the display
    
    
