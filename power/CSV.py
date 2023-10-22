# -*- coding: utf-8 -*-
###############################################################################
# CSV.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
Library for a csv class used by the power meter programs.
"""


import csv
from datetime import datetime
import os


###############################################################################
# CSV #########################################################################
class CSV (object):
    def __init__ (self, fn_prefix, fields):
        self.filename_prefix = fn_prefix
        self.fields = fields

        self.fieldnames = ["Timestamp"] + self.fields
        self.today = 0
        self.csv_directory = "csv/"

        if not os.path.isdir(self.csv_directory):
            os.makedirs(self.csv_directory)

        self.new_file()

    def new_file (self):
        if self.today != datetime.now().day:   # new day? --> start with new file
            self.today = datetime.now().day
            self.filename = f"{self.csv_directory}/{self.filename_prefix}_{datetime.now().strftime('%Y%m%d')}.csv"

            if not os.path.isfile(self.filename):
                with open(self.filename, 'w', newline='') as file:
                     writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                     writer.writeheader()

    @staticmethod
    def get_item_from_rrd (rrd_template, rrd_data, item):
        return { item: rrd_data.split(':')[rrd_template.split(':').index(item)+1] }

    def write (self, rrd_template, rrd_data):
        self.new_file()
        csv_data = { "Timestamp": datetime.now().strftime("%Y%m%d %H:%M:%S") }
        for field in self.fields:
            csv_data.update(self.get_item_from_rrd(rrd_template, rrd_data, field))

        with open(self.filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(csv_data)

# eof #

