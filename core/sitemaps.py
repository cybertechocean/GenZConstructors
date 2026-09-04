from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Project

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:services',
            'core:projects',
            'core:process',
            'core:testimonials',
            'core:faqs',
            'core:request_quote',
            'core:contact',
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    priority = 0.85
    changefreq = 'weekly'

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
