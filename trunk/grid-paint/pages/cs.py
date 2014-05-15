# -*- coding: utf-8 -*-
'''
Created on 14.05.2014

@author: Vlad
'''

import os
import cloudstorage as gcs

import logging

from google.appengine.api import app_identity


my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


def get_bucket():
    bucket_name = os.environ.get('BUCKET_NAME',
                                 app_identity.get_default_gcs_bucket_name())
    bucket = '/' + bucket_name
    return bucket
    

def create_file(filename, file_content_type, file_content):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """

        
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(get_bucket()+filename,
                        'w',
                        content_type=file_content_type,
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write(file_content)
    gcs_file.close()


def read_file(filename):
    """Open file from cloud storage.
    
    Returns contents of the file object.
    """
    cs_file = gcs.open(get_bucket()+filename)
    
    logging.error("cs_file = "+get_bucket()+filename);
    result = cs_file.read();
    cs_file.close()
    return result

def delete_file(filename):
    try:
        gcs.delete(get_bucket()+filename)
    except gcs.NotFoundError:
        pass

