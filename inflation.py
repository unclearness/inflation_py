import cv2
import numpy as np

def depth2orthomesh(depth, x_step=1, y_step=1, scale=[1.0, 1.0, 1.0], minus_depth=True):
    vertices = []
    faces = []
    if len(depth.shape) != 2:
        return None
    h, w = depth.shape
    vertex_id = 0
    added_table = {}
    for y in range(0, h, y_step):
        for x in range(0, w, x_step):
            added_table[(y, x)] = -1
    max_connect_z_diff = 99999.9
    # TODO
    # pixel-wise loop in pure python is toooooooo slow
    for y in range(0, h, y_step):
        for x in range(0, w, x_step):
            d = depth[y, x]
            if d <= 0.000001:
                continue
            if minus_depth:
                d = -d

            vertices.append([x * scale[0], y * scale[1], d * scale[2]])

            added_table[(y, x)] = vertex_id

            current_index = vertex_id
            upper_left_index = added_table[((y - y_step), (x - x_step))]
            upper_index = added_table[((y - y_step), x)]
            left_index = added_table[(y, (x - x_step))]

            upper_left_diff = np.abs(depth[y - y_step, x - x_step] - d)
            upper_diff = np.abs(depth[y - y_step, x] - d)
            left_diff = np.abs(depth[y, x - x_step] - d)

            if upper_left_index > 0 and upper_index > 0\
               and upper_left_diff < max_connect_z_diff\
               and upper_diff < max_connect_z_diff:
                faces.append([upper_left_index, current_index, upper_index])

            if upper_left_index > 0 and left_index > 0\
                and upper_left_diff < max_connect_z_diff\
                    and left_diff < max_connect_z_diff:
                faces.append([upper_left_index, left_index, current_index])

            vertex_id += 1
    return vertices, faces


def _make_ply_txt(vertices, faces, color=[], normal=[]):
    header_lines = ["ply", "format ascii 1.0",
                    "element vertex " + str(len(vertices)),
                    "property float x", "property float y", "property float z"]
    has_normal = len(vertices) == len(normal)
    has_color = len(vertices) == len(color)
    if has_normal:
        header_lines += ["property float nx",
                         "property float ny", "property float nz"]
    if has_color:
        header_lines += ["property uchar red", "property uchar green",
                         "property uchar blue", "property uchar alpha"]
    # no face
    header_lines += ["element face " + str(len(faces)),
                     "property list uchar int vertex_indices", "end_header"]
    header = "\n".join(header_lines) + "\n"

    data_lines = []
    for i in range(len(vertices)):
        line = [vertices[i][0], vertices[i][1], vertices[i][2]]
        if has_normal:
            line += [normal[i][0], normal[i][1], normal[i][2]]
        if has_color:
            line += [int(color[i][0]), int(color[i][1]), int(color[i][2]), 255]
        line_txt = " ".join([str(x) for x in line])
        data_lines.append(line_txt)
    for f in faces:
        line_txt = " ".join(['3'] + [str(int(x)) for x in f])
        data_lines.append(line_txt)

    data_txt = "\n".join(data_lines)

    ply_txt = header + data_txt

    return ply_txt


def writeMeshAsPly(path, vertices, faces):
    with open(path, 'w') as f:
        txt = _make_ply_txt(vertices, faces)
        f.write(txt)


def inflationByDistanceTransform(mask, activation_func=None):
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    depth = dist
    if activation_func is None:
        return depth
    activated_depth = depth.copy()
    h, w = depth.shape
    for j in range(h):
        for i in range(w):
            #print(d, activation_func(d))
            activated_depth[j, i] = activation_func(depth[j, i])
    return activated_depth


def activation_tanh(factor):
    return lambda x: np.tanh(x * factor) / factor


if __name__ == '__main__':
    names = ['A', 'circle', 'hiragana', 'square', 's']

    for name in names:
        mask_path = './data/' + name + '.png'
        print(mask_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask[mask > 100] = 255
        mask[mask <= 100] = 0
        depth = inflationByDistanceTransform(mask)
        vertices, faces = depth2orthomesh(depth)
        writeMeshAsPly(name + '_dist.ply', vertices, faces)
        depth = inflationByDistanceTransform(mask, activation_tanh(0.02))
        vertices, faces = depth2orthomesh(depth)
        writeMeshAsPly(name + '_dist_tanh.ply', vertices, faces)
