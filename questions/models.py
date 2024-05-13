from django.db import models


class Question(models.Model):

    id_question = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=4096, unique=True)
    source = models.CharField(blank=True, default='', max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load_question(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text


class Answer(models.Model):
    id_answer = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name='answers',
        )
    text = models.CharField(max_length=4096)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load_answer(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text





