from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
from math import *
cleargroup=Group()
def matrix_multiplication(a,b):
    columns_a=len(a[0])
    rows_a=len(a)
    columns_b=len(b[0])
    rows_b=len(b)
    
    result_matrix=[[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum=0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix
    else:
        print('Error! the columns of the first matrix must be equal to the rows of the second matrix')
        return None
        
def connect_point(i,j,k,x,y,z):
    a = k[i]
    b = k[j]
    try:
        fill=rgb(x//1,y//2,z//1)
    except:
        fill = 'black'
    cleargroup.add(Line(a[0],a[1],b[0],b[1], fill=fill))

app.stepsPerSecond = 60
angle = 0
angle_x = 0
angle_y = 0
angle_z = 0
scale = 120
speed = 0.01
points = [n for n in range(8)]
steps = 0

points[0] = [[-1], [-1], [1]]
points[1] = [[1], [-1], [1]]
points[2] = [[1], [1], [1]]
points[3] = [[-1], [1], [1]]
points[4] = [[-1], [-1], [-1]]
points[5] = [[1], [-1], [-1]]
points[6] = [[1], [1], [-1]]
points[7] = [[-1], [1], [-1]]

def onStep():
    global angle
    global steps
    global angle_x
    global angle_y
    global angle_z
    #if steps %100 ==0:
    cleargroup.clear()
    
    index = 0
    projected_points = [j for j in range(len(points))]
    
    rotation_x = [[1,0,0], [0, cos(angle_x),-sin(angle_x)], [0, sin(angle_x), cos(angle_x)]]
                
    rotation_y = [[cos(angle_y),0,-sin(angle_y)], [0,1,0], [sin(angle_y), 0, cos(angle_y)]]
    
    rotation_z = [[cos(angle_z),-sin(angle_z),0], [sin(angle_z), cos(angle_z), 0], [0,0,1]]
    
    for point in points:
        rotated_2d=matrix_multiplication(rotation_y, point)
        rotated_2d=matrix_multiplication(rotation_x, rotated_2d)
        rotated_2d=matrix_multiplication(rotation_z, rotated_2d)
        distance = 2.5
        z = 2/(distance-rotated_2d[2][0])
        #z=1
        projection_matrix = [[z,0,0],
                            [0,z,0]]
        projected_2d = matrix_multiplication(projection_matrix, rotated_2d)
        
        x = int(projected_2d[0][0]*scale)+200
        y = int(projected_2d[1][0]*scale)+200
        projected_points[index] = [x,y]
        cleargroup.add(Circle(x,y,1,fill='blue'))
        index+=1
    for m in range(4):
        connect_point(m,(m+1)%4, projected_points,x,y,z*50)
        connect_point(m+4, (m+1)%4+4, projected_points,x,y,z*50)
        connect_point(m, m+4, projected_points,x,y,z*50)
    #for m in range(4):
    #    colorx=10*m
    #    colory=35*m
    #    colorz=50*m
    #    pp = projected_points
    #    cleargroup.add(Polygon(pp[m][0],pp[m][1], pp[m+1][0],pp[m+1][1],  pp[m+2][0],pp[m+2][1], pp[m+3][0],pp[m+3][1],fill=rgb(colorx, colory, colorz)))
    steps +=1
    angle_x+=0.01
    angle_y+=0.01
    angle_z+=0.01
def onKeyHold(keys):
    global angle_x
    global angle_y
    global angle_z
    if 'w' in keys:
        angle_x+=0.05
    if 's' in keys:
        angle_x-=0.05
    if 'd' in keys:
        angle_y+=0.05
    if 'a' in keys:
        angle_y-=0.05
    if 'e' in keys:
        angle_z+=0.05
    if 'q' in keys:
        angle_z-=0.05
cmu_graphics.run()
