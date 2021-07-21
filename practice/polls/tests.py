from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_width_future_question(self):
        time=timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),True)

# Create your tests here.
