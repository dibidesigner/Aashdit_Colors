from rest_framework import serializers
from django.db import transaction
from .models import (
    Sector,
    SectorCharacteristic,
    ColorPalette,
    SampleUI,PersonalityProfile,ImageryGuideline,LayoutGuideline,TypographyGuideline
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


class SectorCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorCharacteristic
        fields = [
            "name",
            "display_order",
        ]


class ColorPaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPalette
        fields = [
            "primary",
            "secondary",
            "accent",
        ]

class ImageryGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageryGuideline
        fields = [
            "id",
            "title",
            "guideline_type",
            "display_order",
        ]     


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
            "line_height",
            "letter_spacing",
            "description",
        ]
        read_only_fields = ["id"]


class SectorSerializer(serializers.ModelSerializer):
    """
    Standard sector serializer used by SectorDetailView
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
            # Relationships
            "characteristics",
            "personality_profiles",
            "color_palette",
            "sample_uis",
            "layout_guideline",
            "typography_guideline",
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

    characteristics = SectorCharacteristicSerializer(
        many=True,
        required=False
    )

    personality_profiles = PersonalityProfileSerializer(
        many=True,
        required=False
    )

    color_palette = ColorPaletteSerializer(
        required=False
    )

    imagery_guidelines = ImageryGuidelineSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Sector

        fields = [
            "name",
            "slug",
            "icon",
            "description",
            "is_active",
            "characteristics",
            "personality_profiles",
            "color_palette",
            "imagery_guidelines",
        ]

    @transaction.atomic
    def create(self, validated_data):

        characteristics_data = validated_data.pop(
            "characteristics",
            []
        )

        personality_data = validated_data.pop(
            "personality_profiles",
            []
        )

        color_data = validated_data.pop(
            "color_palette",
            None
        )

        imagery_data = validated_data.pop(
            "imagery_guidelines",
            []
        )

        sector = Sector.objects.create(
            **validated_data
        )

        for item in characteristics_data:

            SectorCharacteristic.objects.create(
                sector=sector,
                **item
            )

        for item in personality_data:

            PersonalityProfile.objects.create(
                sector=sector,
                **item
            )

        if color_data:

            ColorPalette.objects.create(
                sector=sector,
                **color_data
            )

        for item in imagery_data:

            ImageryGuideline.objects.create(
                sector=sector,
                **item
            )

        return sector
