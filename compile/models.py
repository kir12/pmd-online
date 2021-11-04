from django.db import models
import uuid


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
        self.dosbox_output_file.name = save_path(self, "dosbox_output.txt")
        self.pmd_output_file.name = save_path(self, self.pmd_output_file.name)
        super(PMDUpload, self).save(*args, **kwargs)
