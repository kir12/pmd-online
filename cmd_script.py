from re import I
import requests
import argparse
import textwrap
import base64
import pdb
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/compile/"

if __name__ == "__main__":

    # construct and parse arguments
    parser = argparse.ArgumentParser(
        description="Web-based hosting of PMD",
        formatter_class=argparse.RawTextHelpFormatter)

    group1 = parser.add_argument_group(
        'pmd-args', description="Arguments to pass to PMD")

    group1.add_argument(
        "--options", type=str, default="", help=textwrap.dedent('''\
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
    group1.add_argument("mml_file", type=str, help="path to .MML file\n\n")

    group1.add_argument(
        "--extra-files",
        type=str, nargs="+", help="optional extra files")

    parser.add_argument(
        "--output", type=str, help="Specify custom .M2 output",
        default=None)

    results = parser.parse_args()

    # put together data payload
    data = {'options': results.options}
    if results.output is not None:
        data['output'] = results.output

    payload = {
        'filename': open(results.mml_file, "r"),
    }
    
    if results.extra_files is not None:
        for idx, val in enumerate(results.extra_files):
            payload[f"extra_files_{idx}"] = open(val, "rb")
    # issue post request and get json
    x = requests.post(
        BASE_URL, data=data, files=payload)
    x = x.json()

    print(x)

    #args # print PMD output
    # if 'pmd_response' in x:
    #     print(x["pmd_response"])
    # else:
    #     print(x["pmd_error"])

    # # get M2 output if possible
    # if 'pmd_output_filename' in x:
    #     # connect optional results output path with final filename
    #     if results.output is not None:
    #         w_path = (Path(results.output).parent)/x["pmd_output_filename"]
    #     else:
    #         w_path = Path(x["pmd_output_filename"])

    #     # write m2 file
    #     with open(str(w_path), "wb") as f:
    #         pmd_raw_content = base64.b64decode(x["pmd_output_file"])
    #         f.write(pmd_raw_content)