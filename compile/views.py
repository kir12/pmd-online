from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import re
from .models import PMDUpload
import subprocess
import time
import base64

MC_PATH = Path(__file__).parent.absolute()/'MCE.EXE'

@api_view(['GET'])
def help(request):
    return Response({"msg":"sign things are working refresh"}, status = status.HTTP_200_OK)

# Create your views here.
@api_view(['POST'])
def index(request):

    # (attempt to) load MML file and construct output name
    try:
        # retrieve MML file and output name if possible
        file = request.FILES['filename']
        assert(Path(file.name).suffix.upper() == ".MML")
        output = request.POST.get('output')
        if output is None:
            output = file.name
        output = Path(output).stem
        output = re.sub("[^a-zA-z0-9]", "", output)[:6]
        output = str(Path(output).with_suffix(".m2"))

        # get options
        options = request.POST.get('options')

        # retrieve FF file if possible
        ff_file = None
        if 'ff-file' in request.FILES:
            ff_file = request.FILES['ff-file']
            assert(Path(ff_file.name).suffix.upper() == ".FF")

    # return bad request if possible
    except BaseException:
        return Response({
            'pmd_error': "An invalid file was supplied."
        }, status=status.HTTP_400_BAD_REQUEST)

    # initialize PMDUpload db object and call save on objects
    save_obj = PMDUpload(
        pmd_output_file=output,
        mml_file=file, ff_file=ff_file)
    save_obj.save()
    save_obj.clrf_endings()

    # run PMD
    file_params = f"D:\\{Path(save_obj.mml_file.name).name}"
    if ff_file is not None:
        file_params += f" D:\\{Path(save_obj.ff_file.name).name}"
    dos_pipe = f"> D:\\{Path(save_obj.dosbox_output_file.name).name}"
    popen_inst = [
        "dosbox",
        "-c", "MOUNT C \"compile\"",
        "-c", f"MOUNT D \"media/uploads/{save_obj.directory_name}/\"",
        "-c", "C:",
        "-c", f"MCE.EXE {options} {file_params} {dos_pipe}",
        "-c", "exit"
        ]

    subprocess.check_output(popen_inst, timeout=3)
    # dosbox -c 'MOUNT C "compile"' -c "C:" -c "MCE.EXE > test.txt" -c "exit"

    response = {}
    # grab PMD output if possible
    if Path(f"media/{save_obj.dosbox_output_file.name}").is_file():
        response['pmd_response'] = base64.b64encode(
            save_obj.dosbox_output_file.open().read())
    else:
        response['pmd_error'] = "Warning: PMD timed out while compiling your music file!"

    # grab rendered file if possible
    if Path(f"media/{save_obj.pmd_output_file.name}").is_file():
        response['pmd_output_file'] = base64.b64encode(
            save_obj.pmd_output_file.open().read())
    response['pmd_output_filename'] = Path(save_obj.pmd_output_file.name).name

    return Response(response)
