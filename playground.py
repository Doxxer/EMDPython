from json import loads

__author__ = 'doxer'

file = 'full'
input_json = 'data/' + file + '.json'
output_txt = 'data/' + file + '.txt'

with open(input_json) as jsonFile:
    json_data = loads(jsonFile.read())


def parse_gesture(gesture):
    tag = gesture['tag']
    x = gesture['x']
    y = gesture['y']
    t = gesture['t']
    fingers = 1
    strokes = len(set(gesture['id']))

    with open(output_txt, mode='a') as f:
        f.write("{0}\n".format(' '.join(str(s) for s in (tag, fingers, strokes, len(x)))))
        for px, py, pt in zip(x, y, t):
            f.write("{0} {1} {2}\n".format(px, py, pt))


parse_gesture(json_data[0])

for gesture in json_data:
    parse_gesture(gesture)
