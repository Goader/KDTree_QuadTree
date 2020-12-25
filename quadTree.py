class Point:
    def __init__(self,point):
       self.x = point[0]
       self.y = point[1]

class Rectnagle:
    def __init__(self,left_down_corner,right_upper_corner):
        self.x_down = left_down_corner[0]
        self.y_down = left_down_corner[1]
        self.x_upper = right_upper_corner[0]
        self.y_upper = right_upper_corner[1]

    def contains(self,point):
            return (point.x >= self.x_down and point.x <=self.x_upper and point.y >= self.y_down and point.y <= self.y_upper )

class QuadTree:
    def __init__(self,boundary,capacity,intersection_points):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.intersection_points = intersection_points
    def subdivide(self):
        x_down = self.boundary.x_down
        y_down = self.boundary.y_down
        height = self.boundary.y_upper - self.boundary.y_down
        width= self.boundary.x_upper - self.boundary.x_down
        right_upper_rectangle = Rectnagle([x_down+width/2,y_down+height/2],[x_down+width,y_down+height])
        left_upper_rectangle = Rectnagle([x_down,y_down+height/2],[x_down+width/2,y_down+height])
        right_down_rectangle = Rectnagle([x_down+width/2,y_down],[x_down+width,y_down+height/2])
        left_down_rectangle = Rectnagle([x_down,y_down],[x_down+width/2,y_down+height/2])
        self.right_upper = QuadTree(right_upper_rectangle,self.capacity,self.intersection_points)
        self.left_upper = QuadTree(left_upper_rectangle, self.capacity,self.intersection_points)
        self.left_down = QuadTree(left_down_rectangle,self.capacity,self.intersection_points)
        self.right_down = QuadTree(right_down_rectangle,self.capacity,self.intersection_points)
        self.intersection_points.append([x_down+width/2,y_down+height/2])
        self.intersection_points.append([x_down+width/2,y_down])
        self.intersection_points.append([x_down+width/2,y_down+height])
        self.intersection_points.append([x_down,y_down+height/2])
        self.intersection_points.append([x_down+width,y_down+height/2])
    def insert(self,point):
        if(self.boundary.contains(point)==False):
            return
        if (len(self.points)<self.capacity):
            self.points.append(point)
            return self.intersection_points
        else:
            if (self.divided == False):
                self.subdivide()
                self.divided = True
            self.right_upper.insert(point)
            self.right_down.insert(point)
            self.left_upper.insert(point)
            self.left_down.insert(point)

def find_all_intersections_point(rectangular,points):
    intersections_points =[]
    quad_tree = QuadTree(rectangular,1,[])
    for i in range (len(points)):
        intersections_points.append(quad_tree.insert(points[i]))
    return (intersections_points[0])

rectangular = Rectnagle([0,0],[20,20])
print(find_all_intersections_point(rectangular,[Point([0,2]),Point([10,5]),Point([7,7]),Point([7,8])]))
