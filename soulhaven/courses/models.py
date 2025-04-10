from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Represents a learning course offered in the system.

    Fields:
    - title: The name of the course.
    - description: A detailed overview of the course content.

    Methods:
    - __str__(): Returns the course title for admin display or debugging.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class CoursePart(models.TextChoices):
    """
    Enum-like structure for identifying parts of a course.

    Choices:
    - THEORY: Theoretical content.
    - PRACTICE: Practical exercises.
    - VIDEO: Video-based learning materials.
    - TEST: Final assessment for the course.
    """
    THEORY = 'theory', 'Theoretical Part'
    PRACTICE = 'practice', 'Practical Part'
    VIDEO = 'video', 'Video Lessons'
    TEST = 'test', 'Test'


class CourseProgress(models.Model):
    """
    Tracks a user's progress through individual parts of a course.

    Fields:
    - user: The user who is progressing through the course.
    - course: The course being taken.
    - part: The specific part of the course (theory, practice, video, test).
    - completed_at: Timestamp when the part was completed.
    - score: Optional test score (only used for the 'test' part).

    Meta:
    - unique_together: Ensures one progress record per user/course/part combination.

    Methods:
    - __str__(): Returns a string like "username - course - part" for easy display.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    part = models.CharField(max_length=20, choices=CoursePart.choices)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True) 

    class Meta:
        unique_together = ('user', 'course', 'part')

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.get_part_display()}"
