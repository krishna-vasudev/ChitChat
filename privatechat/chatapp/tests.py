from django.test import TestCase
from chatapp.models import Message

# Create your tests here.
class MessagemodelTest(TestCase):

    def setUp(self):
        self.testing_message=Message(sender="testsender",receiver="testreceiver",message="Testing Testing")
        self.testing_message.save()

    def tearDown(self):
        self.testing_message.delete()

    def test_read_Message(self):
        self.assertEqual(self.testing_message.sender,"testsender")
        self.assertEqual(self.testing_message.receiver,"testreceiver")
        self.assertEqual(self.testing_message.message,"Testing Testing")
        self.assertEqual(self.testing_message.file_status,False)

    def test_update_Message(self):
        self.testing_message.message="new Testing Testing"
        self.testing_message.save()
        self.assertEqual(self.testing_message.message,"new Testing Testing")


