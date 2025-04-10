from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course, CourseProgress, CoursePart
from django.contrib.auth.decorators import login_required
from achievements.utils import award_achievement
from stars.models import StarAction, StarHistory
from challenges.logic import check_course_challenges
from stars.utils import award_stars
import json


@login_required
def get_course_progress(request, course_id):
    """
    Returns the progress status of a user for a specific course.

    Parameters:
    - course_id: ID of the course to check.

    Logic:
    - Retrieves all completed parts for the course by the current user.
    - Determines if the 'test' part can be accessed by checking if
      'theory', 'practice', and 'video' parts are completed.

    Returns:
    - JSON response containing:
        - completed_parts: list of completed course parts
        - can_access_test: boolean flag if user can access the test part
    """
    course = get_object_or_404(Course, id=course_id)
    progress = CourseProgress.objects.filter(user=request.user, course=course)

    completed_parts = [entry.part for entry in progress]
    can_access_test = all(part in completed_parts for part in ['theory', 'practice', 'video'])

    return JsonResponse({
        'completed_parts': completed_parts,
        'can_access_test': can_access_test,
    })


@csrf_exempt
@login_required
def mark_course_part_complete(request):
    """
    Marks a course part as completed for the current user.

    Triggered by:
    - POST request containing course_id, part, and optional score (for 'test').

    Logic:
    - If the part was not already completed, creates a new CourseProgress entry.
    - Awards 200 stars for first-time completion of any part.
    - If the part is 'test', stores the score and checks for:
        - Course challenge completion
        - Course-based achievements:
            - First Course Completed
            - Course Explorer (3 completed)

    Returns:
    - JSON response indicating:
        - status: 'ok'
        - updated: whether this part was newly completed
        - achievements: any newly unlocked achievements (for frontend display)
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        part = data.get('part')
        score = data.get('score')
        course = get_object_or_404(Course, id=course_id)

        progress, created = CourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
            part=part
        )

        unlocked = []

        if created:
            part_title = part.capitalize()
            action_name = f"Course Part Completion: {course.title} - {part_title}"
            award_stars(request.user, action_name, amount=200)

        if part == 'test' and created:
            progress.score = score
            progress.save()

            check_course_challenges(request.user, course)

            completed_courses = CourseProgress.objects.filter(
                user=request.user,
                part='test'
            ).values_list('course', flat=True).distinct().count()

            if completed_courses == 1:
                if award_achievement(
                    request.user,
                    name="First Course Completed",
                    description="You completed your first full course!",
                    image="achievements/first_course.png"
                ):
                    unlocked.append({
                        'name': "First Course Completed",
                        'description': "You completed your first full course!",
                        'image': "achievements/first_course.png"
                    })

            if completed_courses == 3:
                if award_achievement(
                    request.user,
                    name="Course Explorer",
                    description="You’ve completed 3 courses — great learning streak!",
                    image="achievements/three_courses.png"
                ):
                    unlocked.append({
                        'name': "Course Explorer",
                        'description': "You’ve completed 3 courses — great learning streak!",
                        'image': "achievements/three_courses.png"
                    })

        return JsonResponse({
            'status': 'ok',
            'updated': not created,
            'achievements': unlocked
        })