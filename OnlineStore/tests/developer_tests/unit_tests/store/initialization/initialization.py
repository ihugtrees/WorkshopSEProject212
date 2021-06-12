from unittest import TestCase

from OnlineStore.src.presentation_layer.utils import initialize_system


class TestInitFiles(TestCase):
    def test_valid_initialization(self):
        self.assertTrue(initialize_system(init_file="init.json",config_file="config.json"))

    def test_invalid_initialization1(self):
        self.assertFalse(initialize_system(init_file="broken_init.json",config_file="config.json"))

    def test_invalid_initialization2(self):
        self.assertFalse(initialize_system(init_file="init.json",config_file="broken_config.json"))

    def test_invalid_initialization3(self):
        self.assertFalse(initialize_system(init_file="broken_init.json",config_file="config.json"))
