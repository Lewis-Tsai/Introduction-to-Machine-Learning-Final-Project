# %%
import numpy as np
import pretty_midi
# import matplotlib.pyplot as plt

# %%
DATA_DIR = "./"

CHROMA_FS = 100

BASS_UPPER_BOUND = pretty_midi.note_name_to_number("Db5")
BASS_LOWER_BOUND = pretty_midi.note_name_to_number("B0")
BASS_REST_THRESH = 0.25

# %% [markdown]
# ### find bass instrument

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

# %% [markdown]
# ### get beats

# %%
def get_half_bar_beats_from_down_beats(down_beats, end_time):
    half_bar_beats = []

    # half bar beats in complete bar
    for i in range(len(down_beats)-1):
        half_bar_beats.append(down_beats[i])
        half_bar_beats.append((down_beats[i]+down_beats[i+1])/2)

    # half bar beats in incomplete bar
    if half_bar_beats[-2]+(half_bar_beats[-2]-half_bar_beats[-3]) < end_time:
        half_bar_beats[-1] = half_bar_beats[-2]+(half_bar_beats[-2]-half_bar_beats[-3])
    else:
        half_bar_beats.pop()
    
    # append midi end time
    half_bar_beats.append(end_time)
    return np.array(half_bar_beats)

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
    

def get_four_scale_beats(midi_data: pretty_midi.PrettyMIDI):
    end_time = midi_data.get_end_time()
    beats = midi_data.get_beats()
    down_beats = midi_data.get_downbeats()

    # add midi end time to beats and down_beats
    if down_beats[-1] < end_time:
        down_beats = np.array(down_beats.tolist()+[end_time])
    if beats[-1] < end_time:
        beats = np.array(beats.tolist()+[end_time])

    # obtain half_bar_beats and sixteenth_beats
    half_bar_beats = get_half_bar_beats_from_down_beats(down_beats, end_time)
    sixteenth_beats = get_sixteenth_beats_from_beats(beats, end_time)

    return sixteenth_beats, beats, half_bar_beats, down_beats

# %% [markdown]
# ### get chroma feature

# %%
def get_summed_chroma_from_time_squence(chroma, t_seq, ratio=1):
    chroma_per_slot = []
    for i in range(len(t_seq)-1):
        left = int(t_seq[i]*CHROMA_FS)
        right = int(t_seq[i+1]*CHROMA_FS)
        chroma_per_slot.append(chroma[:, left:right].sum(axis=1)/127*ratio)
    return chroma_per_slot

def get_three_scale_chroma(chroma, beats, half_bar_beats, down_beats):
    bar_beat_num_ratio = len(down_beats)/len(beats)
    halfbar_beat_num_ratio = len(half_bar_beats)/len(beats)

    chroma_per_beat = get_summed_chroma_from_time_squence(chroma, beats, 1)
    chroma_per_halfbar = get_summed_chroma_from_time_squence(chroma, half_bar_beats, halfbar_beat_num_ratio)
    chroma_per_bar = get_summed_chroma_from_time_squence(chroma, down_beats, bar_beat_num_ratio)

    return chroma_per_beat,chroma_per_halfbar,chroma_per_bar

# %% [markdown]
# ### get number of simutaneously played instruments

# %%
def get_drum_rolls(midi_data: pretty_midi.PrettyMIDI):
    drum_rolls = []
    for instr in midi_data.instruments:
        instr: pretty_midi.Instrument
        if not instr.is_drum:
            continue
        roll = np.array([0]*int(midi_data.get_end_time()*CHROMA_FS))
        for note in instr.notes:
            note: pretty_midi.Note
            left = int(note.start*CHROMA_FS)
            right = int(note.end*CHROMA_FS)
            roll[left:right] = 1
        drum_rolls.append(roll)
    return np.array(drum_rolls)

# %%
def get_number_of_simutaneously_played_instruments(piano_rolls, drum_rolls, left_t, right_t):
    left = int(left_t*CHROMA_FS)
    right = int(right_t*CHROMA_FS)
    count = 0
    for roll in piano_rolls:
        if (roll[:, left:right]!=0).any():
            count += 1
    for d_roll in drum_rolls:
        if (d_roll[left:right]!=0).any():
            count += 1
    return count

def get_number_of_instruments_per_bar(piano_rolls, drum_rolls, down_beats):
    instrument_per_bar = []
    for i in range(len(down_beats)-1):
        nospi = get_number_of_simutaneously_played_instruments(piano_rolls, drum_rolls, down_beats[i], down_beats[i+1])
        instrument_per_bar.append(nospi)
    return np.array(instrument_per_bar)

# %% [markdown]
# ### get bass 16th note

# %%
def bass_midi_trim(bass_instr: pretty_midi.Instrument):
    for i in range(1, len(bass_instr.notes)):
        if bass_instr.notes[i].start < bass_instr.notes[i-1].end:
            bass_instr.notes[i-1].end = bass_instr.notes[i].start
    return bass_instr

def get_bass_note_in_16th_note(piano_roll: np.ndarray, left_t, right_t):
    left = int(left_t*CHROMA_FS)
    right = int(right_t*CHROMA_FS)
    clip = piano_roll[:,left:right]
    clip = ((clip>0).astype(int)).sum(axis=1)
    
    ans = [0]*(BASS_UPPER_BOUND-BASS_LOWER_BOUND+2)
    if clip.sum() < (right-left+1)*BASS_REST_THRESH:
        ans[-1] = 1
    else:
        ans[np.argmax(clip)] = 1
    return np.array(ans)

# %% [markdown]
# ### midi2input

# %%
def midi_to_input(path):
    midi_data = pretty_midi.PrettyMIDI(path)
    
    ## data preparation
    # bass part (ground truth)
    bass_track = find_bass_instrument(midi_data)
    assert bass_track != None, "didn't find bass instruments in midi file"
    bass_piano_roll = bass_midi_trim(bass_track).get_piano_roll()[BASS_LOWER_BOUND:BASS_UPPER_BOUND+1]
    
    # beat time point
    sixteenth_beats, beats, half_bar_beats, down_beats = get_four_scale_beats(midi_data)

    # chroma
    chroma = midi_data.get_chroma(CHROMA_FS)
    chroma_per_beat, chroma_per_halfbar, chroma_per_bar = get_three_scale_chroma(chroma, beats, half_bar_beats, down_beats)

    # instruments num per bar
    piano_rolls = [instr.get_piano_roll(CHROMA_FS) for instr in midi_data.instruments]
    drum_rolls = get_drum_rolls(midi_data)
    instrument_per_bar = get_number_of_instruments_per_bar(piano_rolls, drum_rolls, down_beats)

    # tempo_changes, time signature
    tempo_changes_time, tempo_changes_tempo = midi_data.get_tempo_changes()
    time_sig_changes = midi_data.time_signature_changes
    if time_sig_changes == []:
        time_sig_changes = [pretty_midi.TimeSignature(4, 4, 0)]
    

    ## run
    # count variable
    half_bar_count = 0
    bar_count = 0
    beat_count = 0
    sixteenth_count = 0
    tempo_change_count = 0
    time_sig_changes_count = 0
    tick_in_bar_count = 0

    # ans
    data_rows = []
    bass_notes = []

    for sixteenth_count in range(len(sixteenth_beats)-1):
        # update bar, halfbar, beat count
        cur_time = sixteenth_beats[sixteenth_count]
        if beat_count+1 < len(beats) and cur_time >= beats[beat_count+1]:
            beat_count += 1
        if half_bar_count+1 < len(half_bar_beats) and cur_time >= half_bar_beats[half_bar_count+1]:
            half_bar_count += 1
        if bar_count+1 < len(down_beats) and cur_time >= down_beats[bar_count+1]:
            bar_count += 1
            tick_in_bar_count = 0
        
        # update tempo, time signature
        if tempo_change_count+1 < len(tempo_changes_time) and cur_time >= tempo_changes_time[tempo_change_count+1]:
            tempo_change_count += 1
        if time_sig_changes_count+1 < len(time_sig_changes) and cur_time >= time_sig_changes[time_sig_changes_count+1].time:
            time_sig_changes_count += 1

        # input part
        row = []
        row.extend(chroma_per_beat[beat_count])
        row.extend(chroma_per_halfbar[half_bar_count])
        row.extend(chroma_per_bar[bar_count])
        row.append(tempo_changes_tempo[tempo_change_count])
        row.append(instrument_per_bar[bar_count])
        row.append(time_sig_changes[time_sig_changes_count].numerator)
        row.append(time_sig_changes[time_sig_changes_count].denominator)
        row.append(tick_in_bar_count)
        row.append(bar_count)
        data_rows.append(row)
        tick_in_bar_count += 1

        # ground truth part
        bass_notes.append(get_bass_note_in_16th_note(bass_piano_roll, cur_time, sixteenth_beats[sixteenth_count+1]))
    return np.array(data_rows), np.array(bass_notes)

# %%
# input_rows, bass_notes = midi_to_input("../input_midi/jazz_standards/4on6.mid")


