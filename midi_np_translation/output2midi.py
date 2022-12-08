# %%
import pretty_midi
import numpy as np

# %%
BASS_UPPER_BOUND = pretty_midi.note_name_to_number("Db5")
BASS_LOWER_BOUND = pretty_midi.note_name_to_number("B0")
REST = 51

DEFAULT_VELOCITY = 100

# %%
def find_bass_instrument(midi_data: pretty_midi.PrettyMIDI):
    for instr in midi_data.instruments:
        instr: pretty_midi.Instrument
        if instr.program == 32 and not instr.is_drum:
            return instr
    for instr in midi_data.instruments:
        instr: pretty_midi.Instrument
        if instr.program > 32 and instr.program <= 39 and not instr.is_drum:
            return instr

def get_sixteenth_beats_from_beats(beats, end_time):
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

# %%
def output_to_midi(bass_ndarr: np.ndarray, ref_midi_path=None, output_path="bass.mid"):
    midi_data = pretty_midi.PrettyMIDI(ref_midi_path)

    if ref_midi_path == None:
        bass_track = pretty_midi.Instrument(program=32)
        bass_track.notes = []
        midi_data.instruments.append(bass_track)
        sixteenth_beats = np.array([i*0.125 for i in range(len(bass_ndarr)+1)])
    else:
        bass_track = find_bass_instrument(midi_data)
        beats = np.append(midi_data.get_beats(), midi_data.get_end_time())
        sixteenth_beats = get_sixteenth_beats_from_beats(beats, midi_data.get_end_time())
        bass_track.notes = []
    
    note_start_time = 0
    last_pitch = np.argmax(bass_ndarr[0])
    for i in range(1, len(bass_ndarr)):
        cur_pitch = np.argmax(bass_ndarr[i])

        if last_pitch != cur_pitch:
            if last_pitch != REST:
                midi_number = last_pitch+BASS_LOWER_BOUND
                new_note = pretty_midi.Note(DEFAULT_VELOCITY, midi_number, note_start_time, sixteenth_beats[i])
                bass_track.notes.append(new_note)
            note_start_time = sixteenth_beats[i]
            last_pitch = cur_pitch
        
    if last_pitch != REST:
        midi_number = last_pitch+BASS_LOWER_BOUND
        new_note = pretty_midi.Note(DEFAULT_VELOCITY, midi_number, note_start_time, sixteenth_beats[i])
        bass_track.notes.append(new_note)
        
    midi_data.write(output_path)

# %%
# bass_test = np.load("../test_input/4on6.mid.ans.npy")
# input_test = np.load("../test_input/4on6.mid.npy")
# output_to_midi(bass_test, "../input_midi/jazz_standards/4on6.mid")
# output_to_midi(bass_test)


