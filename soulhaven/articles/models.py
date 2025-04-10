from django.db import models


class Article(models.Model):
    """
    Represents a content article published on the site, typically by an admin.

    Fields:
    - title_header: The main headline shown on the homepage.
    - paragraph1: First section of the article body.
    - header2: Title for the second section.
    - paragraph2: Content for the second section.
    - header3: Title for the third section.
    - paragraph3: Content for the third section.
    - themes: A comma-separated string of theme tags (e.g., "mental health, self-care").
    - footer_note: Optional concluding note shown at the end of the article.
    - published_date: Automatically set timestamp of when the article was created.

    Methods:
    - get_themes_list(): Returns a list of individual themes parsed from the themes field.
    - __str__(): Returns the title header for admin or debug display.
    """
    title_header = models.CharField(max_length=255)
    paragraph1 = models.TextField()
    
    header2 = models.CharField(max_length=255)
    paragraph2 = models.TextField()
    
    header3 = models.CharField(max_length=255)
    paragraph3 = models.TextField()

    themes = models.CharField(max_length=255, help_text="Comma-separated list of themes")
    
    footer_note = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def get_themes_list(self):
        """
        Splits the themes string into a list of trimmed theme values.

        Returns:
            List[str]: Clean list of individual themes.
        """

        return [theme.strip() for theme in self.themes.split(',') if theme.strip()]

    def __str__(self):
        return self.title_header