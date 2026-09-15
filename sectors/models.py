from django.db import models


class Sector(models.Model):
    """
    Main sector/design guide.
    Example: Government, Healthcare, Education, Tourism
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=120,
        unique=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# 1. SECTOR CHARACTERISTICS
# =========================================================

class SectorCharacteristic(models.Model):
    """
    Example:
    Trustworthy
    Professional
    Stable
    Accessible
    Institutional
    Transparent
    """

    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="characteristics"
    )

    name = models.CharField(
        max_length=100
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["display_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["sector", "name"],
                name="unique_sector_characteristic"
            )
        ]

    def __str__(self):
        return self.name


# =========================================================
# 2. PERSONALITY PROFILE
# =========================================================

class PersonalityProfile(models.Model):
    """
    Example:
    Trust        95%
    Professional 90%
    Serious      85%
    Modern       65%
    Friendly     55%
    Luxury       15%
    Playful      10%
    """

    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="personality_profiles"
    )

    name = models.CharField(
        max_length=100
    )

    score = models.PositiveSmallIntegerField(
        default=0
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["display_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["sector", "name"],
                name="unique_sector_personality"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.score}%"



# =========================================================
# 3. COLOR PALETTE
# =========================================================

class ColorPalette(models.Model):
    """
    Example:

    Primary   #123B63
    Secondary #1F5F95
    Accent    #C9972B
    """

    sector = models.OneToOneField(
        Sector,
        on_delete=models.CASCADE,
        related_name="color_palette"
    )

    primary = models.CharField(
        max_length=20
    )

    secondary = models.CharField(
        max_length=20
    )

    accent = models.CharField(
        max_length=20
    )

    class Meta:
        verbose_name = "Color Palette"
        verbose_name_plural = "Color Palettes"

    def __str__(self):
        return f"{self.sector.name} Color Palette"



# =========================================================
# 4. IMAGERY GUIDELINES
# =========================================================

class ImageryGuideline(models.Model):
    """
    Example:

    Recommended:
        Official buildings
        Citizens
        Maps
        Data visualizations
        Document icons
        Diverse people

    Avoid:
        Stock photo clichés
        Political imagery
        Overly decorative elements
        Complex illustrations
    """

    RECOMMENDED = "recommended"
    AVOID = "avoid"

    GUIDELINE_TYPE_CHOICES = [
        (RECOMMENDED, "Recommended"),
        (AVOID, "Avoid"),
    ]

    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="imagery_guidelines"
    )

    title = models.CharField(
        max_length=200
    )

    guideline_type = models.CharField(
        max_length=20,
        choices=GUIDELINE_TYPE_CHOICES
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["guideline_type", "display_order"]

    def __str__(self):
        return self.title



# =========================================================
# 5. LAYOUT GUIDELINE
# =========================================================

class LayoutGuideline(models.Model):
    """
    Stores layout/design rules for a sector.
    """

    sector = models.OneToOneField(
        Sector,
        on_delete=models.CASCADE,
        related_name="layout_guideline"
    )

    grid_system = models.CharField(
        max_length=200,
        blank=True
    )

    max_content_width = models.CharField(
        max_length=100,
        blank=True
    )

    spacing_system = models.CharField(
        max_length=200,
        blank=True
    )

    border_radius = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Layout Guideline"
        verbose_name_plural = "Layout Guidelines"

    def __str__(self):
        return f"{self.sector.name} Layout"



# =========================================================
# 6. TYPOGRAPHY GUIDELINE
# =========================================================

class TypographyGuideline(models.Model):
    sector = models.OneToOneField(
        Sector,
        on_delete=models.CASCADE,
        related_name="typography_guideline"
    )

    primary_font = models.CharField(
        max_length=100
    )

    secondary_font = models.CharField(
        max_length=100,
        blank=True
    )

    heading_weight = models.CharField(
        max_length=50,
        blank=True
    )

    body_weight = models.CharField(
        max_length=50,
        blank=True
    )

    heading_scale = models.CharField(
        max_length=100,
        blank=True
    )

    line_height = models.CharField(
        max_length=50,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Typography Guideline"
        verbose_name_plural = "Typography Guidelines"

    def __str__(self):
        return f"{self.sector.name} Typography"



# =========================================================
# 7. SHAPE GUIDELINE
# =========================================================

class ShapeGuideline(models.Model):
    sector = models.OneToOneField(
        Sector,
        on_delete=models.CASCADE,
        related_name="shape_guideline"
    )

    style = models.CharField(
        max_length=100,
        blank=True
    )

    border_radius = models.CharField(
        max_length=100,
        blank=True
    )

    border_style = models.CharField(
        max_length=100,
        blank=True
    )

    shadow_style = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Shape Guideline"
        verbose_name_plural = "Shape Guidelines"

    def __str__(self):
        return f"{self.sector.name} Shapes"



# =========================================================
# 8. COMPONENT GUIDELINE
# =========================================================

class ComponentGuideline(models.Model):
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="component_guidelines"
    )

    component_name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    usage_guideline = models.TextField(
        blank=True
    )

    do_use = models.TextField(
        blank=True
    )

    avoid = models.TextField(
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["display_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["sector", "component_name"],
                name="unique_sector_component"
            )
        ]

    def __str__(self):
        return self.component_name



# =========================================================
# 9. SAMPLE UI
# =========================================================

class SampleUI(models.Model):
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="sample_uis"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="sector_samples/",
        blank=True,
        null=True
    )

    image_url = models.URLField(
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title



# =========================================================
# 10. ACCESSIBILITY GUIDELINE
# =========================================================

class AccessibilityGuideline(models.Model):
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="accessibility_guidelines"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    standard = models.CharField(
        max_length=100,
        blank=True
    )

    priority = models.CharField(
        max_length=50,
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title