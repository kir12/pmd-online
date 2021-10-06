from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import re


# Create your views here.
@api_view(['POST'])
def index(request):

    # (attempt to) load MML file and optional output name
    try:
        file = request.FILES['filename']
        assert(Path(file.name).suffix == ".mml")
        output = request.POST.get('output')
        if output is None:
            output = file.name
        output = re.sub("[^a-zA-z0-9]", "", output)[:6]
        output = str(Path(output).with_suffix(".m2"))
    except BaseException:
        return Response({
            'error': "An invalid file was supplied."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: run PMD

    return Response({
        'file': file.name,
        'output': output
    })
