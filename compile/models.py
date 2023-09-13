from django.db import models
import uuid
from pathlib import Path
from pmdonline.settings import MEDIA_ROOT

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
UUID_LIMIT = 5

def save_path(instance, filename):
    return f"uploads/{str(instance.uuidterm)[:UUID_LIMIT]}/{filename.upper()}"

# primary class for uploading PMD files
class PMDUpload(models.Model):
    mml_file = models.FileField(upload_to=save_path)
    m2file = models.FileField(blank=True, upload_to=save_path)
    pmd_output_file = models.FileField(blank=True, upload_to=save_path)
    script_file = models.FileField(null=True, blank=True, upload_to=save_path)
    created = models.DateTimeField(auto_now_add=True)
    uuidterm = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    options = models.CharField(null=True, blank=True, max_length=50)
    # TODO: PMD parameters?

    def save(self, *args, **kwargs):
        # self.dosbox_output_file.name = save_path(self, "dosbox.txt")
        # self.pmd_output_file.name = save_path(self, self.pmd_output_file.name)
        # self.script_file.name = save_path(self, "script.sh")
        super(PMDUpload, self).save(*args, **kwargs)

    # convert mml file to CLRF ending
    def clrf_endings(self):
        with open(f"media/{self.mml_file.name}", 'rb') as file:
            content = file.read()

        content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

        with open(f"media/{self.mml_file.name}", 'wb') as file:
            file.write(content)

    def delete(self):
        self.mml_file.delete()
        self.pmd_output_file.delete()
        self.script_file.delete()
        self.m2file.delete()
        Path(f"{MEDIA_ROOT}/uploads/{str(self.uuidterm)[:UUID_LIMIT]}/").rmdir()
        super(PMDUpload, self).delete()

def extrafile_savepath(instance, filename):
    return f"uploads/{str(instance.pmdupload.uuidterm)[:UUID_LIMIT]}/{filename.upper()}"

# additional files that are passed along that PMD needs to compile
class ExtraFile(models.Model):
    pmdupload = models.ForeignKey("PMDUpload", on_delete=models.CASCADE)
    extrafile = models.FileField(null=True, blank=True, upload_to=extrafile_savepath)

    def delete(self):
        self.extrafile.delete()
        super(ExtraFile, self).delete()
