import numpy as np

class WaveFrontReader:
    def __init__(self, path):
        self.model = load_model_from_file(path)
        self.processData()

    def processData(self):
        self.vertices = [] #all vertices with their informations
        self.materials = {} #all materials as keys and the start indexes for the vertices array
        
        for index in range(0,len(self.model['faces'])):
            current_face = self.model['faces'][index]
            
            if(current_face[2] not in self.materials):
                self.materials[current_face[2]] = index
            
            for i in range(0,3):
                self.vertices.extend(self.model['vertices'][current_face[0][i]-1])
                self.vertices.extend(self.model['texture'][current_face[1][i]-1])

        self.vertices = np.array(self.vertices, dtype=np.float32)

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])


        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model