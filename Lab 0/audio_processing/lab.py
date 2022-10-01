# No Imports Allowed!


from turtle import right


def backwards(sound):
    """
    Reverse the input sound by reversing the order of the samples without modifying the input.
    
    Example sound input:
    s = {
    'rate': 8000,
    'samples': [1.00, 0.91, 0.67, 0.31, -0.10, -0.50, -0.81, -0.98, -0.98, -0.81],
    }
    
    Example output:
    [2,323,454,5545]
    -> [5545, 454, 323, 2]
    
    Returns:
    Dict: reversed sound file
    """
    samples = sound['samples'].copy() #use .copy() so the pointers in memory don't overwrite those for input
    samples.reverse()
    output_sound = {'rate': sound['rate'], 'samples': samples}
    return output_sound


def mix(sound1, sound2, p):
    """
    Mixes sound1 and sound2 of same sampling rate with parameter p, without modifying the original sound files.
    Returns None if the sampling rate is different. Result should have length that is minimum of the 
    sound file lengths.
    
    mixed_samples = p x first sound samples, (1-p) x second sound samples
    
    Returns:
    Dict: Mixed sound file
    """
    # First check that sampling rates match, if not return None
    if sound1['rate'] != sound2['rate']:
        return None  
    samples1 = sound1['samples'].copy()
    samples2 = sound2['samples'].copy()
    # use list comprehension to zip the two different copies of the samples together, make sure both samples exist
    # i.e. taking the minimum length, then do the calculation/conversion on the individual samples
    mixed_samples = [(sample1 * p) + (sample2 * (1-p)) for sample1, sample2 in zip(samples1, samples2) if (sample1, sample2)]
    mixed_sound = {'rate': sound1['rate'], 'samples': mixed_samples}
    return mixed_sound


def echo(sound, num_echoes, delay, scale):
    """
    Create an echoed version of the inputted sound file.
    Delay and scale down a copy of the samples, for each num of echoes.
    
    Input:
    sound: a dictionary representing the original sound
    num_echoes: the number of additional copies of the sound to add
    delay: the amount (in seconds) by which each "echo" should be delayed
    scale: the amount by which each echo's samples should be scaled
    
    1 2 3 4 5
          1 2 3 4 5 * scale
                1 2 3 4 5 * scale
    
    sample_delay = round(delay * sound['rate']) - for the num of samples in the delay
    Returns:
    Dict: echoed sound file
    """
    delay_samples = sound['samples'].copy()
    sample_delay = round(delay * sound['rate']) # num of samples in the delay
    delay_index = sample_delay
                
    scaled_samples = [sample * scale for sample in delay_samples]
    for n in range(num_echoes):          
        if n != 0:
            # scale the scaled samples if not the first run
            scaled_samples = [sample * scale for sample in scaled_samples] 
        while delay_index - len(delay_samples) > 0:
            delay_samples.append(0)
        index = delay_index
        if index == len(delay_samples):
            for i in range(len(scaled_samples)):
                delay_samples.append(scaled_samples[i])
        else:
            # NEED to save the length beforehand b/c the length is increased in the loop
            # which affects the conditional statement below
            len_delay_samples = len(delay_samples) 
            for i in range(len(scaled_samples)):
                if index < len_delay_samples:
                    delay_samples[index] += scaled_samples[i]
                    index += 1
                else:
                    delay_samples.append(scaled_samples[i])
        delay_index += sample_delay
    delayed_sound = {'rate': sound['rate'], 'samples': delay_samples} # create sound object
    
    return delayed_sound


def pan(sound):
    """
    Create a spatial effect of panning from left to right in stereo without modifying original file.
    Volume in left channel decreases as right volume increases.
    
    Input:
    Dict: stereo sound file of the format.
    Example:
    s = {
    'rate': 8000,
    'left': [0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59],
    'right': [1.00, 0.91, 0.67, 0.31, -0.10, -0.50, -0.81, -0.98, -0.98, -0.81],
    }
    
    Returns:
    Dict: panned sound file
    """
    left_samples = sound['left'].copy()
    right_samples = sound['right'].copy()
    num_samples = len(left_samples)
    
    for i in range(len(left_samples)): # left and right samples should have same length
        left_samples[i] = left_samples[i]*(1 - i/(num_samples - 1)) # scale left and right channels
        right_samples[i] = right_samples[i]*(i/(num_samples - 1))
        
    panned_sound = {'rate': sound['rate'], 'left': left_samples, 'right': right_samples}
    return panned_sound


def remove_vocals(sound):
    """
    Removes the vocals from the track by subtracting the difference between L and R channels into mono samples.
    Mono sample = (left - right)
    
    Inputs:
    Dict: input *stero* sound file
    
    Returns:
    Dict: mono sound file with (mostly) no vocals
    """
    left_samples = sound['left'].copy()
    right_samples = sound['right'].copy()
    mono_samples = [left - right for left, right in zip(left_samples, right_samples)]
    no_vocals_sound = {'rate': sound['rate'], 'samples': mono_samples}
    return no_vocals_sound


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
from json import load
import wave
import struct


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l, r in zip(sound["left"], sound["right"]):
            l = int(max(-1, min(1, l)) * (2**15 - 1))
            r = int(max(-1, min(1, r)) * (2**15 - 1))
            out.append(l)
            out.append(r)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/meow.wav, rather than just as meow.wav, to account for the sound
    # files being in a different directory than this file)
    # meow = load_wav("sounds/meow.wav")
    # water_wav = load_wav("sounds/water.wav")
    # synth = load_wav("C:/Users/colos/OneDrive - Massachusetts Institute of Technology/Sophomore/6.1010/Labs/Lab 0/audio_processing/sounds/synth.wav")
    # inp = {'rate': 9, 'samples': [1,2,3]}
    # s = {
    # 'rate': 8,
    # 'samples': [1, 2, 3, 4, 5],
    # }
    # chord = load_wav('sounds/chord.wav')
    # car = load_wav('sounds/car.wav', stereo=True)
    lookout_mountain = load_wav('sounds/lookout_mountain.wav', stereo=True)
    
    write_wav(remove_vocals(lookout_mountain), "no_vocals_lookout.wav")

    # write_wav(backwards(meow), 'meow_reversed.wav')
