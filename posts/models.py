from django.db import models


from users.models import User


# Post main model
class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    rates = models.ManyToManyField('PostRates', blank=True, related_name='post_rates')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post: "{self.title}" by {self.user}'


# Post rates
class PostRates(models.Model):
    RATES_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    giver = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATES_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Post rates'
        verbose_name_plural = 'Posts rates'

    def __str__(self):
        return f'Post {self.post.id} rates'
