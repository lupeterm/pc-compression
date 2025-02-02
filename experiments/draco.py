import os
from .time_it import metrics
from .Results import SingleResult

DRACO_ENC = "/home/peter/Documents/uni/pc-compression/encoders/draco_encoder"
DRACO_DEC = "/home/peter/Documents/uni/pc-compression/decoders/draco_decoder"
DRACO_ENC_OPTIONS = "-qp 11 -qt 10 -qn 8 -qg 8 -cl 7"  # default values

def draco(path_to_ply: str, output_folder_enc: str, output_folder_dec: str):
    assert path_to_ply.endswith(".ply")
    assert os.path.exists(path_to_ply)
    if not os.path.exists(output_folder_enc):
        os.mkdir(output_folder_enc)
    if not os.path.exists(output_folder_dec):
        os.mkdir(output_folder_dec)

    print(f"Running draco on {path_to_ply = }")
    _, f = path_to_ply.rsplit("/", 1)
    enc_file = os.path.join(output_folder_enc, f.replace(".ply", ".drc"))
    dec_file = os.path.join(output_folder_dec, f.replace(".drc", ".ply"))
    print(f"{enc_file=}\n{dec_file=}")

    @metrics
    def draco_enc():
        command = f"{DRACO_ENC} -i {path_to_ply} -o {enc_file} {DRACO_ENC_OPTIONS}"
        os.system(command)

    @metrics
    def draco_dec():
        command = f"{DRACO_DEC} -i {enc_file} -o {dec_file}"
        os.system(command)

    duration_enc_ns = draco_enc()
    duration_dec_ns = draco_dec()
    enc_size = os.path.getsize(enc_file) * 8
    num_points = int(f.replace(".ply", "").rsplit("-")[1])
    bpp = enc_size / num_points
    print(f"{bpp =}")
    return SingleResult(
        file=f,
        bpp=bpp,
        time_enc_ns=duration_enc_ns, # type: ignore
        time_dec_ns=duration_dec_ns, # type: ignore
        enc_file_size_bits=enc_size,
        num_points=num_points,
    )