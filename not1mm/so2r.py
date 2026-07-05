#!/usr/bin/env python3
"""
not1mm Contest logger
Email: michael.bridak@gmail.com
GPL V3
Class: RateWindow
Purpose: not sure yet
"""

import logging
import os
from json import loads
from json.decoder import JSONDecodeError

from PyQt6 import uic
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QDockWidget

import not1mm.fsutils as fsutils

logger = logging.getLogger(__name__)


class SO2RWindow(QDockWidget):
    """The SO2R window. Shows which radio is currently transmitting or receiving, hopefully not confusing the operator even more."""

    message = pyqtSignal(dict)
    pref = {}
    so2rwindow_closed = pyqtSignal()

    def __init__(self, action):
        super().__init__()
        self.action = action
        self.active = False
        self.load_pref()
        uic.loadUi(fsutils.APP_DATA_PATH / "so2r.ui", self)

    def msg_from_main(self, packet):
        """"""

        if packet.get("cmd", "") in ("CONTACTCHANGED", "UPDATELOG", "DELETE"):
            ...

    def setActive(self, mode: bool):
        self.active = bool(mode)

    def load_pref(self) -> None:
        """
        Load preference file to get current db filename and sets the initial darkmode state.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            if os.path.exists(fsutils.CONFIG_FILE):
                with open(
                    fsutils.CONFIG_FILE, "rt", encoding="utf-8"
                ) as file_descriptor:
                    self.pref = loads(file_descriptor.read())
                    logger.info(f"loaded config file from {fsutils.CONFIG_FILE}")
            else:
                self.pref["current_database"] = "ham.db"

        except (IOError, JSONDecodeError) as exception:
            logger.critical("Error: %s", exception)

    def closeEvent(self, event) -> None:
        self.action.setChecked(False)
        self.so2rwindow_closed.emit()
        event.accept()
