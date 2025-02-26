import open3d as o3d
import os
from argparse import ArgumentParser
import numpy as np

def pcd_to_ply(folder: str, file: str):
    assert file.endswith(".pcd")
    pcd = o3d.io.read_point_cloud(os.path.join(folder, file))
    points=np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    p_tensor = o3d.core.Tensor(points, dtype=o3d.core.float32)
    c_tensor = o3d.core.Tensor(colors, dtype=o3d.core.uint8)
    pc = o3d.t.geometry.PointCloud(p_tensor)
    pc.point.colors = c_tensor
    ofile = file.replace(".pcd", "")
    ofile = f"T{ofile}-{points.size}.ply"
    ofile = os.path.join(folder, ofile)
    print(f"writing to {ofile}")
    o3d.t.io.write_point_cloud(ofile, pc)

def scale_scene(ifile: str, ofile: str):
    pcd = o3d.io.read_point_cloud(ifile)
    pcd = pcd.scale(1000, center=pcd.get_center())
    o3d.io.write_point_cloud(ofile, pcd)


def ply_binary_to_ascii(file: str):
    pcd = o3d.io.read_point_cloud(file)
    o3d.t.io.write_point_cloud(file+".ascii", pcd)
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--root", type=str)
    parser.add_argument("--single", type=str)
    parser.add_argument("-o", type=str)
    args = parser.parse_args()
    if not args.single:
        for scene in os.listdir(args.root):
            # scene_root = os.path.join(args.root, scene)
            # for f in os.listdir(scene_root):
                # if not f.endswith(".pcd"):
            if not scene.startswith("T"):
                continue
            # pcd_to_ply(scene_root, f)
            ifile = os.path.join(args.root, scene)
            ofile = os.path.join(args.o, scene)
            print(ifile, ofile)
            scale_scene(ifile, ofile)
    else :
        file = args.single
        ply_binary_to_ascii(file)