from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CV, CoverLetter


class CareerProTests(TestCase):
    def setUp(self):
        """Set up a test environment before every test function runs."""
        # Create a test user
        self.user = User.objects.create_user(
            username='tester',
            password='password123'
        )

        # Create a second user to test security/privacy
        self.other_user = User.objects.create_user(
            username='hacker',
            password='password123'
        )

        # Create a CV for the main tester
        self.cv = CV.objects.create(
            user=self.user,
            title="Software Engineer CV",
            education="Degree",
            experience="3 Years",
            skills="Django, Python"
        )

    # --- 1. CRUD TESTING ---

    def test_dashboard_access_and_read(self):
        """Test if a logged-in user can see their CV on the dashboard."""
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software Engineer CV")

    def test_cv_update(self):
        """Test if a user can edit an existing CV (The 'U' in CRUD)."""
        self.client.login(username='tester', password='password123')
        new_title = "Senior Developer CV"
        response = self.client.post(reverse('cv_update', args=[self.cv.pk]), {
            'title': new_title,
            'education': self.cv.education,
            'experience': self.cv.experience,
            'skills': self.cv.skills
        })
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.title, new_title)
        self.assertRedirects(response, reverse('dashboard'))

    def test_cv_delete(self):
        """Test if a user can remove a CV (The 'D' in CRUD)."""
        self.client.login(username='tester', password='password123')
        response = self.client.post(reverse('cv_delete', args=[self.cv.pk]))
        self.assertEqual(CV.objects.count(), 0)
        self.assertRedirects(response, reverse('dashboard'))

    # --- 2. SECURITY & AUTH TESTING ---

    def test_privacy_isolation(self):
        """Security: Ensure User A cannot see or edit User B's data."""
        # Log in as the 'hacker' user
        self.client.login(username='hacker', password='password123')

        # Try to view the dashboard (should not see the tester's CV)
        response = self.client.get(reverse('dashboard'))
        self.assertNotContains(response, "Software Engineer CV")

        # Try to delete the tester's CV directly via URL
        # (Should return 404 Not Found)
        response = self.client.post(reverse('cv_delete', args=[self.cv.pk]))
        self.assertEqual(response.status_code, 404)

    # --- 3. AI LOGIC TESTING ---

    def test_cover_letter_storage(self):
        """
        Test if a letter is successfully saved to the database (Persistence).
        """
        CoverLetter.objects.create(
            user=self.user,
            cv=self.cv,
            job_title="Python Dev",
            company_name="Google",
            generated_content="This is a test AI letter."
        )
        self.assertEqual(CoverLetter.objects.count(), 1)
