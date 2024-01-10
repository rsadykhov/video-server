import os
from django.db import models
from django.dispatch import receiver
import json
from .validators import validate_file_extension
from .recommender_system import get_recommendations



class Videos(models.Model):
    class Meta:
        verbose_name = "Videos"
        verbose_name_plural = "Videos"

    title = models.CharField(max_length=127, unique=True, verbose_name="Title")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    video = models.FileField(blank=False, null=False, upload_to="videos", validators=[validate_file_extension], verbose_name="Video")
    categories = models.ManyToManyField("Categories", blank=True, through="videos.VideoCategoriesThrough", verbose_name="Categories")
    tags = models.ManyToManyField("Tags", blank=True, through="videos.VideoTagsThrough", verbose_name="Tags")
    uploaded_on = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded On")
    similar_videos = models.JSONField(default=dict, blank=True, null=True, verbose_name="Similar Videos")
    opposite_videos = models.JSONField(default=dict, blank=True, null=False, verbose_name="Opposite Videos")
    add_to_hidden = models.BooleanField(default=False, verbose_name="Add To Hidden")

    def __str__(self):
        return f"{self.title}"
    
    def clean(self, *args, **kwargs):
        recommendations = get_recommendations(video_pk=self.pk)
        self.similar_videos = json.dumps(recommendations["similar"])
        self.opposite_videos = json.dumps(recommendations["opposite"])
        super().clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)



class Categories(models.Model):
    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"
    
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    n_items = models.SmallIntegerField(default=0, verbose_name="Number of Items in Category")

    def __str__(self):
        return f"{self.name}"



class VideoCategoriesThrough(models.Model):
    """
    Through model between Videos and Categories. 
    Updates Categories model when a new relationship is added.
    """
    class Meta:
        verbose_name = "Video Categories"
        verbose_name_plural = "Video Categories"
    
    video = models.ForeignKey("Videos", on_delete=models.CASCADE)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.video}: {self.category}"
    
    def __custom_validation_after_save(self):
        n_categories = len(VideoCategoriesThrough.objects.filter(category=self.category))
        t = Categories.objects.get(id=self.category.id)
        t.n_items = n_categories
        t.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__custom_validation_after_save()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.__custom_validation_after_save()



class Tags(models.Model):
    class Meta:
        verbose_name = "Tags"
        verbose_name_plural = "Tags"
    
    name = models.CharField(max_length=255, unique=True, verbose_name="Tag Name")
    n_items = models.SmallIntegerField(default=0, verbose_name="Number of Tagged Items")

    def __str__(self):
        return f"{self.name}"



class VideoTagsThrough(models.Model):
    """
    Through model between Videos and Tags. 
    Updates Tags model when a new relationship is added.
    """
    class Meta:
        verbose_name = "Video Tags"
        verbose_name_plural = "Video Tags"
    
    video = models.ForeignKey("Videos", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tags", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.video}: {self.tag}"
    
    def __custom_validation_after_save(self):
        n_tags = len(VideoTagsThrough.objects.filter(tag=self.tag))
        t = Tags.objects.get(id=self.tag.id)
        t.n_items = n_tags
        t.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__custom_validation_after_save()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.__custom_validation_after_save()




@receiver(models.signals.post_delete, sender=Videos)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Videos` object is deleted.
    """
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)



@receiver(models.signals.pre_save, sender=Videos)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when corresponding `Videos` object is updated with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = Videos.objects.get(pk=instance.pk).video
    except Videos.DoesNotExist:
        return False
    new_file = instance.video
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)