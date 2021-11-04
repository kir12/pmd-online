import requests
import argparse
import textwrap
import pdb

BASE_URL = "http://127.0.0.1:8000/compile/"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Useful MIDI processing operations for PMD",
        formatter_class=argparse.RawTextHelpFormatter)

    group1 = parser.add_argument_group('pmd-args', description="Arguments to pass to PMD")

    group1.add_argument(
        "--options", type=str, help=textwrap.dedent('''\
            Optional parameters to pass into PMD:
            \\V\tCompile with Tonedatas & Messages & Filenames
            \\VW\tWrite Tonedata after Compile
            \\N\tCompile on OPN   Mode(Default)
            \\L\tCompile on OPL   Mode
            \\M\tCompile on OPM   Mode
            \\T\tCompile on TOWNS Mode
            \\P\tPlay after Compile Complete
            \\S\tNot Write Compiled File & Play
            \\A\tNot Set ADPCM_File before Play
            \\O\tNot Put Title Messages after Play
            \\C\tCalculate & Put Total Length of Parts
            Example: /v/c\n
        '''))
    group1.add_argument("mml_file", type=str, help="path to .MML file")

    parser.add_argument(
        "-o", "--output", type=str, help="Specify custom .M2 output", default=None)

    results = parser.parse_args()

    data = {}
    if results.output is not None:
        data['output'] = results.output
    x = requests.post(
        BASE_URL, data=data, files={'filename': open(results.mml_file, "r")})
    print(x.text)