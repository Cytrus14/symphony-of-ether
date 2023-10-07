import uuid

class ImageSection:
    def __init__(self, x_pos=0, y_pos=0, z_pos=0, intensity=0):
        self.id = int(str(uuid.uuid4()).replace('-', ''), 16)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.intensity = intensity
    def __str__(self):
        return ('id: ' + str(self.id) + '\n' +
            'x_pos: ' + str(self.x_pos) + '\n' +
            'y_pos: ' + str(self.y_pos) + '\n' +
            'z_pos: ' + str(self.z_pos) + '\n' +
            'intensity: ' + str(self.y_pos) + '\n')