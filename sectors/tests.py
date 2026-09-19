from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Sector


class SectorSaveAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.save_url = reverse("sector-save")

    def test_post_save_sector_full_payload(self):
        payload = {
            "name": "Healthcare & Wellness",
            "icon": "HeartPulse",
            "description": "Healthcare design guidelines and palette",
            "is_active": True,
            "characteristics": [
                {"name": "Clean", "display_order": 1},
                {"name": "Trustworthy", "display_order": 2}
            ],
            "personality_profiles": [
                {"name": "Empathy", "score": 90, "display_order": 1}
            ],
            "color_palette": {
                "primary": "#00A896",
                "secondary": "#028090",
                "accent": "#F0F3F4"
            },
            "imagery_guidelines": [
                {"title": "Medical staff", "guideline_type": "recommended", "display_order": 1}
            ],
            "layout_guideline": {
                "grid_system": "12 Column",
                "max_content_width": "1200px",
                "spacing_system": "8px base",
                "border_radius": "8px",
                "description": "Clean grid layout"
            },
            "typography_guideline": {
                "primary_font": "Inter",
                "secondary_font": "Roboto",
                "heading_weight": "600",
                "body_weight": "400",
                "heading_scale": "1.25",
                "line_height": "1.5",
                "description": "Accessible typography"
            },
            "shape_guideline": {
                "style": "Rounded",
                "border_radius": "8px",
                "border_style": "Solid",
                "shadow_style": "Soft Drop Shadow",
                "description": "Soft rounded elements"
            },
            "component_guidelines": [
                {
                    "component_name": "Primary Button",
                    "description": "Main call to action button",
                    "usage_guideline": "Use primary teal color",
                    "do_use": "High contrast white text",
                    "avoid": "Dark text on teal",
                    "display_order": 1
                }
            ],
            "sample_uis": [
                {
                    "title": "Patient Portal",
                    "description": "Main portal dashboard",
                    "image_url": "https://example.com/portal.png",
                    "display_order": 1,
                    "is_active": True
                }
            ],
            "accessibility_guidelines": [
                {
                    "title": "Contrast ratio",
                    "description": "At least 4.5:1 ratio for standard text",
                    "standard": "WCAG 2.1 AA",
                    "priority": "High",
                    "display_order": 1
                }
            ]
        }

        response = self.client.post(self.save_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "Healthcare & Wellness")
        self.assertEqual(response.data["data"]["slug"], "healthcare-wellness")
        self.assertEqual(len(response.data["data"]["characteristics"]), 2)
        self.assertEqual(response.data["data"]["color_palette"]["primary"], "#00A896")

    def test_post_update_existing_sector(self):
        sector = Sector.objects.create(
            name="Finance",
            slug="finance",
            description="Old description"
        )
        update_url = reverse("sector-save-detail", kwargs={"pk": sector.id})
        payload = {
            "name": "Finance & Banking",
            "description": "Updated financial guidelines"
        }

        response = self.client.post(update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "Finance & Banking")
        self.assertEqual(response.data["data"]["description"], "Updated financial guidelines")

    def test_get_sectors(self):
        Sector.objects.create(name="Education", slug="education")
        response = self.client.get(self.save_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertGreaterEqual(response.data["count"], 1)

    def test_delete_sector(self):
        sector = Sector.objects.create(name="Tech", slug="tech")
        delete_url = reverse("sector-save-detail", kwargs={"pk": sector.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Sector.objects.filter(id=sector.id).exists())

    def test_post_save_sector_with_temp_client_id(self):
        # Frontend form state may include temp client ID like 122 for new sectors
        payload = {
            "id": 122,
            "name": "Automotive & Mobility",
            "description": "Design guide for auto industry"
        }
        response = self.client.post(self.save_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "Automotive & Mobility")
        self.assertNotEqual(response.data["data"]["id"], 122) # Should assign new DB ID

