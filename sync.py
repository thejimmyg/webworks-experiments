import sys
import os
import http.client
import xml.etree.ElementTree

def debug(msg):
    pass#print('[DEBUG] %s'%(msg,))

def info(msg):
    print('[INFO] %s'%(msg,))

class SDCard:
    def __init__(self):
        self.conn = http.client.HTTPConnection('192.168.0.1')

    def listdir(self, path):
        if not path.startswith('/'):
            raise Exception("Paths must start with '/")
        self.conn.request(
            'POST',
            '/api/sdcard/sdfile',
            b"<?xml version	'1.0' encoding='UTF-8'?><request><CurrentPath>"+path.encode('utf8')+b"</CurrentPath></request>"
        )
        response = self.conn.getresponse()
        body = response.read()
        debug(body)
        files = []
        tree = xml.etree.ElementTree.fromstring(body)
        for file_elem in tree.find('FileList'):
            debug(xml.etree.ElementTree.tostring(file_elem))
            file_data = {
                'type': file_elem.find('Type').text,
                'size': file_elem.find('Size').text,
            } 
            if file_data['type'] == '0':
                file_data['name'] = file_elem.find('fileUrlOrFolderPath').text[len(path):]
            else:
                file_data['name'] = file_elem.find('fileUrlOrFolderPath').text[len('http://192.168.0.1/sdcard/')+len(path):]
            # XXX Why do we need this?
            if file_data['name'].startswith('/'):
                file_data['name'] = file_data['name'][1:]
            files.append(file_data)
        return files

    def fetch(self, folder, path):
        if path.startswith('/'):
            raise Exception("Paths must not start with '/")
        self.conn.request(
            'GET',
            '/sdcard/'+path,
        )
        response = self.conn.getresponse()
        with open(os.path.join(folder, path), 'wb') as fp:
            fp.write(response.read())

    def sync(self, folder, path):
        #print(folder, path)
        if path.startswith('/'):
            raise Exception('Path cannot start with /')
        for item in self.listdir('/'+path):
            #print('  '+item['name'])
            if item['type'] == '0':
                dir_path = os.path.join(folder, path, item['name'])
                if not os.path.exists(dir_path):
                    info('Making %r'%(dir_path))
                    os.mkdir(dir_path)
                if path:
                    #print('-'+path+'/'+item['name'])
                    self.sync(folder, path+'/'+item['name'])
                else:
                    #print('+'+item['name'])
                    self.sync(folder, item['name'])
            else:
                file_path = os.path.join(folder, path, item['name'])
                if (file_path.endswith('.JPG') or file_path.endswith('.MTS') or file_path.endswith('.MOV')) and not '.Trash-' in file_path:
                    if not os.path.exists(file_path) or (os.stat(file_path).st_size != int(item['size'])):
                        print('Getting %s'%(file_path))
                        self.fetch(folder, os.path.join(path, item['name']))

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("Usage: python3 sync.py FOLDER")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.exists(folder) or not os.path.isdir(folder):
        print("Error: No such directory %r"%(folder,))
        sys.exit(2)
    sd = SDCard()
    sd.sync(folder, '')
    #print(sd.listdir('/DCIM/106_PANA'))
    #print('\n'.join([str(file) for file in sd.listdir('/')]))
    #print('\n'.join([str(file) for file in sd.listdir('/DCIM/106_PANA')]))



