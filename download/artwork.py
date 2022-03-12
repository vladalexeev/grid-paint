import os
import json
import urllib2

def download(folder):
    for file_name in os.listdir(folder):
        if file_name.endswith('.json'):
            print('Process file', file_name)
            with open(os.path.join(folder, file_name)) as f:
                artwork_list = json.load(f)
            print('File opened')
            for artwork in artwork_list:
                print('Load images for %s' % artwork['id'])
                response_json = urllib2.urlopen('https://grid-paint.com/' + artwork['json_file_name'])
                json_content = response_json.read()
                json_file_name = os.path.join(folder + artwork['json_file_name'])
                if not os.path.exists(os.path.dirname(json_file_name)):
                    os.makedirs(os.path.dirname(json_file_name))
                with open(json_file_name, 'w') as f:
                    f.write(json_content)

                response_image = urllib2.urlopen('https://grid-paint.com/' + artwork['full_image_file_name'])
                image_content = response_image.read()
                image_file_name = os.path.join(folder + artwork['full_image_file_name'])
                if not os.path.exists(os.path.dirname(image_file_name)):
                    os.makedirs(os.path.dirname(image_file_name))
                with open(image_file_name, 'wb') as f:
                    f.write(image_content)

                response_small_image = urllib2.urlopen('https://grid-paint.com/' + artwork['small_image_file_name'])
                small_image_content = response_small_image.read()
                small_image_file_name = os.path.join(folder + artwork['small_image_file_name'])
                if not os.path.exists(os.path.dirname(small_image_file_name)):
                    os.makedirs(os.path.dirname(small_image_file_name))
                with open(small_image_file_name, 'wb') as f:
                    f.write(small_image_content)

    print('finished')
