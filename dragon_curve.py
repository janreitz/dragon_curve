import cairo
import math

# [1]
# [1,1,0]
# [1,1,0,1,1,0,0]
# [1,1,0,1,1,0,0,1,1,1,0,0,1,0,0]

# configuration
WIDTH, HEIGHT = 10000, 10000
NUM_FOLDS = 20
def dragon_curve(folds: int):
    paper = []
    for _ in range(folds):
        paper = fold1(paper)
    return paper

def fold1(paper):
    new_paper = []
    new_folds = [1 if i%2 == 0 else 0 for i in range(len(paper) + 1)]
    for i in range(len(new_folds) + len(paper)):
        if i%2 == 0:
            new_paper.append(new_folds[math.floor(i/2)])
        else:
            new_paper.append(paper[math.floor(i/2)])
    return new_paper

def fold2(paper):
    new_paper = paper
    new_folds = [1 if i%2 == 0 else 0 for i in range(len(paper) + 1)]
    for i, fold in enumerate(new_folds):
        new_paper.insert(i*2, fold)
    return new_paper

if __name__ == "__main__":
    paper = []
    for i in range(NUM_FOLDS):
        paper = fold1(paper)

    # generating arc data to plot
    max_x, max_y = 0, 0
    min_x, min_y = 0, 0
    x, y = 0, 0 # Start
    radius = 1
    direction = (-1,0)
    arcs = []
    for fold in paper:
        if direction == (1,0):
            if not fold: # right hand arc
                arcs += [(x, y + radius, - math.pi/2, 0) ]
                #ctx.arc(x, y + radius, radius, - math.pi/2, 0)
                x = x + radius
                y = y + radius
                direction = (0, 1)
            else: # left hand arc
                arcs += [ (x, y - radius, math.pi/2, 0)]
                #ctx.arc_negative(x, y - radius, radius, math.pi/2, 0)
                x = x + radius
                y = y - radius
                direction = (0, -1)
        elif direction == (0,1):
            if not fold: # right hand arc
                arcs += [(x - radius, y, 0, math.pi/2) ]
                #ctx.arc(x - radius, y, radius, 0, math.pi/2)
                x = x - radius
                y = y + radius
                direction = (-1, 0)
            else: # left hand arc
                arcs += [ (x + radius, y, math.pi, math.pi/2)]
                #ctx.arc_negative(x + radius, y, radius, math.pi, math.pi/2)
                x = x + radius
                y = y + radius
                direction = (1, 0)
        elif direction == (-1,0):
            if not fold: # right hand arc
                arcs += [(x, y - radius, math.pi/2, math.pi) ]
                #ctx.arc(x, y - radius, radius, math.pi/2, math.pi)
                x = x - radius
                y = y - radius
                direction = (0, -1)
            else: # left hand arc
                arcs += [ (x, y + radius, -math.pi/2, math.pi)]
                #ctx.arc_negative(x, y + radius, radius, -math.pi/2, math.pi)
                x = x - radius
                y = y + radius
                direction = (0, 1)
        elif direction == (0,-1):
            if not fold: # right hand arc
                arcs += [(x + radius, y, math.pi, - math.pi/2) ]
                #ctx.arc(x + radius, y, radius, math.pi, - math.pi/2)
                x = x + radius
                y = y - radius
                direction = (1, 0)
            else: # left hand arc
                arcs += [(x - radius, y, 0, - math.pi/2)]
                #ctx.arc_negative(x - radius, y, radius, 0, - math.pi/2)
                x = x - radius
                y = y - radius
                direction = (-1, 0)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        min_x = min(x, min_x)
        min_y = min(y, min_y)
    
    image_width = (max_x - min_x)
    image_height = (max_y - min_y)

    # Drawing the curve
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context (surface)
    scaling_factor = min(WIDTH/image_width, HEIGHT/image_height)
    ctx.scale(scaling_factor, scaling_factor) 
    ctx.translate(-min_x, -min_y) 
    # background
    ctx.set_source_rgb(0.133,0.314,0.584)
    ctx.paint()

    # Line brush setup
    ctx.set_source_rgb(0.9,0.9,0.9)
    ctx.set_line_width(0.1)

    i = 0
    for x, y, angle_start, angle_stop in arcs:
        if paper[i]:
            ctx.arc_negative(x, y, radius, angle_start, angle_stop)
        else:
            ctx.arc(x, y, radius, angle_start, angle_stop)
        i += 1
    
    ctx.stroke()
    surface.write_to_png("dragon_curve.png")  # Output to PNG






