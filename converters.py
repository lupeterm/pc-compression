import open3d as o3d
import os
from argparse import ArgumentParser


def pcd_to_ply(file: str):
    assert file.endswith(".pcd")
    pcd = o3d.io.read_point_cloud(file)
    ofile = file.replace(".pcd", ".ply")
    print(f"writing to {ofile}")
    o3d.io.write_point_cloud(ofile, pcd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--root", type=str)
    args = parser.parse_args()
    for scene in os.listdir(args.root):
        scene_root = os.path.join(args.root, scene)
        for f in os.listdir(scene_root):
            if not f.endswith(".pcd"):
                continue
            pcd_to_ply(os.path.join(scene_root, f))
