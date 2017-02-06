import boto
import gcs_oauth2_boto_plugin
import os
import shutil
import StringIO
import tempfile
import time
import sys
from boto.gs.connection import GSConnection;
GOOGLE_STORAGE = 'gs'

def listbucket(project_id):
    uri = boto.storage_uri('', GOOGLE_STORAGE)
    # If the default project is defined, call get_all_buckets() without arguments.
    header_values = {"x-goog-project-id": project_id}
    print '== bucket list =='
    for bucket in uri.get_all_buckets(headers=header_values):
        print bucket.name

def download_bucket(project_id, buckets):
    for bucket in buckets:
        print 'current bucket: ' + bucket
        if not os.path.exists(bucket):
            os.makedirs(bucket)

        uri = boto.storage_uri(bucket, GOOGLE_STORAGE)
        for obj in uri.get_bucket():
            print 'downloading: ' + bucket + '/' + obj.name
            src_uri = boto.storage_uri(
                bucket + '/' + obj.name, GOOGLE_STORAGE)
            # The unintuitively-named get_file() doesn't return the object
            # contents; instead, it actually writes the contents to
            # object_contents.
            with open(bucket + '/' + obj.name, "wb") as localfile:
                src_uri.get_key().get_file(localfile)

def cleanup30d(project_id):
    delta = 30 * 24 * 60 * 60 #30 days
    #delta = 5 * 60  # 5 minutes

    delete_buckets = []
    now = time.time();
    uri = boto.storage_uri('', GOOGLE_STORAGE)
    # If the default project is defined, call get_all_buckets() without arguments.
    header_values = {"x-goog-project-id": project_id}
    for bucket in uri.get_all_buckets(headers=header_values):
        temp = bucket.name.split('-')
        if(now - float(temp[1]) > delta):
            print 'target for deletion: %s' % bucket.name
            delete_buckets.append(bucket.name)
        else:
            print 'not target: %s' % bucket.name

    for bucket in delete_buckets:
        uri = boto.storage_uri(bucket, GOOGLE_STORAGE)
        for obj in uri.get_bucket():
            print 'Deleting object: %s...' % obj.name
            obj.delete()
        print 'Deleting bucket: %s...' % uri.bucket_name
        uri.delete_bucket()

def upload(project_id, files):
    now = time.time()
    PROJECT_BUCKET = 'project-%d' % now

    for name in (PROJECT_BUCKET,):
        # Instantiate a BucketStorageUri object.
        uri = boto.storage_uri(name, GOOGLE_STORAGE)
        # Try to create the bucket.
        try:
            # If the default project is defined,
            # you do not need the headers.
            # Just call: uri.create_bucket()
            header_values = {"x-goog-project-id": project_id}
            uri.create_bucket(headers=header_values)

            print 'Successfully created bucket "%s"' % name
        except boto.exception.StorageCreateError, e:
            print 'Failed to create bucket:', e

    # Upload these files to PROJECT_BUCKET.
    for filename in files:
        # with open(os.path.join(temp_dir, filename), 'r') as localfile:
        with open(filename, 'rb') as localfile:
            dst_uri = boto.storage_uri(
                PROJECT_BUCKET + '/' + filename, GOOGLE_STORAGE)
            # The key-related functions are a consequence of boto's
            # interoperability with Amazon S3 (which employs the
            # concept of a key mapping to localfile).
            dst_uri.new_key().set_contents_from_file(localfile)
        print 'Successfully created "%s/%s"' % (
            dst_uri.bucket_name, dst_uri.object_name)

if __name__ == '__main__':
    # Fallback logic. In https://console.cloud.google.com/
    # under Credentials, create a new client ID for an installed application.
    # Required only if you have not configured client ID/secret in
    # the .boto file or as environment variables.
    #CLIENT_ID = '109114778767971400640'
    #CLIENT_SECRET = 'your client secret'
    #gcs_oauth2_boto_plugin.SetFallbackClientIdAndSecret(CLIENT_ID, CLIENT_SECRET)

    narg = len(sys.argv)
    if narg == 3:
        if(sys.argv[1] == '-cleanup30d'):
            #usage: script.py -cleanup project_id
            cleanup30d(sys.argv[2])
        elif(sys.argv[1] == '-listbucket'):
            # usage: script.py -listbucket project_id
            listbucket(sys.argv[2])
    elif narg >= 4:
        if(sys.argv[1] == '-upload'):
            #usage: script.py -upload project_id file1 [file2 ... fileN]
            fnames = []
            for i in range(3,narg):
                fnames.append(sys.argv[i])
            upload(sys.argv[2], fnames)
        elif(sys.argv[1] == '-download-bucket'):
            # usage: script.py -download-bucket project_id bucket1 [bucket2 ... bucketN]
            buckets = []
            for i in range(3, narg):
                buckets.append(sys.argv[i])
            download_bucket(sys.argv[2], buckets)