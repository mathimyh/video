from manim import *
import numpy as np
import math
from itertools import chain

class SineArrow(Scene):
    def construct(self):
        amount = 14
        
        arrows = []
        
        for i in range(amount):
            arrow = Arrow(start=ORIGIN, end=1.2*RIGHT).shift(7*LEFT + i*RIGHT)
            self.add(arrow)
            arrows.append(arrow)
        
        self.wait(2)
        
        self.play(Indicate(arrows[0]))
        
        self.wait(0.5)
        
        for i in range(amount):
            arrow = arrows[i]

            # Function to update the angle of the arrow based on a sine wave
            def update_arrow(arrow, dt):
                # Create a time attribute if it doesn't exist
                if not hasattr(arrow, 'time'):
                    arrow.time = 0
                # Increment time by delta time
                arrow.time += dt
                # Calculate the angle using the sine function
                angle = np.sin(arrow.time) * PI / 4  # Adjust the amplitude as needed
                arrow.set_angle(angle)
                
                # Adjust color according to the angle
                h_val = (np.sin(arrow.time) * 60 + 180) / 360
                color = ManimColor.from_hsv([h_val, 1, 0.6])
                arrow.set_color(color)
                

            # Add the updater to the arrow
            arrow.add_updater(update_arrow)

            # Animate the scene
            self.wait(0.4)

        self.wait(10)



class Magnet(MovingCameraScene):
    def construct(self):
        
        # Colors
        value = 0.6
        
        # Create the rectangular magnet
        magnet = Rectangle(height=3.1, width=10, color = GRAY)
        self.play(Create(magnet))
        self.wait(0.5)
        
        # Show north and south 
        line = Line(start=np.array([0., -1.55, 0.]), end=np.array([0., 1.55, 0.]), color = GRAY ,buff=2)
        north = Text('N', font_size=80, color=RED_E, fill_opacity=1).shift(2.5*RIGHT)
        south = Text('S', font_size=80, color= DARK_BLUE, fill_opacity=1).shift(2.5*LEFT)
        
        # Turn N and S into an arrow indicating field direction
        self.play(AnimationGroup(GrowFromCenter(south), GrowFromCenter(north), GrowFromCenter(line)))     
        self.wait(1)
        fields = []
        for i in range(30):
            temp = []
            for j in range(10):
                field = Arrow(start=np.array([-4,0.,0.]), end=np.array([4,0.,0.]))
                field.set_color(ManimColor.from_hsv([180/360,1,value]))
                temp.append(field)
            fields.append(temp)
        self.play(AnimationGroup(ShrinkToCenter(south), ShrinkToCenter(north), ShrinkToCenter(line), GrowArrow(fields[0][0])))   
        self.wait(1)
        
        self.add(*list(chain.from_iterable(fields)))
        
        # Create all the small arrows
        yea = 31
        no = 10
        
        arrows = []
        
        for i in range(30):
            temp = []
            for j in range(10):
                arrow = Arrow(start=np.array([-5 + 10 * (i+1/2)/yea, 1.5 - 3 * (1/2+j)/no, 0.]), end=np.array([-5 + 10 * (1/2+i)/yea + 9/yea, 1.5 - 3 * (1/2+j)/no,0.]))
                arrow.set_color(ManimColor.from_hsv([180/360,1,value]))
                temp.append(arrow)
            arrows.append(temp)
          
        # # Animation for shrinking the field arrow down and adding all the other
        # arrow_fadings = []
        # fade_outs = []
        # for elem in arrows:
        #     for arrow in elem:
        #         arrow_fadings.append(FadeIn(arrow)) 
        #         fade_outs.append(FadeOut(arrow)) 
            
        # This does not work, but dont want to remove it just yet  
        # self.play(LaggedStart(ReplacementTransform(field, arrows[math.trunc(len(arrows)/2)][math.trunc(len(arrows[0])/2)]), AnimationGroup(arrow_fadings), lag_ratio=0.5))
        # self.wait(1)'
        
        shrinks = []
        for i in range(30):
            for j in range(10):
                shrinks.append(ReplacementTransform(fields[i][j], arrows[math.trunc(len(arrows)/2)][math.trunc(len(arrows[0])/2)]))
        
        transforms = []
        for i in range(30):
            for j in range(10):
                transforms.append(Transform(fields[i][j], arrows[i][j]))
        
        
        # Shrink it down and add the other arrows. Remove the extra one 
        # self.play(Transform(field, arrows[math.trunc(len(arrows)/2)][math.trunc(len(arrows[0])/2)]))
        # self.play(*shrinks)
        self.play(*transforms)
        # self.play(*arrow_fadings)
        self.wait(2)
        
        backgrounds = []
        spins = []
        
        # Make the new grid with smaller arrows that represent spin.
        for i in range(64):
            temp = []
            temp2 = []
            for j in range(32):
                arrow = Arrow(start=np.array([-10 + 20 * (i+1/2)/yea, 3.2 - 6.4 * (1/2+j)/no, 0.])/1000, end=np.array([-10 + 20 * (1/2+i)/yea + 16/yea, 3.2 - 6.4 * (1/2+j)/no,0.])/1000)
                arrow.set_color(ManimColor.from_hsv([180/360,1,value]))
                if i < 16 or i > 47 or j < 7 or j > 24:
                    temp.append(arrow)
                else:
                    temp2.append(arrow)
            backgrounds.append(temp)
            if len(temp2) != 0:
                spins.append(temp2)
        
        background_fade_ins = []
        for elem in backgrounds:
            for yeayeay in elem:
                background_fade_ins.append(FadeIn(yeayeay, run_time=0.2))
                
        spins_fade_ins = [] 
        for elem in spins:
            for spin in elem:
                spins_fade_ins.append(FadeIn(spin, run_time=0.2))
        
        # Make a middle grid to transition better :)
        middles1 = []
        for i in range(32):
            temp = []
            for j in range(16):
                arrow = Arrow(start=np.array([-5 + 10 * (i+1/2)/yea, 1.6 - 3.2 * (1/2+j)/no, 0.])/10, end=np.array([-5 + 10 * (1/2+i)/yea + 9/yea, 1.6 - 3.2 * (1/2+j)/no,0.])/10)
                arrow.set_color(ManimColor.from_hsv([180/360,1,value]))
                temp.append(arrow)
            middles1.append(temp)
        
        middles_fade_ins1 = []
        for elem in middles1:
            for middle in elem:
                middles_fade_ins1.append(FadeIn(middle, run_time = 0.2))  
                 
        
        # Zoom in 
        self.play(LaggedStart(self.camera.auto_zoom([spins[1][1], spins[-2][-2]], margin=5e-4), AnimationGroup(middles_fade_ins1), AnimationGroup(background_fade_ins, spins_fade_ins), lag_ratio=[0.67,1.1], run_time=2.5))
        self.remove(*list(chain.from_iterable(middles1)), *list(chain.from_iterable(backgrounds)), *list(chain.from_iterable(arrows)), magnet)  
        self.wait()  
        
        # Bug maybe so I have to add the spins all over....
        spinnings = []
        for i in range(32):
            temp = []
            for j in range(18):
                arrow = Arrow(start=np.array([-10 + 20 * (i+1/2)/yea + 20*16/yea, 3.2 - 6.4 * (1/2+j)/no - 6.4*7/no, 0.])/1000, end=np.array([-10 + 20 * (1/2+i)/yea + 16/yea + 20*16/yea, 3.2 - 6.4 * (1/2+j)/no - 6.4*7/no,0.])/1000)
                arrow.set_color(ManimColor.from_hsv([180/360,1,value]))
                temp.append(arrow)
            spinnings.append(temp)
            
        self.add(*list(chain.from_iterable(spinnings)))
        self.wait(1)
        self.remove(*list(chain.from_iterable(spins)))
        
        # Make it so only one row is showing at first. Also indicate the first in the row before it gets excited
        fade_outs = []
        fade_ins = []
        zooms = []
        for i, col in enumerate(spinnings):
            for j, row in enumerate(col):
                if i < 10 or i > 20 or j != 8:
                    fade_outs.append(FadeOut(row))
                    fade_ins.append(FadeIn(row))          
        self.play(*fade_outs)
        self.wait(0.5)
    
        # Function to update the angle of the arrow based on a sine wave
        def update_arrow(arrow, dt):
            # Create a time attribute if it doesn't exist
            if not hasattr(arrow, 'time'):
                arrow.time = 0
            # Increment time by delta time
            arrow.time += dt
            # Calculate the angle using the sine function
            angle = np.sin(arrow.time) * PI / 5  # Adjust the amplitude as needed
            arrow.set_angle(angle)
            
             # Adjust color according to the angle
            h_val = (np.sin(arrow.time) * 60 + 180) / 360
            color = ManimColor.from_hsv([h_val, 1, value])
            arrow.set_color(color)
        
        # Zoom in on the chain
        self.play(self.camera.auto_zoom([spinnings[10][8],spinnings[20][8]], margin = 5e-4))
        self.wait(1)
        
        self.play(Indicate(spinnings[10][8]))
        self.wait(0.5)
        
        # Make all the spins follow a spin wave
        for i, row in enumerate(spinnings):
            for arrow in row:
                arrow.add_updater(update_arrow)
            if i > 9 and i < 21:
                self.wait(0.4)
        self.wait(2)
        
        # Update the time for the spins that are fading in. When they are out they do not update so need to do it manually. 
        for i, col in enumerate(spinnings):
            for j, row in enumerate(col):
                if i < 10 or i > 20 or j != 8:
                    row.time = spinnings[13][8].time + (13 - i)*0.4 
        
        # Fade the spins back in
        self.play(*fade_ins)
        
        # Update the time for the spins that are fading in. When they are out they do not update so need to do it manually. 
        for i, col in enumerate(spinnings):
            for j, row in enumerate(col):
                if i < 10 or i > 20 or j != 8:
                    row.time = spinnings[13][8].time + (13 - i)*0.4 
        self.wait(2)
        
        # Zoom out again
        self.play(self.camera.auto_zoom([spins[1][1], spins[-2][-2]], margin=5e-4))
        self.wait(10)


