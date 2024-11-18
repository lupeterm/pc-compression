import open3d as o3d
import numpy as np

PLY_PREFIX = """
ply
format ascii 1.0
element vertex NUMPOINTS
property float x
property float y
property float z
end_header
"""


def open3d_pc_to_float_ply(pcd: o3d.geometry.PointCloud, oFile: str):
    points = np.asarray(pcd.points).astype(np.float32)
    normals = np.asarray(pcd.normals).astype(np.float32)
    header = PLY_PREFIX.replace("NUMPOINTS", str(len(points)))
    np.savetxt(
        fname=oFile,
        X=np.concatenate((points, normals), axis=1),
        header=header,
        delimiter=" ",
        comments="",
    )


def open3d_pc_to_obj(pcd: o3d.geometry.PointCloud, oFile: str):
    radii = [0.005, 0.01, 0.02, 0.04]
    # slow asf
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii)
    )
    vertices = np.asarray(mesh.vertices)
    normals = np.asarray(mesh.vertex_normals)
    print(vertices.shape, normals.shape)
    if not oFile.endswith(".obj"):
        oFile = oFile.split(".")[0] + ".obj"
    with open(oFile, "w") as f:
        for vertex, normal in zip(vertices, normals):
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            f.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")


if __name__ == "__main__":
    demo_crop_data = o3d.data.DemoCropPointCloud()
    pcd = o3d.geometry.PointCloud()
    pcd = o3d.io.read_point_cloud(demo_crop_data.point_cloud_path)
    o3d.io.write_point_cloud("withnormals.ply", pcd, write_ascii=True)

    open3d_pc_to_float_ply(pcd, "test.ply")
    open3d_pc_to_obj(pcd, "test.obj")
