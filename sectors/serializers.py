from rest_framework import serializers
from django.db import transaction
from django.utils.text import slugify
from .models import (
    Sector,
    SectorCharacteristic,
    PersonalityProfile,
    ColorPalette,
    ImageryGuideline,
    LayoutGuideline,
    TypographyGuideline,
    ShapeGuideline,
    ComponentGuideline,
    SampleUI,
    AccessibilityGuideline,
)


class PersonalityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityProfile
        fields = [
            "id",
            "name",
            "score",
            "display_order",
        ]
        read_only_fields = ["id"]


class SectorCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorCharacteristic
        fields = [
            "id",
            "name",
            "display_order",
        ]
        read_only_fields = ["id"]


class ColorPaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPalette
        fields = [
            "id",
            "primary",
            "secondary",
            "accent",
        ]
        read_only_fields = ["id"]


class ImageryGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageryGuideline
        fields = [
            "id",
            "title",
            "guideline_type",
            "display_order",
        ]
        read_only_fields = ["id"]


class SampleUISerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleUI
        fields = [
            "id",
            "title",
            "description",
            "image",
            "image_url",
            "display_order",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        image = attrs.get("image")
        image_url = attrs.get("image_url")

        if not image and not image_url:
            raise serializers.ValidationError({
                "image": "Either image or image_url is required."
            })

        return attrs


class LayoutGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutGuideline
        fields = [
            "id",
            "grid_system",
            "max_content_width",
            "spacing_system",
            "border_radius",
            "description",
        ]
        read_only_fields = ["id"]


class TypographyGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypographyGuideline
        fields = [
            "id",
            "primary_font",
            "secondary_font",
            "heading_weight",
            "body_weight",
            "heading_scale",
            "line_height",
            "description",
        ]
        read_only_fields = ["id"]


class ShapeGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShapeGuideline
        fields = [
            "id",
            "style",
            "border_radius",
            "border_style",
            "shadow_style",
            "description",
        ]
        read_only_fields = ["id"]


class ComponentGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentGuideline
        fields = [
            "id",
            "component_name",
            "description",
            "usage_guideline",
            "do_use",
            "avoid",
            "display_order",
        ]
        read_only_fields = ["id"]


class AccessibilityGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessibilityGuideline
        fields = [
            "id",
            "title",
            "description",
            "standard",
            "priority",
            "display_order",
        ]
        read_only_fields = ["id"]


class SectorSerializer(serializers.ModelSerializer):
    """
    Standard sector serializer used for read responses
    """

    characteristics = SectorCharacteristicSerializer(
        many=True,
        read_only=True
    )

    personality_profiles = PersonalityProfileSerializer(
        many=True,
        read_only=True
    )

    color_palette = ColorPaletteSerializer(
        read_only=True
    )

    imagery_guidelines = ImageryGuidelineSerializer(
        many=True,
        read_only=True
    )

    sample_uis = SampleUISerializer(
        many=True,
        read_only=True
    )

    layout_guideline = LayoutGuidelineSerializer(
        read_only=True
    )

    typography_guideline = TypographyGuidelineSerializer(
        read_only=True
    )

    shape_guideline = ShapeGuidelineSerializer(
        read_only=True
    )

    component_guidelines = ComponentGuidelineSerializer(
        many=True,
        read_only=True
    )

    accessibility_guidelines = AccessibilityGuidelineSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Sector

        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "characteristics",
            "personality_profiles",
            "color_palette",
            "imagery_guidelines",
            "sample_uis",
            "layout_guideline",
            "typography_guideline",
            "shape_guideline",
            "component_guidelines",
            "accessibility_guidelines",
        ]


class PopularSectorSerializer(serializers.ModelSerializer):

    characteristics = SectorCharacteristicSerializer(
        many=True,
        read_only=True
    )

    color_palette = ColorPaletteSerializer(
        read_only=True
    )

    sample_ui_count = serializers.SerializerMethodField()

    class Meta:
        model = Sector

        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "description",
            "characteristics",
            "color_palette",
            "sample_ui_count",
        ]

    def get_sample_ui_count(self, obj):
        return obj.sample_uis.filter(
            is_active=True
        ).count()


class SectorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Sector data sent from React.
    Supports full nested creation and updates for all related models.
    Auto-generates slug if missing.
    """

    slug = serializers.SlugField(
        required=False,
        allow_blank=True
    )

    characteristics = SectorCharacteristicSerializer(
        many=True,
        required=False
    )

    personality_profiles = PersonalityProfileSerializer(
        many=True,
        required=False
    )

    color_palette = ColorPaletteSerializer(
        required=False,
        allow_null=True
    )

    imagery_guidelines = ImageryGuidelineSerializer(
        many=True,
        required=False
    )

    layout_guideline = LayoutGuidelineSerializer(
        required=False,
        allow_null=True
    )

    typography_guideline = TypographyGuidelineSerializer(
        required=False,
        allow_null=True
    )

    shape_guideline = ShapeGuidelineSerializer(
        required=False,
        allow_null=True
    )

    component_guidelines = ComponentGuidelineSerializer(
        many=True,
        required=False
    )

    sample_uis = SampleUISerializer(
        many=True,
        required=False
    )

    accessibility_guidelines = AccessibilityGuidelineSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Sector

        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "description",
            "is_active",
            "characteristics",
            "personality_profiles",
            "color_palette",
            "imagery_guidelines",
            "layout_guideline",
            "typography_guideline",
            "shape_guideline",
            "component_guidelines",
            "sample_uis",
            "accessibility_guidelines",
        ]

    def validate(self, attrs):
        name = attrs.get("name")
        slug = attrs.get("slug")

        if not slug and name:
            base_slug = slugify(name)
            generated_slug = base_slug
            count = 1
            instance_id = self.instance.id if self.instance else None

            while Sector.objects.filter(slug=generated_slug).exclude(id=instance_id).exists():
                generated_slug = f"{base_slug}-{count}"
                count += 1

            attrs["slug"] = generated_slug

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        characteristics_data = validated_data.pop("characteristics", [])
        personality_data = validated_data.pop("personality_profiles", [])
        color_data = validated_data.pop("color_palette", None)
        imagery_data = validated_data.pop("imagery_guidelines", [])
        layout_data = validated_data.pop("layout_guideline", None)
        typography_data = validated_data.pop("typography_guideline", None)
        shape_data = validated_data.pop("shape_guideline", None)
        component_data = validated_data.pop("component_guidelines", [])
        sample_ui_data = validated_data.pop("sample_uis", [])
        accessibility_data = validated_data.pop("accessibility_guidelines", [])

        sector = Sector.objects.create(**validated_data)

        self._save_nested_relations(
            sector=sector,
            characteristics_data=characteristics_data,
            personality_data=personality_data,
            color_data=color_data,
            imagery_data=imagery_data,
            layout_data=layout_data,
            typography_data=typography_data,
            shape_data=shape_data,
            component_data=component_data,
            sample_ui_data=sample_ui_data,
            accessibility_data=accessibility_data,
        )

        return sector

    @transaction.atomic
    def update(self, instance, validated_data):

        characteristics_data = validated_data.pop("characteristics", None)
        personality_data = validated_data.pop("personality_profiles", None)
        color_data = validated_data.pop("color_palette", None)
        imagery_data = validated_data.pop("imagery_guidelines", None)
        layout_data = validated_data.pop("layout_guideline", None)
        typography_data = validated_data.pop("typography_guideline", None)
        shape_data = validated_data.pop("shape_guideline", None)
        component_data = validated_data.pop("component_guidelines", None)
        sample_ui_data = validated_data.pop("sample_uis", None)
        accessibility_data = validated_data.pop("accessibility_guidelines", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if characteristics_data is not None:
            instance.characteristics.all().delete()
            for item in characteristics_data:
                SectorCharacteristic.objects.create(sector=instance, **item)

        if personality_data is not None:
            instance.personality_profiles.all().delete()
            for item in personality_data:
                PersonalityProfile.objects.create(sector=instance, **item)

        if color_data is not None:
            if hasattr(instance, "color_palette"):
                instance.color_palette.delete()
            if color_data:
                ColorPalette.objects.create(sector=instance, **color_data)

        if imagery_data is not None:
            instance.imagery_guidelines.all().delete()
            for item in imagery_data:
                ImageryGuideline.objects.create(sector=instance, **item)

        if layout_data is not None:
            if hasattr(instance, "layout_guideline"):
                instance.layout_guideline.delete()
            if layout_data:
                LayoutGuideline.objects.create(sector=instance, **layout_data)

        if typography_data is not None:
            if hasattr(instance, "typography_guideline"):
                instance.typography_guideline.delete()
            if typography_data:
                TypographyGuideline.objects.create(sector=instance, **typography_data)

        if shape_data is not None:
            if hasattr(instance, "shape_guideline"):
                instance.shape_guideline.delete()
            if shape_data:
                ShapeGuideline.objects.create(sector=instance, **shape_data)

        if component_data is not None:
            instance.component_guidelines.all().delete()
            for item in component_data:
                ComponentGuideline.objects.create(sector=instance, **item)

        if sample_ui_data is not None:
            instance.sample_uis.all().delete()
            for item in sample_ui_data:
                SampleUI.objects.create(sector=instance, **item)

        if accessibility_data is not None:
            instance.accessibility_guidelines.all().delete()
            for item in accessibility_data:
                AccessibilityGuideline.objects.create(sector=instance, **item)

        return instance

    def _save_nested_relations(
        self,
        sector,
        characteristics_data,
        personality_data,
        color_data,
        imagery_data,
        layout_data,
        typography_data,
        shape_data,
        component_data,
        sample_ui_data,
        accessibility_data,
    ):
        for item in characteristics_data:
            SectorCharacteristic.objects.create(sector=sector, **item)

        for item in personality_data:
            PersonalityProfile.objects.create(sector=sector, **item)

        if color_data:
            ColorPalette.objects.create(sector=sector, **color_data)

        for item in imagery_data:
            ImageryGuideline.objects.create(sector=sector, **item)

        if layout_data:
            LayoutGuideline.objects.create(sector=sector, **layout_data)

        if typography_data:
            TypographyGuideline.objects.create(sector=sector, **typography_data)

        if shape_data:
            ShapeGuideline.objects.create(sector=sector, **shape_data)

        for item in component_data:
            ComponentGuideline.objects.create(sector=sector, **item)

        for item in sample_ui_data:
            SampleUI.objects.create(sector=sector, **item)

        for item in accessibility_data:
            AccessibilityGuideline.objects.create(sector=sector, **item)
