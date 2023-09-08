from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path, PureWindowsPath
import re
from .models import PMDUpload
import subprocess
import time
import base64
import os.path
from pmdonline.settings import MEDIA_ROOT
from io import StringIO
from django.core.files import File 


MC_PATH = Path(__file__).parent.absolute()/'MCE.EXE'

@api_view(['GET'])
def help(request):
    
    # construct command string
    outputpath = str(Path(__file__).parent / "output.txt")
    pth = str(PureWindowsPath(__file__).relative_to(Path.home()).parent)
    thiscmd = ["dosemu", "-dumb", f'"D: || cd {pth} || MCE.EXE"']
    if "root" in pth:
        thiscmd = ["xdotool","key","Enter","|"] + thiscmd
    thiscmd += [">",outputpath]

    # save it to a script.sh file 
    with open(str(Path(__file__).parent /"script.sh"),"w") as f:
        print(" ".join(thiscmd), file=f)

    # execute the script
    subprocess.run(["sh",str(Path(__file__).parent / "script.sh")])
    with open(outputpath,"r") as f:
        out = f.read()
        return Response({"msg":out}, status = status.HTTP_200_OK)

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

    dosemupath_absolute = Path(__file__).parent
    mmlfilepath_absolute = Path(save_obj.mml_file.path)

    mmlfilepath_relative =  str(PureWindowsPath(os.path.relpath(mmlfilepath_absolute.resolve(), dosemupath_absolute.resolve())))
    dosemupath_relative = str(PureWindowsPath(dosemupath_absolute.relative_to(Path.home())))

    # construct command string
    outputpath = str(Path(__file__).parent / "output.txt")
    thiscmd = ["dosemu", "-dumb", f'"D: || cd {dosemupath_relative} || MCE.EXE {mmlfilepath_relative}"']
    if "root" in str(Path.home()):
        thiscmd = ["xdotool","key","Enter","|"] + thiscmd
    thiscmd += [">",outputpath]

    # generate script.sh file
    save_obj.script_file.save("script.sh", File(StringIO(" ".join(thiscmd))))

    # # save it to a script.sh file 
    # with open(str(Path(__file__).parent /"script.sh"),"w") as f:
    #     print(" ".join(thiscmd), file=f)

    # execute the script
    subprocess.run(["sh",save_obj.script_file.path])
    with open(outputpath,"r") as f:
        out = f.read()
        return Response({"pmd_response":out}, status = status.HTTP_200_OK)

    # # run PMD
    # file_params = f"D:\\{Path(save_obj.mml_file.name).name}"
    # if ff_file is not None:
    #     file_params += f" D:\\{Path(save_obj.ff_file.name).name}"
    # dos_pipe = f"> D:\\{Path(save_obj.dosbox_output_file.name).name}"
    # popen_inst = [
    #     "dosbox",
    #     "-c", "MOUNT C \"compile\"",
    #     "-c", f"MOUNT D \"media/uploads/{save_obj.directory_name}/\"",
    #     "-c", "C:",
    #     "-c", f"MCE.EXE {options} {file_params} {dos_pipe}",
    #     "-c", "exit"
    #     ]

    # subprocess.check_output(popen_inst, timeout=3)
    # # dosbox -c 'MOUNT C "compile"' -c "C:" -c "MCE.EXE > test.txt" -c "exit"

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
