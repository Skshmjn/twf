import json
from itertools import permutations
from flask import Flask, request, jsonify

app = Flask(__name__)

distance_dict = {
    "C1 C2": 4,
    "C2 C1": 4,
    "C2 C3": 3,
    "C3 C2": 3,
    "C3 C1": 5,
    "C1 C3": 5,
    "C1 L": 3,
    "C2 L": 2.5,
    "C3 L": 2,
    "L C1": 3,
    "L C2": 2.5,
    "L C3": 2,

}
weight_dict = {}


def possible_paths(center_list=None):
    if center_list is None:
        center_list = ['C1', 'C2', 'C3']
    perm = [list(i) for i in permutations(center_list, len(center_list))]

    new_list = []

    for path in perm:
        for i in range(len(center_list)):
            if i is 0:
                path.append('L')
            else:
                path.insert(i * -2, 'L')

            new_list.append(path[:])

    for i in range(len(new_list)):
        new_list[i] = [str(x + " " + y) for x, y in zip(new_list[i], new_list[i][1:])]

    return new_list


@app.route("/")
def home():
    message = json.dumps({
        "A": 2, "B": 3, "C": 5, "D": 7, "E": 8, "F": 1, "G": 6, "H": 4, "I": 9

    })
    print(message)
    return 'use url http://127.0.0.1:5000/twf and send json in format {}'.format(message)


@app.route("/twf", methods=['POST'])
def entry():
    values = request.get_json()
    weight_dict['C1'] = int(values['A']) * 3 + int(values['B']) * 2 + int(values['C']) * 8
    weight_dict['C2'] = int(values['D']) * 12 + int(values['E']) * 25 + int(values['F']) * 15
    weight_dict['C3'] = int(values['G']) * 0.5 + int(values['H']) + int(values['I']) * 2
    cheapest_path, cheapest_amount = cost(weight_dict)
    cheapest_path = [i[:-2] for i in cheapest_path]
    return str(cheapest_path) + str(cheapest_amount), 200


def cost(weight_from_center):
    weight = 0
    cost_list = []
    path_list = possible_paths()
    for path in path_list:
        cost = 0
        for stops in path:
            distance = distance_dict[stops]
            stop = stops.split()
            if stop[0] == 'L':
                pass
            else:
                weight += weight_from_center[stop[0]]

            if weight <= 5:
                cost += distance * 10
            else:
                cost += distance * 10 + ((weight - 5) / 5) * 8 * distance

            if stop[1] == 'L':
                weight = 0

        cost_list.append(cost)

    return path_list[cost_list.index(min(cost_list))], min(cost_list)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
