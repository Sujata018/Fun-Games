import turtle
from random import randint

'''
Draws a colorful flower with a 'Happy Diwali' wish at the bottom.
'''
colors=['yellow', 'gold','orange','red','maroon','violet','magenta','purple','navy','blue','skyblue','cyan','turquoise','lightgreen','green', 'darkgreen', 'chocolate', 'brown']
cind=0

petals=6                    # Number of petals in a single layer
layers=2                    # Number of layers
radius=200                  # Size of the outer layer of petals 
petal_lenth_width_ratio=15  # Narrowness of the petals. Increase it to draw narrower petals
textHeight=60               # Height of the text at bottom

def drawEllipse(radius):
    '''
    Draw a single petal
    '''
    global petal_lenth_width_ratio
    for i in range(2):
        turtle.circle(radius,90)
        turtle.circle(radius/petal_lenth_width_ratio,90)

def drawPetals(layer,shift=0):
    '''
    Draw a single layer of petals
    '''
    global cind,petals,radius,colors
    for petal in range(petals):
        turtle.seth(360/petals*(petal)+shift)
        turtle.color(colors[cind%len(colors)])
        cind += 1
        turtle.begin_fill()
        drawEllipse(radius*(1-layer*1/3))
        turtle.end_fill()

def drawRangoli():
    '''
    Draw a flower with petals and layers as defined using global variables
    '''
    turtle.speed=0                   # Set speed to fastest
    for layer in range(layers):
        drawPetals(layer)            # Draw a layer of petals
        drawPetals(layer,180/petals) # Shift the layer and draw again

def writeH(h=30):
    '''
    Write letter H
    '''
    turtle.seth(-90)                               # look north
    turtle.color(colors[randint(0,len(colors)-1)]) # pick a random color
    turtle.forward(h)                             
    turtle.up()
    turtle.backward(h/2)
    turtle.left(90)
    turtle.down()
    turtle.forward(h/2)
    turtle.up()
    turtle.right(90)
    turtle.backward(h/2)
    turtle.down()
    turtle.forward(h)

def writeA(h=30):
    '''
    Write letter A
    '''

    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.forward(h)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.right(90)
    turtle.forward(h)
    
    turtle.up()
    turtle.backward(h/2)
    turtle.left(90)
    turtle.backward(h/2)
    turtle.down()
    turtle.forward(h/2)
    turtle.right(90)
    turtle.forward(h/2)

def space(h=30):
    '''
    Insert space within two letters
    '''
    turtle.up()
    turtle.seth(0)
    turtle.forward(h/2)
    turtle.down()

def writeP(h=30):
    '''
    Write letter P
    '''
    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.forward(h)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.right(90)
    turtle.forward(h/2)
    
    turtle.up()
    turtle.backward(h/2)
    turtle.left(90)
    turtle.forward(h/2)
    turtle.down()

def writeY(h=30):
    '''
    Write letter Y
    '''
    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.up()
    turtle.forward(h)
    turtle.down()
    turtle.backward(h/2)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.left(90)
    turtle.forward(h/2)
    turtle.up()
    turtle.backward(h/2)
    turtle.right(90)
    turtle.backward(h/4)
    turtle.right(90)
    turtle.down()
    turtle.forward(h/2)

def writeD(h=30):
    '''
    Write letter D
    '''
    turtle.seth(0)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.forward(h/4)
    turtle.circle(h/2,45)
    turtle.seth(90)
    turtle.forward(h/2)
    turtle.circle(h/2,45)
    turtle.seth(180)
    turtle.forward(h/2)
    turtle.left(90)
    turtle.forward(h)
    turtle.up()
    turtle.left(90)
    turtle.forward(h/2)
    turtle.down()    

def writeI(h=30):
    '''
    Write letter I
    '''
    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.forward(h)
    turtle.backward(h)

def writeW(h=30):
    '''
    Write letter W
    '''
    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.forward(h)
    turtle.backward(h)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.left(90)
    turtle.forward(h)
    turtle.backward(h)
    turtle.right(90)
    turtle.forward(h/2)
    turtle.left(90)
    turtle.forward(h)
    turtle.backward(h)

def writeL(h=30):
    '''
    Write letter L
    '''
    turtle.seth(90)
    turtle.color(colors[randint(0,len(colors)-1)])
    turtle.up()
    turtle.forward(h)
    turtle.down()
    turtle.backward(h)
    turtle.right(90)
    turtle.forward(h/2)
    
    
def drawHappyDiwali():
    '''
    Write HAPPY DIWALI at the bottom.
    '''
    global colors,textHeight
    turtle.up()
    turtle.setpos(-5*textHeight,-250)
    turtle.down()
    turtle.width(10)

    writeH(textHeight)
    space(textHeight)
    writeA(textHeight)
    space(textHeight)
    writeP(textHeight)
    space(textHeight)
    writeP(textHeight)
    space(textHeight)
    writeY(textHeight)
    space(2*textHeight)
    writeD(textHeight)
    space(textHeight)
    writeI(textHeight)
    space(textHeight)
    writeW(textHeight)
    space(textHeight)
    writeA(textHeight)
    space(textHeight)
    writeL(textHeight)
    space(textHeight)
    writeI(textHeight)
    
if __name__=='__main__':
    '''
    Main program draws a colorful flower in the middle and writes text HAPPY DIWALI at the bottom.
    '''
    
    drawRangoli()
    drawHappyDiwali()
    turtle.hideturtle()
