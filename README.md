# AudioVisualizer
It is a pygame-based music visualiser. It takes the songs and applies the Fast Fourier Transformation for every 25 ms of the song and visualises them in the form of "Power Band". The application runs at 40 fps and uses multiprocess to play the actual song. This code uses multiprocess. One process will play the audio whereas the main thread deals with visualization. For the sake of brevity, the code is well commented.

## Required Packages

```bash
pip install pygame pydub pygame_gui numpy
```
Sometimes the ```ffmpg``` packages that the ```pydub``` needed to play the audio may not be installed. It can be installed with the following  command:
```bash
sudo apt install ffmpeg
```
## Instruction
* The application itself is pretty forward in nature. There is a button on the top left corner which can be used to select the audio to play and visualize it. 
* As of now only the "MP3" format is accepted but technically the code can run in various formats like "WAV" etc.
* ***This code does not gracefully kill the spawned extra process. One should manually kill the process.***

## Screenshot
![Screenshot](URL "./screen.png")

## References
  
  - [Python Silde](https://www.youtube.com/watch?v=4Otqdwql63c)
  
  - [Pydub](https://github.com/jiaaro/pydub/)

## 🤝 Support

Contributions, issues, and feature requests are welcome!

