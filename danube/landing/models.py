from django.db import models
from ckeditor.fields import RichTextField


class Testimonial(models.Model):
    name = models.CharField(
        max_length=250, null=False, blank=False, help_text="Testimonial's owner name"
    )
    title = models.CharField(
        max_length=250, null=False, blank=False, help_text="Job title"
    )
    content = RichTextField(null=False, blank=False, help_text="Testimonial's content")

    def __str__(self):
        return str(self.name)


class FAQ(models.Model):
    question = models.CharField(
        max_length=500, null=False, blank=False, help_text="Question text"
    )
    answer = RichTextField(null=False, blank=False, help_text="Answer to the question.")

    def __str__(self):
        return str(self.question)
