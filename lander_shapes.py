
from GameObject import GameObject


class Lander(GameObject):

    def __init__(self, world, position):
        polygon_points = [[[0.39,0], [0.66,0], [1,0.3], [1,1], [0,1],[0,0.3]]]
        circle_shapes = []
        image_path = "assets/lander.png"
        scale = 2

        density = 1
        friction = 0.3
        restitution = 0.4

        self.body, self.image = self.prepare_shape(world, position, polygon_points, circle_shapes, image_path, scale,
                                                   density, friction, restitution)
