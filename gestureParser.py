from json import loads

__author__ = 'doxer'

file = '11_10_SM'
input_json = 'data/' + file + '.json'
output_txt = 'data/' + file + '.txt'

with open(input_json) as jsonFile:
    json_data = loads(jsonFile.read())

st = {'O': 1, 'ok': 1, '1': 1, '2': 1, '3': 1, '4': 2, '5': 2, '6': 1, '9': 1, 'z': 1, '2v': 2, '2vh': 4, '2h': 2,
      '3v': 3, '3h': 3, '3vh': 6, '2v_diff': 2, '2w': 2, '2w_diff': 2, '2v_up': 2}

fin = {'O': 1, 'ok': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '9': 1, 'z': 1, '2v': 2, '2vh': 2, '2h': 2,
       '3v': 3, '3h': 3, '3vh': 3, '2v_diff': 1, '2w': 2, '2w_diff': 1, '2v_up': 2, '+': 1, 'B': 1, 'W': 1, 'x': 1,
       'o': 1, '3hv': 3,
       '2h_diff': 1}


def parse_gesture(gesture):
    tag = gesture['tag']
    if tag == '2h_diff':
        return
    x = gesture['x']
    y = gesture['y']
    t = gesture['t']
    sid = gesture['id']
    if tag not in fin:
        print "ERROR " + tag
        return

    fingers = fin[tag]
    strokes = len(set(sid))

    with open(output_txt, mode='a') as f:
        f.write("{0}\n".format(' '.join(str(s) for s in (tag, fingers, strokes, len(x)))))
        for px, py, pt, psid in zip(x, y, t, sid):
            f.write("{0} {1} {2} {3}\n".format(px, py, pt, psid))


print json_data[0].keys()

for gesture in json_data:
    parse_gesture(gesture)