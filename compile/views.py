from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import re
from .models import PMDUpload
import subprocess
import time

MC_PATH = Path(__file__).parent.absolute()/'MCE.EXE'


# Create your views here.
@api_view(['POST'])
def index(request):

    # (attempt to) load MML file and construct output name
    try:
        file = request.FILES['filename']
        assert(Path(file.name).suffix == ".mml")
        output = request.POST.get('output')
        if output is None:
            output = file.name
        output = Path(output).stem
        output = re.sub("[^a-zA-z0-9]", "", output)[:6]
        output = str(Path(output).with_suffix(".m2"))
    except BaseException:
        return Response({
            'error': "An invalid file was supplied."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # initialize PMDUpload db object and call save on objects
    save_obj = PMDUpload(pmd_output_file=output, mml_file=file)
    save_obj.save()
    save_obj.clrf_endings()

    # run PMD
    # "dosbox", str(MC_PATH), ">>", save_obj.dosbox_output_file.path]
    popen_inst = [
        "dosbox",
        "-c", "MOUNT C \"compile\"",
        "-c", f"MOUNT D \"media/uploads/{save_obj.directory_name}/\"",
        "-c", "C:",
        "-c", f"MCE.EXE /v D:\\{Path(save_obj.mml_file.name).name}> D:\\{Path(save_obj.dosbox_output_file.name).name}",
        "-c", "exit"
        ]

    subprocess.Popen(popen_inst)
    # dosbox -c 'MOUNT C "compile"' -c "C:" -c "MCE.EXE > test.txt" -c "exit"

    # check if file created
    while not Path(f"media/{save_obj.dosbox_output_file}").is_file():
        time.sleep(0.1)
    
    return Response({
        'file': file.name,
        'output': output
    })
