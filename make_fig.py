#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import random
import glob
import math 



class Bubble():
    def __init__(self, Size):
        self.size = random.randint(30, 50)
        # [mm]
        self.volume = 4/3 * math.pi * (self.size/1000/2)**3
        self.buoyancy = self.volume * 9.8 * 1000
        # The bounyancy is the force.
        # 9.8 [m/s2]: gravity acceleration
        # 1000 [kg/m3]: density of water

        # center
        self.position = [random.randint(0, Size[0]), random.randint(Size[1]/2, Size[1])]
        self.velocity = 0
        self.axis = [self.position[0]-self.size/2, self.position[1]-self.size/2, self.position[0]+self.size/2, self.position[1]+self.size/2]
        self.appear = False
        self.Appear()

    def PosUpdate(self, dt):
        # dt : sampling time [ms]
        self.Appear()

        if self.appear:
            self.velocity = (-1) * self.buoyancy * dt/1000 + self.velocity
            self.position[1] = self.position[1] + self.velocity
            self.axis = [self.position[0]-self.size/2, self.position[1]-self.size/2, self.position[0]+self.size/2, self.position[1]+self.size/2]

    def PosModify(self):
        self.axis = [self.position[0]-self.size/2, self.position[1]-self.size/2, self.position[0]+self.size/2, self.position[1]+self.size/2]

    def Appear(self):
        if self.appear == False:
            if random.randint(0, 9) >= 8 :
                self.appear = True
    

def main():
    # Image.Draw
    # Mode, Size, Color

    # picture size
    Size = [500, 300]
    Sampling = 50 # [ms]

    B = []
    images = []

    BubbleNum = 30

    FONTPATH = '/Library/Fonts/Verdana.ttf'
    fnt = ImageFont.truetype(FONTPATH, 80)

    txt = Image.new("RGB", Size, (255,255,255))
    mask = Image.new("L", Size, 0)

    d = ImageDraw.Draw(txt)
    d.text((50,100), "Hello", font=fnt, fill=(0,0,0))

    for i in range(BubbleNum):
        B.append(Bubble(Size))
        
    # 楕円 : ellipse()
    # 四角 : rectangle()
    # 直線 : line()
    # draw.ellipse((100, 100, 150, 150), fill=(255, 255, 255), outline=(0,0,0))

    # Simulation
    for j in range(100):
        im = Image.new('RGB', Size, (0, 0, 0))
        # im = Image.new('RGB', Size, (120, 180, 250))
        draw = ImageDraw.Draw(im)
        filename = "./pic/image" + str(j) + ".png"
        
        for i in range(BubbleNum):
            if B[i].appear == True:
                ReplacePos(B, i)
                B[i].PosModify()
                draw.ellipse(B[i].axis, fill=(255, 255, 255), outline=(5,5,5))
                
            B[i].PosUpdate(Sampling)
            
        out = Image.composite(txt, mask, im.convert("L"))
        out.save(filename, quality=95)
        txt.save("txt.png")

        Im = Image.open(filename)
        images.append(Im)
    
    images[0].save('out.gif', save_all=True, append_images=images[1:], duration=Sampling, loop=0)
    # duration : [ms]


def ReplacePos(Object, Target):
    Num = len(Object)
    Pos = [0, 0]
    for i in range(Num):
        if Target != i:
            Pos[0] = Object[Target].position[0] - Object[i].position[0]
            Pos[1] = Object[Target].position[1] - Object[i].position[1]
            if math.sqrt(float(Pos[0]**2+Pos[1]**2)) < (Object[Target].size/2 + Object[i].size/2):
                # print("Target" , Object[Target].position)
                # print("i" , Object[i].position)
                # print(Pos)
                # print(math.sqrt(float(Pos[0]**2+Pos[1]**2)), (Object[Target].size/2 + Object[i].size/2))
                coeff = (Object[Target].size/2 + Object[i].size/2) / math.sqrt(float(Pos[0]**2 + Pos[1]**2))
                if Object[Target].size >= Object[i].size:
                    Object[i].position[0] = Object[Target].position[0] - Pos[0] * coeff
                    Object[i].position[1] = Object[Target].position[1] - Pos[1] * coeff
                else:
                     Object[Target].position[0] = Pos[0] * coeff + Object[i].position[0]
                     Object[Target].position[1] = Pos[1] * coeff + Object[i].position[1]

if __name__ == '__main__':
    main()