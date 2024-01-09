import os
from django.core.exceptions import ValidationError



def validate_file_extension(value):
    # Get path and filename
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')