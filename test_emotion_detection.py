import unittest
from unittest.mock import patch, Mock

from EmotionDetection.emotion_detection import emotion_detector


def make_response(emotions, status_code=200):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.text = (
        '{"emotionPredictions":[{"emotion":'
        + str(emotions).replace("'", '"')
        + "}]}"
    )
    return mock_response


class TestEmotionDetection(unittest.TestCase):

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, mock_post):
        mock_post.return_value = make_response({
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.90,
            "sadness": 0.04
        })

        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, mock_post):
        mock_post.return_value = make_response({
            "anger": 0.90,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.01,
            "sadness": 0.04
        })

        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, mock_post):
        mock_post.return_value = make_response({
            "anger": 0.02,
            "disgust": 0.01,
            "fear": 0.03,
            "joy": 0.04,
            "sadness": 0.90
        })

        result = emotion_detector("I am feeling very sad")
        self.assertEqual(result["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, mock_post):
        mock_post.return_value = make_response({
            "anger": 0.02,
            "disgust": 0.01,
            "fear": 0.90,
            "joy": 0.04,
            "sadness": 0.03
        })

        result = emotion_detector("I am afraid")
        self.assertEqual(result["dominant_emotion"], "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, mock_post):
        mock_post.return_value = make_response({
            "anger": 0.02,
            "disgust": 0.90,
            "fear": 0.03,
            "joy": 0.01,
            "sadness": 0.04
        })

        result = emotion_detector("This is disgusting")
        self.assertEqual(result["dominant_emotion"], "disgust")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = emotion_detector("")

        self.assertIsNone(result["anger"])
        self.assertIsNone(result["disgust"])
        self.assertIsNone(result["fear"])
        self.assertIsNone(result["joy"])
        self.assertIsNone(result["sadness"])
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
