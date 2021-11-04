from django.db import models
import uuid 
from django.core.files.base import ContentFile

def save_path(instance, filename):
    return f"uploads/{instance.directory_name}/{filename}"

class PMDUpload(models.Model):
    mml_file = models.FileField(upload_to=save_path)
    dosbox_output_file = models.FileField(blank=True, upload_to=save_path)
    pmd_output_file = models.FileField(blank=True, upload_to=save_path)
    created = models.DateTimeField(auto_now_add=True)
    directory_name = models.CharField(max_length=10, default = "dir")
    # TODO: PMD parameters?

    def save(self, *args, **kwargs):
        self.directory_name = str(uuid.uuid4())[:6]
        self.mml_file.name = self.mml_file.name.upper()
        self.pmd_output_file.name = args.output_name.upper()
        self.dosbox_output_file.name = "dosbox_output.txt"
        # self.dosbox_output_file.save(
        #     "dosbox_output.txt", ContentFile(''))
        super(PMDUpload, self).save(*args, **kwargs)
