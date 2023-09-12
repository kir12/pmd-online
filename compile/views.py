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
        # ff_file = None
        # if 'ff-file' in request.FILES:
        #     ff_file = request.FILES['ff-file']
        #     assert(Path(ff_file.name).suffix.upper() == ".FF")

    # return bad request if possible
    except BaseException:
        return Response({
            'pmd_error': "An invalid file was supplied."
        }, status=status.HTTP_400_BAD_REQUEST)

    # initialize PMDUpload db object and call save on objects
    save_obj = PMDUpload(
        pmd_output_file=output,
        mml_file=file, options=options ) # , ff_file=ff_file)
    save_obj.save()
    save_obj.clrf_endings()

    # devise relative paths for dosemu
    dosemupath_absolute = Path(__file__).parent.parent
    mmlfilepath_absolute = Path(save_obj.mml_file.path)
    mmlfilepath_relative = str(PureWindowsPath(mmlfilepath_absolute.relative_to(dosemupath_absolute)))
    dosemupath_relative = str(PureWindowsPath(dosemupath_absolute.relative_to(Path.home())))

    # generate output files
    save_obj.pmd_output_file.save("OUTPUT.TXT", File(StringIO("")))
    save_obj.m2file.save(Path(save_obj.mml_file.name).with_suffix(".m2").name, File(StringIO("")))

    # construct command string
    outputpath = save_obj.pmd_output_file.path 
    thiscmd = ["dosemu", "-dumb", f'"D: || cd {dosemupath_relative} || compile\\MCE.EXE {save_obj.options} {mmlfilepath_relative}"']
    if "root" in str(Path.home()):
        thiscmd = ["xdotool","key","Enter","|"] + thiscmd
    thiscmd += [">",outputpath]

    # generate script.sh file
    save_obj.script_file.save("SCRIPT.SH", File(StringIO(" ".join(thiscmd))))

    # execute the script
    subprocess.run(["sh",save_obj.script_file.path])
    with open(outputpath,"r") as f:
        out = f.read()

    response = {"pmd_response":out}

    # normally encoding files in base64 is bad, but M2 files max out at 40 - 50 Kb which is negligibly small
    if Path(save_obj.m2file.path).is_file():
        response["m2file"] = base64.b64encode(
            save_obj.m2file.open().read()
        )
        response["status"] = 0
    else:
        response["m2file"] = ""
        response["status"] = 1

    save_obj.delete()    

    return Response(response, status = status.HTTP_200_OK)

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
