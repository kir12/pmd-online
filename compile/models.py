from django.db import models
import uuid 


class PMDUpload(models.Model):
    returned_m2_filename = models.CharField(max_length=10, blank=True)
    internal_filename = models.CharField(max_length=10, blank=True)
    mml_file = models.FileField(upload_to='uploads/')
    m2_file = models.FileField(blank=True, upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        internal_name = str(uuid.uuid4())[:6]
        self.mml_file.name = f"{internal_name}.mml"
        self.internal_filename = internal_name
        super(PMDUpload, self).save(*args, **kwargs)
