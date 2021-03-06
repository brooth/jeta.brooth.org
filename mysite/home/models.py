from __future__ import unicode_literals
import os

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.sitemaps import Sitemap

from markdown import markdown


class MarkdownPage(models.Model):
    title = models.CharField(max_length=140)
    path = models.CharField(max_length=140, unique=True, blank=True)
    md_filename = models.CharField(max_length=100)
    html_content = models.TextField(editable=False, blank=True, null=True)
    modified_ts = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        filename = settings.MARKDOWN_FILES_URL + self.md_filename
        if(os.path.exists(filename)):
            md_file = open(filename, 'r+')
            self.html_content = markdown(md_file.read(), extensions=['codehilite'])
            md_file.close()
        else:
            md_file = open(filename, 'w+')
            md_file.write('<div class="page-header">\n\t<h2></h2>\n</div>')
            md_file.close()
            self.html_content = 'Under construction'

        super(MarkdownPage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + ' ~ (' + self.path + ') ~ (' + self.md_filename + ')'


class MarkdownPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return MarkdownPage.objects.all()

    def lastmod(self, obj):
        return obj.modified_ts

    def location(self, item):
        return '/' + item.path


class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['/donate.html']

    def location(self, item):
        return item
