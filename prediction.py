#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Google Prediction API

Authors: Joe Gregorio, Marc Cohen
Edited by Yong Phelan Nkfum

Command-line application that trains on your input data. This sample does
the same thing as the Hello Prediction! example. You might want to run
the setup.sh script to load the sample data to Google Storage.

Usage:
  $ python prediction.py "bucket/object" "model_id" "project_id"

You can also get help on all the command-line flags the program understands
by running:

  $ python prediction.py --help

To get detailed log output run:

  $ python prediction.py --logging_level=DEBUG
"""
from __future__ import print_function

__author__ = ('jcgregorio@google.com (Joe Gregorio), '
              'marccohen@google.com (Marc Cohen)')

import argparse
import os
import pprint
import sys
import time

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('object_name',
    help='Full Google Storage path of csv data (ex bucket/object)')
argparser.add_argument('model_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('project_id',
    help='Model Id of your choosing to name trained model')


def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print('\n' + header_line)
  print(line)
  print(header_line)


def main(argv):
  # If you previously ran this app with an earlier version of the API
  # or if you change the list of scopes below, revoke your app's permission
  # here: https://accounts.google.com/IssuedAuthSubTokens
  # Then re-run the app to re-authorize it.
  service, flags = sample_tools.init(
      argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
      scope=(
          'https://www.googleapis.com/auth/prediction',
          'https://www.googleapis.com/auth/devstorage.read_only',
	  'https://www.googleapis.com/auth/devstorage.full_control',
	  'https://www.googleapis.com/auth/devstorage.read_write'))

  #open file handlers
  fh1 = open('test.csv','r')
  fh2 = open('predictions.csv', 'w+')

  contents = fh1.readlines()
  numoflines = len(contents)-1 #header not considered during predictions

  header = contents[0]
  header = 'predicted_outcome,'+header
  fh2.write(header) #write header to new file with predicted_outcome column

  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()

    # Make some predictions using trained model.
    print_header('Making some predictions')

    counter = 1 #first line is the header, start processing from the second line.
    while counter < numoflines:
  	  columns = contents[counter].split(',')
	  bidder_id = columns[1]
	  payment_account = columns[2]
	  address = columns[3].strip() #strip carriage return

	  #predict outcome using bidder_id, payment_account and address
          body = {'input': {'csvInstance': [bidder_id,payment_account,address]}}
          result = papi.predict(body=body, id=flags.model_id, project=flags.project_id).execute()

          print('Prediction results for "%s","%s","%s"...' % (bidder_id,payment_account,address))
	  outcome = result.get(u'outputLabel')
	  pprint.pprint(outcome)
	  fh2.write(outcome+','+contents[counter])
	  
	  counter = counter+1

    fh1.close()
    fh2.close()

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize.')

if __name__ == '__main__':
  main(sys.argv)
