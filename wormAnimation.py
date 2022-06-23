import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon, Circle
import matplotlib.gridspec as gridspec
from neuron import h,gui

class Cell:
    def __init__(self, gid,x,y,z):
        self.gid = gid
        self._setup_morphology()
        self.all=self.soma.wholetree()
        self._setup_biophysics()
        self.x = x
        self.y = y
        self.z = z

        self.spike_detector = h.NetCon(self.soma(0.5)._ref_v,None,sec=self.soma)
        self.spike_times = h.Vector()
        self.spike_detector.record(self.spike_times)

        self.ncs = []

        self.soma_v = h.Vector().record(self.soma(0.5)._ref_v)

    def __repr__(self):
        return "{}[{}]".format(self.name,self.gid)
    
class BallAndStick(Cell):
    name = 'Ball and Stick' 
 
    def _setup_morphology(self):
        self.soma = h.Section(name="soma",cell=self)
        self.dend = h.Section(name="dend",cell=self)

        self.dend.connect(self.soma)

        self.soma.L = self.soma.diam=12.6157 # Length in micro meter
        self.dend.L = 200   # Length in micro meter
        self.dend.diam = 1  # Diameter in micro meter

    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100    # Axial resistenace in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads/ cm^2
        
        self.soma.insert('hh')

        for seg in self.soma:
            seg.hh.gnabar = 0.12 # Sodium conductance in S/cm^2
            seg.hh.gkbar = 0.036 # Potassium conductance in S/cm^2
            seg.hh.gl = 0.0003   # Leak conductance in S/cm^2
            seg.hh.el = -54.3    # Reversal potential in mV
            
        # Insert passive current in the dendrite
        self.dend.insert('pas')
        for seg in self.dend:
            seg.pas.g = 0.001 # Passive conductance in S/cm^2
            seg.pas.e = -65   # Leak reversal potential in mV

        # The synapse
        self.syn = h.ExpSyn(self.dend(0.5))
        self.syn.tau = 2
        self.syn_i = h.Vector().record(self.syn._ref_i)
        
class CElegans:
    '''
    A network of 10 ball-and-stick cells : 2 receptors (sensilla), connected with
    2 interneurons, which in turn are connected with a pair of cords consisteing
    of 3 cells each, which are motoneurons, that control ventral muscles and
    dorsal muscles
    '''
    def __init__(
        self,sensilla_pos,stim_w=0.4, stim_t=9, stim_delay=1, syn_w=0.5, syn_delay=10
    ):
        '''
        param stim_w: Weight of the stimulus
        param stim_t: time of the stimulus (in ms)
        param stim_delay: delay of the stimulus (in ms)
        param syn_w: Synaptic weight
        param syn_delay: Delay of the synapse
        '''
        self.syn_w = syn_w
        self.stim_t = stim_t
        self.stim_delay = stim_delay
        self.stim_w = stim_w
        self.syn_delay = syn_delay
        self._create_cells(sensilla_pos)
        self._connect_cells()

        self.t = h.Vector().record(h._ref_t)

    def _add_stimulus(self,cell_num,stimnum=1):
        # add stimulus
        self.netstim = h.NetStim()
        self.netstim.number = stimnum
        self.netstim.start = self.stim_t
        self.nc = h.NetCon(self.netstim, self.cells[cell_num].syn)
        self.nc.delay = self.stim_delay
        self.nc.weight[0] = self.stim_w
        
    def _create_cells(self,pos):
        self.cells = []

        # sensilla
        self.cells.append(BallAndStick(0,pos[0],pos[1],pos[2]))        # first sensilla to setect food
        self.cells.append(BallAndStick(1,pos[0]+50,pos[1],pos[2]))     # second sensilla to sense touch
        self.cells.append(BallAndStick(1,pos[0]+100,pos[1],pos[2]))    # third sensilla to sense torch light
        
        # interneurons
        self.cells.append(BallAndStick(2,pos[0],pos[1]+50,pos[2]))     # three for forward movement 
        self.cells.append(BallAndStick(3,pos[0],pos[1]+100,pos[2]))    
        self.cells.append(BallAndStick(4,pos[0],pos[1]+150,pos[2]))    
          
        self.cells.append(BallAndStick(5,pos[0]+50,pos[1]+100,pos[2])) # for shrinking
          
        self.cells.append(BallAndStick(2,pos[0],pos[1]+50,pos[2]))     # three for backward movement 
        self.cells.append(BallAndStick(3,pos[0],pos[1]+100,pos[2]))    
        self.cells.append(BallAndStick(4,pos[0],pos[1]+150,pos[2]))    
          
        # ventral cord
        self.cells.append(BallAndStick(6,pos[0]-60,pos[1]+50,pos[2]))    
        self.cells.append(BallAndStick(7,pos[0]-60,pos[1]+100,pos[2]))    
        self.cells.append(BallAndStick(8,pos[0]-60,pos[1]+150,pos[2]))    

        # dorsal cord
        self.cells.append(BallAndStick(9,pos[0]+60,pos[1]+50,pos[2]))  
        self.cells.append(BallAndStick(10,pos[0]+60,pos[1]+100,pos[2]))  
        self.cells.append(BallAndStick(11,pos[0]+60,pos[1]+150,pos[2]))  
        
    def _connect_cells(self):

        # connect sensilla to interneurons
        source = self.cells[0]
        target = self.cells[3]
        self._connect_source_target(source,target)
       
        source = self.cells[1]
        target = self.cells[6]
        self._connect_source_target(source,target)

        source = self.cells[2]
        target = self.cells[7]
        self._connect_source_target(source,target)

        # Connection between interneurons
        source = self.cells[3]
        target = self.cells[4]
        self._connect_source_target(source,target)

        source = self.cells[4]
        target = self.cells[5]
        self._connect_source_target(source,target)

        source = self.cells[7]
        target = self.cells[8]
        self._connect_source_target(source,target)

        source = self.cells[8]
        target = self.cells[9]
        self._connect_source_target(source,target)

        # connect interneurons to ventral chord for forward movement (serial)
        source = self.cells[3]
        target = self.cells[10]
        self._connect_source_target(source,target)

        source = self.cells[4]
        target = self.cells[11]
        self._connect_source_target(source,target)

        source = self.cells[5]
        target = self.cells[12]
        self._connect_source_target(source,target)

        # connect interneurons to ventral chord for backward movement (serial)
        source = self.cells[7]
        target = self.cells[12]
        self._connect_source_target(source,target)

        source = self.cells[8]
        target = self.cells[11]
        self._connect_source_target(source,target)

        source = self.cells[9]
        target = self.cells[10]
        self._connect_source_target(source,target)

       # connect interneuron to ventral chord for shrink (parallel)
        source = self.cells[6]
        target = self.cells[10]
        self._connect_source_target(source,target)

        source = self.cells[6]
        target = self.cells[11]
        self._connect_source_target(source,target)

        source = self.cells[6]
        target = self.cells[12]
        self._connect_source_target(source,target)
        
        # connect interneurons to dorsal chord for forward movement (serial)
        source = self.cells[3]
        target = self.cells[13]
        self._connect_source_target(source,target)

        source = self.cells[4]
        target = self.cells[14]
        self._connect_source_target(source,target)

        source = self.cells[5]
        target = self.cells[15]
        self._connect_source_target(source,target)

        # connect interneurons to dorsal chord for backward movement (serial)
        source = self.cells[7]
        target = self.cells[15]
        self._connect_source_target(source,target)

        source = self.cells[8]
        target = self.cells[14]
        self._connect_source_target(source,target)

        source = self.cells[9]
        target = self.cells[13]
        self._connect_source_target(source,target)

        # connect interneuron to dorsal chord for shrink (parallel)
        source = self.cells[6]
        target = self.cells[13]
        self._connect_source_target(source,target)

        source = self.cells[6]
        target = self.cells[14]
        self._connect_source_target(source,target)

        source = self.cells[6]
        target = self.cells[15]
        self._connect_source_target(source,target)

        
    def _connect_source_target(self,source,target):
        nc = h.NetCon(source.soma(0.5)._ref_v, target.syn, sec=source.soma)
        nc.weight[0] = self.syn_w
        nc.delay = self.syn_delay
        source.ncs.append(nc)


class wormPit(object):
    worm_color = 'red'
    worm_border_color = 'black'
    worm = None
    shrinked_worm = None
    food = None
    food_color = 'green'
    food_count = 0
    egg_point=[]
    CElegan = None
    
    def __init__(self):
        self.mouth_pos = 15
        self.width = 200
        self.height = 80
        self.worm_points=[]

        # Create the figure and axes to draw the worm
        self.fig1 = plt.figure(figsize=(self.width,self.height))
        self.ax1 = self.fig1.add_axes((0.05,0.05,0.9,0.9),
                                    aspect='equal', frameon=False,
                                    xlim=(-0.05,self.width+0.05),
                                    ylim=(-0.05+self.height+0.05))
        for axis in (self.ax1.xaxis,self.ax1.yaxis):
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())

        # Draw the CElegan
        self._drawWorm(4)

        # Create event hook for mouse clicks
        self.fig1.canvas.mpl_connect('button_press_event',self._button_press)

        # Create event hook for mouse hover
        self.fig1.canvas.mpl_connect('motion_notify_event',self._mouse_hover)

        # Create neuron structure of the worm
        self.CElegan = self._create_neurons() 

        # Create the figure to plot Neuron firings of the worm
        self.fig2 = plt.figure()
        self.gs = gridspec.GridSpec(nrows=4, ncols=3)
        h.finitialize(-65)
        h.continuerun(100)  # simulate for 100 mS

        self._plot_firings()

   
    def _drawWorm(self,width):
        '''
        Draws the worm
        '''
        top_pts = []
        bottom_pts = []
        width /= 2
        
        for i in range(self.mouth_pos - 14,self.mouth_pos):
            k = i%6
            if k == 1 or k == 2:
                top_y = 5 + width
                bottom_y = 5 - width
                
            elif k == 3 or k == 0:
                top_y = 4 + width
                bottom_y = 4 - width
                
            elif k == 4 or k == 5:
                top_y = 3 + width
                bottom_y = 3 - width

            top_pts.append([i,top_y])
            bottom_pts.append([i,bottom_y])

            if i == self.mouth_pos - 14:
                tail_y = bottom_y + width
            elif i == self.mouth_pos - 1:
                mouth_y = bottom_y + width
            elif i == self.mouth_pos - 10:
                self.egg_point = [i,top_y]

                
        top_pts.append([self.mouth_pos,mouth_y])
        
        self.worm_points = top_pts + list(reversed(bottom_pts)) + [[self.mouth_pos-15,tail_y]] + [top_pts[0]]
#        p = Polygon(self.worm_points, fc=self.worm_color, ec=self.worm_border_color)
        if width == 2:
            self.worm = Polygon(self.worm_points, fc=self.worm_color)
            self.ax1.add_patch(self.worm)
        else:
            self.shrinked_worm = Polygon(self.worm_points, fc=self.worm_color)
            self.ax1.add_patch(self.shrinked_worm)

        self.fig1.canvas.draw()

    def _button_press(self, event):
        if (event.xdata is None) or (event.ydata is None):               # invalid click
            return
        x,y = map(int,(event.xdata,event.ydata))
        if (x < 0 or y < 0 or x >= self.width or y >= self.height):      # click outside window
            return

        if self.shrinked_worm is not None:
            self.shrinked_worm.set_visible(False)
        if self.food is not None:
            self.food.set_visible(False)

        if (x in range(self.mouth_pos - 15,self.mouth_pos+1)) and (y in range (1,8)):  # touching the worm
            if self.food_count > 0:
                self.food_count = 0
            self._shrinkWorm()
            self._touch_head(self.CElegan)
            
        elif (x >  self.mouth_pos) and (y in range (1,8)):               # giving food to the worm or lighting torch
            if event.button == 1:                                        # lighting torch
                self.mouth_pos -= 2
                self.worm.set_visible(False)
                self._drawWorm(4)
                plt.pause(0.5)
                self._light_torch(self.CElegan, 1)
            else:                                                        # giving food    
                self._drawFood(x,y)
                num_moves = 0
                while (x > self.mouth_pos):
                    self.mouth_pos += 1
                    plt.pause(0.5)
                    self.worm.set_visible(False)
                    self._drawWorm(4)
                    num_moves += 1
                plt.pause(6)
                self._removeFood()
                plt.pause(1)

                self._give_food(self.CElegan, num_moves)
                plt.pause(1)
            
                if self.food_count >= 3:                                     # lay an egg if getting too much food
                    self.food_count = 0
                    self._layEgg()
                    plt.pause(1)
                    self._lay_egg(self.CElegan)

        else:                                                            # click on any other place in screen
            return

    def _mouse_hover(self, event):
        plt.figure(self.fig1.number)
        plt.text(15,15,"Click on head to touch head")            
        plt.text(15,20,"Left click to light torch")
        plt.text(15,25,"Right click to place chemical attractant")            
        self.fig1.canvas.draw()
        return

    def _shrinkWorm(self):
        plt.figure(self.fig1.number)

        plt.pause(0.5)                      # wait for 0.5 seconds
        self.worm.set_visible(False)
        self._drawWorm(2)                   # shrink
        
        plt.pause(5)                        # wait for 5 seconds

        self.shrinked_worm.remove()
        self.worm.set_visible(True)         # expand again
        self.fig1.canvas.draw()
        return

    def _drawFood(self,x,y):
        plt.figure(self.fig1.number)

        food_points=[[x+1,y+1],[x-1,y+1],[x-1,y-1],[x+1,y-1],[x+1,y+1]]
        self.food = Polygon(food_points, fc=self.food_color)              # draw a green square food
        self.ax1.add_patch(self.food)

        self.fig1.canvas.draw()
        self.food_count += 1
        return

    def _removeFood(self):
        plt.figure(self.fig1.number)
        self.food.remove()
        self.fig1.canvas.draw()
        return

    def _layEgg(self):
        plt.figure(self.fig1.number)

        egg = Circle(self.egg_point, radius=1, color='grey')    # draw a round egg
        self.ax1.add_patch(egg)

        self.fig1.canvas.draw()
        return

    def _plot_firings(self):

        plt.figure(self.fig2.number)

        plt.clf()

        ax1=plt.subplot(4,3,10)
        plt.plot(self.CElegan.t,self.CElegan.cells[13].soma_v)
        plt.title('MotoNeuron Dorsal (front)')

        ax2=plt.subplot(4,3,11)
        plt.plot(self.CElegan.t,self.CElegan.cells[14].soma_v)
        plt.title('MotoNeuron Dorsal (middle)')

        ax3=plt.subplot(4,3,12)
        plt.plot(self.CElegan.t,self.CElegan.cells[15].soma_v)
        plt.title('MotoNeuron Dorsal (back)')

        plt.subplot(431,sharex=ax1)
        plt.plot(self.CElegan.t,self.CElegan.cells[0].soma_v)
        plt.title('Sensilla 1')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(432,sharex=ax2)
        plt.plot(self.CElegan.t,self.CElegan.cells[1].soma_v)
        plt.title('Sensilla (for touch)')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(433,sharex=ax3)
        plt.plot(self.CElegan.t,self.CElegan.cells[2].soma_v)
        plt.title('Sensilla 3')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(434,sharex=ax1)
        plt.plot(self.CElegan.t,self.CElegan.cells[3].soma_v)
        plt.title('InterNeuron 1')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(435,sharex=ax2)
        plt.plot(self.CElegan.t,self.CElegan.cells[4].soma_v)
        plt.title('InterNeuron 2')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(436,sharex=ax3)
        plt.plot(self.CElegan.t,self.CElegan.cells[5].soma_v)
        plt.title('InterNeuron 3')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(437,sharex=ax1)
        plt.plot(self.CElegan.t,self.CElegan.cells[10].soma_v)
        plt.title('MotoNeuron Ventral (front)')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(438,sharex=ax2)
        plt.plot(self.CElegan.t,self.CElegan.cells[11].soma_v)
        plt.title('MotoNeuron Ventral (middle)')
        plt.tick_params('x', labelbottom=False)

        plt.subplot(439,sharex=ax3)
        plt.plot(self.CElegan.t,self.CElegan.cells[12].soma_v)
        plt.title('MotoNeuron Ventral (back)')
        plt.tick_params('x', labelbottom=False)
             
        plt.show()

    def _create_neurons(self):
        h.load_file("stdrun.hoc")

        ## Create a worm
        cell_pos = [0,0,0]
        CElegan=CElegans(cell_pos)
        return CElegan

    def _touch_head(self,CElegan):
        CElegan._add_stimulus(1)
        h.finitialize(-65)
        h.continuerun(100)  # simulate for 100 mS
        self._plot_firings()

    def _give_food(self,CElegan, num):
        CElegan._add_stimulus(0,num)
        h.finitialize(-65)
        h.continuerun(100)  # simulate for 100 mS
        self._plot_firings()

    def _lay_egg(self,CElegan):
        CElegan._add_stimulus(5)
        h.finitialize(-65)
        h.continuerun(100)  # simulate for 100 mS
        self._plot_firings()

    def _light_torch(self,CElegan, num):
        CElegan._add_stimulus(2,num)
        h.finitialize(-65)
        h.continuerun(100)  # simulate for 100 mS
        self._plot_firings()


if __name__=='__main__':

    worm = wormPit()           # Draw worm in wormpit
    plt.show()
