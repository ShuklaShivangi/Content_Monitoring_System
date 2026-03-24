from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ContentItem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    source = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Flag(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE)
    score = models.IntegerField()
    reviewed_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.keyword} - {self.content_item}"