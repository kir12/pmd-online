from django.db import models
import uuid

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

def save_path(instance, filename):
    return f"uploads/{instance.directory_name}/{filename.upper()}"


class PMDUpload(models.Model):
    mml_file = models.FileField(upload_to=save_path)
    dosbox_output_file = models.FileField(blank=True, upload_to=save_path)
    pmd_output_file = models.FileField(blank=True, upload_to=save_path)
    created = models.DateTimeField(auto_now_add=True)
    directory_name = models.CharField(max_length=10, default="dir")
    # TODO: PMD parameters?

    def save(self, *args, **kwargs):
        self.directory_name = str(uuid.uuid4())[:6]
        self.dosbox_output_file.name = save_path(self, "dosbox.txt")
        self.pmd_output_file.name = save_path(self, self.pmd_output_file.name)
        super(PMDUpload, self).save(*args, **kwargs)

    # convert mml file to CLRF ending
    def clrf_endings(self):
        with open(f"media/{self.mml_file.name}", 'rb') as file:
            content = file.read()

        content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

        with open(f"media/{self.mml_file.name}", 'wb') as file:
            file.write(content)
