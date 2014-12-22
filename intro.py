# coding=utf-8


class IntroInfo:
    def __init__(self, name, timestamp, start, end):
        self.name = name
        self.timestamp = timestamp
        self.start = start
        self.end = end

    def __str__(self):
        return self.name + ":" + repr(self.timestamp) + ":" + repr(self.start)+ ":" + repr(self.end)

from mpris2.player import Player
from mpris2.interfaces import Interfaces
from mpris2.metada_map import Metadata_Map
from mpris2.playback_status import PLAYING

from time import sleep
import json
import zlib
import os

uri = Interfaces.MEDIA_PLAYER + '.' + "CMPlayer"
mp2 = Player(dbus_interface_info={'dbus_uri': uri})

f = open("/home/max/projects/c/Intro/analyse-gtk/test.bin")

strings = zlib.decompress(f.read()).split("\n")

infos = dict()
print "Reloading AK-47! Please wait patiently... "
for (string) in strings:
    if not string:
        continue

    json_data = json.loads(string)

    name = os.path.basename(json_data['name'])
    info = IntroInfo(name, json_data['timestamp'], json_data['start'], json_data['end'])

    infos[name] = info
    print info

print "Done."

while True:

    if mp2.PlaybackStatus != PLAYING:
        continue

    currentTitle = os.path.basename(mp2.Metadata[Metadata_Map.URL])
    try:
        currentInfo = infos[currentTitle]
        trackID = mp2.Metadata[Metadata_Map.TRACKID]
        position = long(mp2.Position)

        print "Playing:\t" + currentInfo.__str__()
        print "Timestamp:\t" + repr(position) + "μs"

        if position > currentInfo.timestamp + currentInfo.start:
            end = currentInfo.timestamp + currentInfo.end

            if position < end:
                mp2.SetPosition(mp2.Metadata[Metadata_Map.TRACKID], end)
    except KeyError:
        pass

    sleep(0.5)


    # Season 2: 2:25 -> 2:46 -> 3:24
    # Start: -21 End: +48