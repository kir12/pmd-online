import requests
import argparse
import pdb

BASE_URL = "http://127.0.0.1:8000/compile/"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Useful MIDI processing operations for PMD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("mml_file", type=str, help="path to .mml file")
    parser.add_argument("-o", "--output", type=str, help="optional .m2 output filename", default=None)

    results = parser.parse_args()

    data = {}
    if results.output is not None:
        data['output'] = results.output
    x = requests.post(
        BASE_URL, data=data, files={'filename': open(results.mml_file, "r")})
    print(x.text)