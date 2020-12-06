import random
import math

f = open("games/example/map1.tmx", 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?> \n')
f.write('<map version="1.0" orientation="orthogonal" width="21" height="21" tilewidth="64" tileheight="64"> \n')
f.write('<properties> \n')
f.write('<property name="name" value="Blackrock"/> \n')
f.write('</properties> \n')
f.write('<tileset firstgid="1" name="graphics" tilewidth="64" tileheight="64"> \n')
f.write('<image source="graphics2x-basic.png" width="640" height="1344"/> \n')
f.write('</tileset> \n')
f.write('<tileset firstgid="211" name="walls" tilewidth="64" tileheight="64"> \n')
f.write('<image source="graphics2x-walls.png" width="128" height="1024"/> \n')
f.write('</tileset> \n')
f.write('<layer name="Tile Layer 1" width="21" height="21"> \n')
f.write('<data> \n')

for i in range (1,442): 
    # if((math.abs(i-1)/21)%2==1):
    #     data = '<tile gid="211"/> \n'
    # else if((((i-1)/21)%2==0 and i%2==1)):
    #     data = '<tile gid="211"/> \n'
    # else:
    #     data = '<tile gid="57"/> \n'
    data = '<tile gid="57"/>\n'
    if(i%21 == 0 or i%21 == 1 or i<=21 or i>=422):
        data= '<tile gid="211"/>\n'
    f.write(data)
f.write('</data> \n')
f.write('</layer> \n')
f.write('</map> \n')

f.close()