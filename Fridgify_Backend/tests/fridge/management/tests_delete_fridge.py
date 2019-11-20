from django.test import TestCase
from Fridgify_Backend.views.fridge.management import delete_fridge
import json


class ManagementTestCasesDeleteFridge(TestCase):

    """Delete fridge test case"""
    def test_delete_fridge(self):
        response = json.loads(delete_fridge.entry_point("dummy").content)
        self.assertEqual(response["message"], "Delete fridge", "Delete fridge")
