import math
import matplotlib.pyplot as plt
import pandas as pd
    
def main():
    #theta = float(input('theta: '))
    #print(shooter_angle(theta))
    graph_points() 

def graph_points():
    data = {'theta':[], 'shot angle':[], 'alpha':[], 'encoder left':[]}
    min = 87.9141869
    max = 163
    theta = min
    step = 0.25
    while theta <= max:
        data['theta'].append(theta)
        data['shot angle'].append(shooter_angle(theta)[0])
        data['alpha'].append(shooter_angle(theta)[1])
        print(theta, data['shot angle'][-1])
        theta += step

    # encpder left sub woof: .497 --> 0.707
    encoder_step = (0.708 - 0.497) / (len(data['theta'])-1)
    pos = 0.708
    for i in range(len(data['theta'])):
        data['encoder left'].append(pos)
        pos -= encoder_step

    
    plt.plot(data['encoder left'], data['shot angle'])

    #labels = ['intake', 'subwoof fast', "min angle", 'subwoof store']
    plt.scatter(0.49700000000001626, 66.14798090891051, c = 'black')
    plt.annotate('intake (0.497)', (0.49700000000001626 + 0.005, 66.14798090891051))
    
    plt.scatter(0.5244300000000144, 46.419038891096505, c = 'black')
    plt.annotate('subwoof fast (0.5244)', (0.5244300000000144 + 0.005, 46.419038891096505))

    plt.scatter(0.6243033333333399, 25.598161555783452, c = 'black')
    plt.annotate('min angle (0.6243)', (0.6243033333333399 + 0.005, 25.598161555783452))

    plt.scatter(0.708, 50.59359786181974, c = 'black')
    plt.annotate('subwoof store (0.708)', (0.708 + 0.005 ,50.59359786181974))
        
    
    plt.ylabel('angle of shot (degrees)')
    plt.xlabel('value of absolute encoder (degrees)')
    plt.title('encoder value vs shot angle')
    plt.grid(True, which='minor', linestyle='-', linewidth=0.25, color='gray')  # main grid lines
    plt.grid(True, which='major', linestyle=':', linewidth=0.5, color='black')
    plt.minorticks_on()
    plt.show()


def shooter_angle(theta):
    a = [0, 2.5]
    b = [11.153559,0]
    c = [cos(theta) * 17.671305 + 11.153559, sin(theta) * 17.671305]
    #print(c)
    
    max = 210
    min = (180/ math.pi) * math.atan((c[1] - a[1]) / (c[0]))
    
    #print(theta)
    if min < 0:
        min = 180 + min

    alpha = ((max - min) / 2) + min
    guess = math.sqrt((c[0] - (10.588640 * sin(alpha) + a[1])) ** 2 + (c[1] - (10.588640 * cos(alpha))) ** 2 )
    while int((guess * 1000)) / 1000 != 8.625:
        alpha_more = ((max - alpha) / 2) + alpha
        guess_more = math.sqrt((c[1] - (10.588640 * sin(alpha_more) + a[1])) ** 2 + (c[0] - (10.588640 * cos(alpha_more))) ** 2 )

        alpha_less = ((alpha - min) / 2) + min
        guess_less = math.sqrt((c[1] - (10.588640 * sin(alpha_less) + a[1])) ** 2 + (c[0] - (10.588640 * cos(alpha_less))) ** 2 )
        
        if math.fabs(guess_less - 8.625) < math.fabs(guess_more - 8.625):
            guess = guess_less
            alpha = alpha_less
            max = alpha_more
        else:
            guess = guess_more
            alpha = alpha_more
            min = alpha_less

        guess = math.sqrt((c[1] - (10.588640 * sin(alpha) + a[1])) ** 2 + (c[0] - (10.588640 * cos(alpha))) ** 2 )
        

    d = [10.588640 * cos(alpha), 10.588640 * sin(alpha) + 2]

    dx = math.fabs(d[0] - c[0])
    beta = (180/ math.pi) * math.acos((dx*b[0]) / (8.625 * 11.153559))

    return beta, alpha
    

def cos(theta):
    return math.cos(theta * (math.pi / 180))

def sin(theta):
     return math.sin(theta * (math.pi / 180))

if __name__ == '__main__':
    main()