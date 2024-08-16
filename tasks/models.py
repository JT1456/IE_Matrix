from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    EFFORT_CHOICES = [(i, str(i)) for i in range(1, 11)]
    IMPACT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    # Task Details
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    #Impact and Effort sliders
    impact = models.IntegerField(choices=IMPACT_CHOICES, default=1)
    effort = models.IntegerField(choices=EFFORT_CHOICES, default=1)

    PRIORITY_CHOICES = [('Q1', 'High Impact / Low Effort'),
                        ('Q2', 'High Impact / High Effort'),
                        ('Q3', 'Low Impact / High Effort'),
                        ('Q4', 'Low Impact / Low Effort')
    ]   

    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, editable=False, null=True)

    # Task Status
    completed = models.BooleanField(default=False)


    #User Relationship

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kargs):
        if self.impact >= 6 and self.effort <= 5:
            self.priority='Q1'
        
        elif self.impact >= 6 and self.effort > 5:
            self.priority='Q2'

        elif self.impact < 6 and self.effort <= 5:
            self.priority='Q3'
        
        else:
            self.priority = "Q4"
        
        super(Task, self).save(*args, **kargs)

    def __str__(self):
        return f"Task: {self.id}, Priority: {self.get_priority_display()}"

