import cv2
import numpy as np


class Video:
    """
    Atributes:
    ----------
    video : cv2.VideoCapture
        Video itself
    
    length : int
        Number of frames
    
    width : int
        Pixel video width
    
    height : int
        Pixel video height
    """
    
    def __init__(self, filename):
        """
        Upload videofile with given filename to object.
        
        Parameters:
        -----------
        filename : str
        """
        self.video = cv2.VideoCapture(filename)
        
        self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    def __len__(self):
        return self.length
    
    
    def get_fps(self):
        # returns FPS (frames per second) float value
        return self.video.get(cv2.CAP_PROP_FPS)
    
    
    def get_frame(self, index, new_size=None):
        """
        Returns frame with given index as np.array shape (self.height, self.width, 3)
        
        Parameters:
        -----------
        index : int
            Frame index
        
        new_size : None or tuple with 2 integers
            Change video size if not None
        
        Returns:
        --------
        frame : np.array shape (self.height, self.width, 3) dtype uint8
            Frame itself
        """
        self.video.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self.video.read()
        if new_size is not None:
            frame = cv2.resize(frame, new_size)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
        
    
    def generate_frames(self):
        """
        Yields each frame as np.array shape (self.height, self.width, 3)
        
        Yields:
        np.array shape (self.height, self.width, 3) dtype uint8
        """
        for index in range(self.length):
            yield self.get_frame(index)
    
    
    def get_matrix(self, input_index, output_index, new_size=None):
        """
        Returns np.array of frames in given io-borders 
        as np.array shape (output_index - input_index, self.height, self.width, 3)
        Include input_index, but not output_index
        
        Parameters:
        -----------
        input_index : int
            Input frame index
            
        output_index : int
            Output frame index
        
        new_size : None or tuple with 2 integers
            Change video size if not None
        
        Returns:
        --------
        frames : np.array shape (output_index - input_index, self.height, self.width, 3)
        """
        frames = []
        for index in range(input_index, output_index):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = self.video.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if new_size is not None:
                frame = cv2.resize(frame, new_size)
            frames.append(frame)
        frames = np.array(frames)
        return frames
    
    
    def generate_matrices(self, matrix_length, new_size=None):
        """
        Yields self.length - matrix_length frame matrices 
        as np.array shape (matrix_length, self.height, self.width, 3)
        
        Parameters:
        -----------
        matrix_length : int
            Number of frames in matrix
            
        new_size : None or tuple with 2 integers
            Change video size if not None
        """
        for index in range(self.length - matrix_length):
            yield self.get_matrix(index, index + matrix_length, new_size=new_size)
        


            

def find_all(s, sub):
    # Returns list of beginings of substring
    new_s = s
    poses = []
    previous = 0
    pos = new_s.find(sub)
    while pos != -1:
        poses.append(previous + pos)
        new_s = new_s[pos + len(sub):]
        previous += pos + len(sub)
        pos = new_s.find(sub)
    return poses


def str_to_seconds(time):
    # make float seconds from"HH:MM:SS.XX"
    r = np.array(time.split(':'), dtype=float) * np.array([3600, 60, 1])
    #return round(r.sum(), 3)
    return r.sum()


def get_cuts(filename, fps=None):
    # return array of cut moments (frame_id)
    with open(filename, 'r') as file:
        timeline_str = file.read()
    if fps is None:
        fps = timeline_str[timeline_str.find('fps')-10:timeline_str.find('fps')+3]
        fps = float(fps.replace('fps', ' ').replace('  ', ' ').split(' ')[-2])
        if fps == 23.98:
            fps = 23.976
    times = np.unique([str_to_seconds(timeline_str[i+4:i+16]) for i in find_all(timeline_str, 'in=')])
    if fps == int(fps):
        cuts = np.round(times*fps).astype(int)
    else:
        cuts = (times*fps).astype(int)
    cuts = cuts[1:]
    return cuts