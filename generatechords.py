import random
import pandas as pd
# from collections import OrderedDict

def gen_measure(note, voices):
    # generate rhythm
    rhythm = gen_rhythm()
    

    
def gen_rhythm():
    rhythm = []
    time = 0.
    d = {'length' : [0.25, 0.5, 1., 2.], 'weight' : [1., 4., 8., 1.]}
    notes = pd.DataFrame(data = d, index = ['sixteenth', 'eighth', 'quarter', 'half'])
    while time < 4:
        notes['weight'] = d['weight']
        for note in notes.index.tolist():
            # print("Time: {}, Note: {}".format(time, note))
            if round(4-time,2) < notes['length'][note]:
               notes['weight'][note] = 0
            if note != 'half':
                m = 1
                while notes['length'][note]*(2**m) < 2: 
                    if time % round(notes['length'][note]*(2**m),2) != 0: 
                        notes['weight'][note] *= 1/notes['length'][note]
                        # import pdb; pdb.set_trace()
                    m += 1
            print("Time: {}, Note: {}, Note Weight: {}".format(time,note,notes['weight'][note]))
        length = random.choices(notes['length'], notes['weight'])[0]
        # import pdb; pdb.set_trace()
        time += length
        rhythm.append(length)
    return rhythm

print(gen_rhythm())
