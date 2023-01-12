# %%
import pretty_midi
import numpy as np

# %%
BASS_UPPER_BOUND = pretty_midi.note_name_to_number("D5")
BASS_LOWER_BOUND = pretty_midi.note_name_to_number("B0")
REST = 52

DEFAULT_VELOCITY = 100

# %% [markdown]
# ### functions from midi2input

# %%
def _find_bass_instrument(midi_data: pretty_midi.PrettyMIDI):
    for instr in midi_data.instruments:
        instr: pretty_midi.Instrument
        if instr.program == 32 and not instr.is_drum:
            return instr
    for instr in midi_data.instruments:
        instr: pretty_midi.Instrument
        if instr.program > 32 and instr.program <= 39 and not instr.is_drum:
            return instr

def _get_sixteenth_beats_from_beats(beats, end_time):
    sixteenth_beats = []
    # sixteenth_beats in complete beat
    for i in range(len(beats)-2):
        for j in range(4):
            sixteenth_beats.append((beats[i]*(4-j)+beats[i+1]*j)/4)

    # sixteenth_beats in incomplete beat
    for j in range(4):
        temp = (beats[-2]-beats[-3])/4*j + beats[-2]
        if temp > end_time:
            break
        sixteenth_beats.append(temp)
    # append midi end time
    sixteenth_beats.append(end_time)
    return np.array(sixteenth_beats)

# %% [markdown]
# ### output2midi

# %%
def output_to_midi(bass_ndarr: np.ndarray, ref_midi_path=None, output_path="bass.mid"):
    """
    bass_ndarr: a np.ndarray represents bass notes, which supposely has the same shape of .ans.npy.
                You can use `ndarr_obj.reshape((-1,52))` to reshape your input, or this function will do for you.

    ref_midi_path: the original midi file with bass and other instruments, the function will
                replace the bass track by the bass line you input. If it's None, only the bass 
                track will be output.
                
    output_path: the name of output midi file
    """
    bass_ndarr = np.reshape(bass_ndarr, (-1, 52))
    # if there is a reference midi file, create new midi file by modifying it, otherwise use defalt setting
    midi_data = pretty_midi.PrettyMIDI(ref_midi_path)
    if ref_midi_path == None:
        sixteenth_beats = np.array([i*0.125 for i in range(len(bass_ndarr)+1)])

        bass_track = pretty_midi.Instrument(program=32)
        bass_track.notes = []
        midi_data.instruments.append(bass_track)
    else:
        beats = np.append(midi_data.get_beats(), midi_data.get_end_time())
        sixteenth_beats = _get_sixteenth_beats_from_beats(beats, midi_data.get_end_time())

        bass_track = _find_bass_instrument(midi_data)
        bass_track.notes = []
    
    # appending notes according to bass_ndarr
    note_start_time = 0
    last_pitch = np.argmax(bass_ndarr[0])
    for i in range(1, len(bass_ndarr)):
        cur_pitch = np.argmax(bass_ndarr[i])
        if last_pitch != cur_pitch:
            if last_pitch != REST:
                midi_number = last_pitch + BASS_LOWER_BOUND
                new_note = pretty_midi.Note(DEFAULT_VELOCITY, midi_number, note_start_time, sixteenth_beats[i])
                bass_track.notes.append(new_note)
            note_start_time = sixteenth_beats[i]
            last_pitch = cur_pitch

    # flush the last note at the end of track
    if last_pitch != REST:
        midi_number = last_pitch+BASS_LOWER_BOUND
        new_note = pretty_midi.Note(DEFAULT_VELOCITY, midi_number, note_start_time, sixteenth_beats[-1])
        bass_track.notes.append(new_note)
    
    # write file
    midi_data.write(output_path)