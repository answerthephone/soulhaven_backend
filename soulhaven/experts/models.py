from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

class Expert(models.Model):
    """
    Represents an expert (e.g. psychologist, therapist) registered on the SOULHAVEN platform.

    Fields:
    - name: Full name of the expert.
    - email: Unique contact email address.
    - platform_title: Title or designation shown on the platform (default is "Эксперт платформы 'SOULHAVEN'").
    - profile_image: Profile picture of the expert.
    
    - education: Educational background and qualifications.
    - specialization: Areas of expertise (e.g. anxiety, family therapy).
    - experience: Number of years of professional experience.
    
    - methods: Description of work methods or therapy approaches.
    - tools: List of tools or techniques used in practice (stored as an array of strings).

    - certificate_image: Optional image of professional certificate.
    - certificate_text: Optional textual description or credentials.
    
    - personal_message: Optional personal message or philosophy shown on the expert page.
    
    - slug: Unique slug used in URLs for SEO and routing (auto-generated from name).
    
    - available: Indicates whether the expert is currently available.
    - created_at: Timestamp when the expert was added to the system.

    Methods:
    - save(): Automatically generates a slug if not provided.
    - __str__(): Returns the expert's full name.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    platform_title = models.CharField(max_length=255, default='Эксперт платформы "SOULHAVEN"')
    profile_image = models.ImageField(upload_to='experts/profile_images/')
    
    education = models.TextField()
    specialization = models.TextField()
    experience = models.IntegerField() #in years
    
    methods = models.TextField(help_text="Описание методов работы")
    tools = ArrayField(
        models.CharField(max_length=255),
        help_text="Список инструментов работы",
        blank=True,
        default=list
    )

    certificate_image = models.ImageField(upload_to='experts/certificates/', blank=True, null=True)
    certificate_text = models.TextField(blank=True)
    
    personal_message = models.TextField(blank=True)
    
    slug = models.SlugField(unique=True, blank=True)
    
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
