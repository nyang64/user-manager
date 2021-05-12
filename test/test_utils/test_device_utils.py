from utils import device_utils


class TestDeviceUtils:

    metrics_hex = "aa7a82d89ec58f265821ba0e170001040000200026dee608bf04e8e3065f6fe112c78aafa47ec5438a6783b979b67d9078f6f740f1e830d49d708eed4612b298008649b2"
    encryption_key = "41414241354345353534413734454144"

    def test_get_metrics_data(self):
        parsed_data = device_utils.get_metrics_data(
            self.metrics_hex, self.encryption_key
        )
        assert parsed_data is not None

    def test_parse_metrics(self):
        hex_string = "0100000042621141eaba85400000000000000000d8b0edce9c00000000000000"
        parsed_data = device_utils.parse_metrics(hex_string)
        assert parsed_data is not None
        assert parsed_data["buttonPresses"] == 1

    def test_decipher_ts(self):
        hex_ts = "7556fe3c91000000"
        ts = device_utils.decipher_ts(hex_ts)
        assert ts != ""
