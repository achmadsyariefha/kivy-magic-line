# coding=utf-8

import time
from telenium.tests import TeleniumTestCase


class LinesTestCase(TeleniumTestCase):
    cmd_entrypoint = [u'main.py']

    def test_ui_test(self):
        self.assertExists('//RootScreen', timeout=30)
        self.assertExists('//StartScreen[0]', timeout=30)
        self.assertExists('//MDLabel[0]', timeout=30)
        self.cli.wait_click('//MDFillRoundFlatButton[@text="Start"]', timeout=30)
        self.assertExists('//GameScreen[0]', timeout=30)
        self.cli.wait_click('//MDActionTopAppBarButton[0]', timeout=30)
        self.assertExists('//MDDialog', timeout=30)
        self.cli.wait_click('//MDFlatButton[@text="YES"]', timeout=30)
        self.cli.wait_click('//MDFillRoundFlatButton[@text="Settings"]', timeout=30)
        self.assertExists('//SettingsScreen[0]', timeout=30)
        self.cli.wait_click('//Check[1]', timeout=30)
        self.cli.wait_click('//Check[2]', timeout=30)
        self.cli.wait_click('//Check[0]', timeout=30)
        self.cli.wait_click('//MDActionTopAppBarButton[0]', timeout=30)
        self.cli.wait_click('//MDFillRoundFlatButton[@text="Help"]', timeout=30)
        self.assertExists('//HelpScreen[0]', timeout=30)
        self.cli.wait_click('//MDActionTopAppBarButton[0]', timeout=30)
        self.cli.wait_click('//MDFillRoundFlatButton[@text="Exit"]', timeout=30)
        self.assertExists('//MDDialog', timeout=30)
        self.cli.wait_click('//MDFlatButton[@text="NO"]', timeout=30)

    def test_game_test(self):
        self.cli.wait_click('//MDFillRoundFlatButton[@text="Start"]', timeout=5)
        self.assertNotExists('//StartScreen', timeout=5)
        self.assertExists('//GameScreen', timeout=5)
        self.assertExists('//MDLabel', timeout=5)
        self.assertExists('//GridLayout', timeout=5)
        self.cli.wait_click('//Button[00]', timeout=5)
        self.cli.wait_click('//Button[01]', timeout=5)
        self.cli.wait_click('//Button[09]', timeout=5)
        self.cli.wait_click('//Button[19]', timeout=5)
        self.cli.wait_click('//Button[99]', timeout=5)
        self.cli.wait_click('//Button[98]', timeout=5)
        self.cli.wait_click('//Button[90]', timeout=5)
        self.cli.wait_click('//Button[80]', timeout=5)
        self.cli.wait_click('//MDActionTopAppBarButton[0]', timeout=30)
        self.cli.wait_click('//MDFlatButton[@text="YES"]', timeout=30)
        self.assertNotExists('//GameScreen', timeout=5)
