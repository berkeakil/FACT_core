#!/usr/bin/python3
'''
    Firmware Analysis and Comparison Tool (FACT)
    Copyright (C) 2015-2018  Fraunhofer FKIE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import sys
from typing import Iterable

from helperFunctions.program_setup import program_setup
from helperFunctions.web_interface import ConnectTo
from storage.db_interface_backend import BackEndDbInterface

PROGRAM_NAME = 'FACT Database Migration Helper'
PROGRAM_DESCRIPTION = 'Migrate FACT\'s Database from an old version'


def main():
    _, config = program_setup(PROGRAM_NAME, PROGRAM_DESCRIPTION, command_line_options=sys.argv)

    logging.info('Trying to migrate MongoDB')
    with ConnectTo(BackEndDbInterface, config) as db_service:  # type: BackEndDbInterface
        firmwares = db_service.firmwares.find()  # type: Iterable[dict]
        for firmware in firmwares:
            firmware_object = db_service._convert_to_firmware(firmware)
            db_service.add_firmware(firmware_object)

    return 0


if __name__ == '__main__':
    sys.exit(main())