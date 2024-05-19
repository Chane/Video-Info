import logging
import sys
import argparse
import os

from config import VIDEOFOLDER
from videoprops import get_video_properties

class VideoInfo:
    def __init__(self):
        parser = argparse.ArgumentParser();
        parser.add_argument(
            '-d', '--debug',
            help = "Log debug information",
            action = "store_const", dest = "loglevel", const = logging.DEBUG,
            default = logging.WARNING
        )

        parser.add_argument(
            '-v', '--verbose',
            help = "Log verbose information",
            action = "store_const", dest = "loglevel", const = logging.INFO
        )

        args = parser.parse_args();

        logging.basicConfig(stream = sys.stdout, level = args.loglevel)
        self.logger = logging.getLogger(__name__)

    def writeMessage(self, message):
        self.logger.log(logging.INFO, message)

    def writeDebug(self, message):
        self.logger.log(logging.DEBUG, message)

    def run(self):
        self.writeMessage(VIDEOFOLDER)

        info = []
        for root, dirs, files in os.walk(VIDEOFOLDER):
            for file in files:
                file_path = VIDEOFOLDER + '/' + file
                props = get_video_properties(file_path)

                file_stats = os.stat(file_path)
                size = file_stats.st_size

                file_size = round((size / 1024) / 1014, 2)

                clean_file = file.replace(',','')

                width = props['width']
                height = props['height']

                #if width == 3840 and height == 2160:
                detail = f'''{clean_file},{width},{height},{props['codec_name']},{file_size}'''
                
                self.writeDebug(detail)
                info.append(detail)

                    #os.system(f'ffmpeg -i "{file_path}" -n -vf scale=-1:1080 "{os.path.dirname(os.path.abspath(__file__))}/output/{file}"')
        
        with open (os.path.dirname(os.path.abspath(__file__)) + '/info.csv', 'w') as f:
            for line in info:
                f.write(f"{line}\n")