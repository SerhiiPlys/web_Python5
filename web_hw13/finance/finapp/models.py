from django.db import models

# Create your models here.
class Record(models.Model):
    name = models.CharField('ФИО', max_length=100)
    email = models.CharField('Email', max_length=50)
    plan_plus = models.CharField('Плановые нормальные доходы', max_length=50)
    unplan_plus = models.CharField('Внелановые нормальные доходы', max_length=50)
    fart_plus = models.CharField('Случайные доходы', max_length=50)
    plan_minus = models.CharField('Плановые нормальные расходы', max_length=50)
    unplan_minus = models.CharField('Внелановые нормальные расходы', max_length=50)
    idiotic_minus = models.CharField('Идиотские расходы', max_length=50)
    date = models.DateTimeField('Дата записи')

    def __str__(self):
        return f'Касательно {self.name}  {self.email}'

    class Meta:
        verbose_name = 'Одна запись'
        verbose_name_plural = 'Записи'
