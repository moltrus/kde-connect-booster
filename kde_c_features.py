from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc, imwrite, getTickCount, getTickFrequency, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import POINTER, cast, CLSCTX_ALL, GUID
from pyaudio import paInt16, PyAudio
from PIL import ImageGrab
from time import time
import winsound
import wave
import os


def ring_pc(duration=1200):
    """
    The `ring_pc` function activates the speakers, sets the volume, and plays a beep sound for a
    specified duration.
    
    :param duration: The `duration` parameter is the length of time in seconds that the PC will ring
    for. By defaults it is set to 600 seconds (0.5 * 1200)
    """


    devices = AudioUtilities.GetSpeakers()
    interface_1 = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    interface_2 = devices.Activate(IAudioEndpointVolume._iid_, 7, None)
    volume_1 = cast(interface_1, POINTER(IAudioEndpointVolume))
    volume_2 = cast(interface_2, POINTER(IAudioEndpointVolume))

    tf = open(os.path.join(os.environ['TMP'],'ring_pid'),'w')
    tf.write(str(os.getpid()))
    tf.close()

    [(volume_1.SetMute(False, GUID()),volume_2.SetMasterVolumeLevelScalar(1.0, None),winsound.Beep(6000,int(i*1000))) for i in [0.5]*duration]


def stop_ringing_pc():
    """
    The function `stop_ringing_pc` stops a process with a given PID from running.
    """
    tf = open(os.path.join(os.environ['TMP'],'ring_pid'),'r')
    pid = tf.read()
    tf.close()
    if pid.isdigit():
        os.system(f"taskkill /f /pid {int(pid)}")

def shutdown_pc(delay=10):
    """
    The function `shutdown` shuts down the computer after a specified delay.
    
    :param delay: The `delay` parameter specifies the number of seconds to wait before shutting down the
    computer. By default, it is set to 10 seconds
    """

    os.system(f"shutdown /s /t {delay}")

def restart_pc():
    """
    The function restart_pc uses the os.system command to restart the computer.
    """

    os.system(f"shutdown /r")

def hibernate_pc():
    """
    The function "hibernate_pc" uses the os.system command to initiate a hibernation of the computer.
    """

    os.system(f"shutdown /h")

def lock_pc():
    """
    The function "lock_pc" uses the "os" module to lock the workstation by calling the "LockWorkStation"
    function from the "user32.dll" library.
    """

    os.system("rundll32.exe user32.dll,LockWorkStation")

def grab_picture(save_dir,is_high_res=False):
    """
    The function `grab_picture` captures an image from the computer's camera and saves it to a specified
    directory, with an optional parameter to set the resolution.
    
    :param save_dir: The save_dir parameter is the directory where the captured image will be saved

    :param is_high_res: The parameter "is_high_res" is a boolean value that determines whether the
    captured image should be in high resolution or not. If it is set to True, the camera will be set to
    capture images with a resolution of 1280x720 pixels. If it is set to False, the camera, defaults to
    False (optional)
    """

    try:
        camera = VideoCapture(0)

        if is_high_res:
            camera.set(CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(CAP_PROP_FRAME_HEIGHT, 720)

        if camera.isOpened():
            state, image = camera.read()
            if state:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                imwrite(os.path.join(save_dir,'Camera_'+str(time())+'.png'), image)
            else:
                exit()
    except Exception:
        exit()

def grab_screen(save_dir):
    """
    The function `grab_screen` takes a directory path as input and captures a screenshot of the screen,
    saving it as a PNG file with a timestamp in the specified directory.
    
    :param save_dir: The save_dir parameter is the directory where you want to save the screenshot
    """

    screenshot = ImageGrab.grab()
    screenshot.save(os.path.join(save_dir,'Screenshot_'+str(time())+'.png'))

def grab_video(save_dir,duration):
    """
    The function `grab_video` captures video from the webcam for a specified duration and saves it to a
    specified directory.
    
    :param save_dir: The save_dir parameter is the directory where you want to save the video file

    :param duration: The "duration" parameter specifies the length of time in seconds for which the
    video should be recorded
    """

    vid = VideoCapture(0)
    frames = []
    start_time = getTickCount()
    while True:
        ret, frame = vid.read()
        if ret:
            frames.append(frame)
            current_time = getTickCount()
            elapsed_time = (current_time - start_time) / getTickFrequency()
            if elapsed_time >= duration:
                break
        else:
            break
    vid.release()
    fourcc = VideoWriter_fourcc(*'XVID')
    out = VideoWriter(os.path.join(save_dir,'Video_'+str(time())+'.avi'), fourcc, 20.0, (640, 480))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()


def record_audio(save_dir,duration):
    """
    The `record_audio` function records audio for a specified duration and saves it as a WAV file in the
    specified directory.
    
    :param save_dir: The `save_dir` parameter is the directory where you want to save the recorded audio
    file. It should be a string representing the path to the directory

    :param duration: The "duration" parameter specifies the length of time in seconds for which the
    audio will be recorded
    """

    FORMAT = paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024

    audio = PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    wf = wave.open(os.path.join(save_dir,'Audio_'+str(time())+'.wav'), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        wf.writeframes(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf.close()
