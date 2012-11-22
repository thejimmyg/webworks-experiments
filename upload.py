#!/usr/bin/env python3

import http.client 
import mimetypes
import sys
import os

# Get the auth header by sniffing the HTTP headers using a tool like Firefox's LiceHTTPHeaders whilst you sign in.
AUTH=b''

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = b''
    for i, x in enumerate(L):
        if isinstance(x, bytes):
            body += x
        else:
            body += x.encode('ascii')
        if i >= 0 and i < len(L)-1:
            body += b'\r\n'
     
    #body = CRLF.join([isinstance(x, str) and x.encode('utf8') or x for x in L])
    content_type = b'multipart/form-data; boundary=' + BOUNDARY.encode('ascii')
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def upload(filenames, directory=None):
    if not len(filenames) > 1:
        raise Exception('No filenames specifeid')
    fields = []
    if directory:
        fields = [('directory', directory)]
    for filename in filenames:
        content_type, body = encode_multipart_formdata(fields, [('userfile', filename, open(filename, 'rb').read())])
        h = http.client.HTTPSConnection('indonesia.jimmyg.org')
        print("Uploading %r ..."%(filename))
        #print(body)
        h.request(
            'POST',
            '/upload',
            body,
            {b'Authorization': b'Basic '+AUTH, b'Content-Type': content_type},
        )
        #print("done.")
        #print("The resposne is:")
        #a = h.getresponse()
        #print(a)
        #print(a.read())

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3.2 upload.py DIRECTORY FILE1 FILE2 etc")
        sys.exit(1)
    for filename in sys.argv[2:]:
        if not os.path.exists(filename):
            print("No such file %r"%(filename,))
            sys.exit(1)
    directory = sys.argv[1].strip()
    if not directory:
        directory = None
    upload(sys.argv[2:], directory)

