import os
from .time_it import metrics
from .Results import SingleResult

MPEG_PCC_TMC3 = "/home/peter/Documents/uni/pc-compression/mpeg-pcc-tmc13/build/tmc3/tmc3"
TMC3_ENC_OPTIONS = "--mode=0 --inputScale=100  --uncompressedDataPath=INPUT  --compressedStreamPath=OUTPUT"
TMC3_DEC_OPTIONS = "--mode=1 --outputUnitLength=100 --compressedStreamPath=INPUT --reconstructedDataPath=OUTPUT"

def tmc3(path_to_ply: str, output_folder_enc: str, output_folder_dec: str):
    assert path_to_ply.endswith(".ply")
    assert os.path.exists(path_to_ply)
    if not os.path.exists(output_folder_enc):
        os.mkdir(output_folder_enc)
    if not os.path.exists(output_folder_dec):
        os.mkdir(output_folder_dec)

    print(f"Running tmc3 on {path_to_ply = }")
    _, f = path_to_ply.rsplit("/", 1)
    enc_file = os.path.join(output_folder_enc, f.replace(".ply", ".bin"))
    dec_file = os.path.join(output_folder_dec, f.replace(".bin", ".ply"))
    print(f"{enc_file=}\n{dec_file=}")

    @metrics
    def tmc3_enc():
        command = f"{MPEG_PCC_TMC3} {TMC3_ENC_OPTIONS}".replace("INPUT", path_to_ply).replace("OUTPUT", enc_file)
        os.system(command)

    @metrics
    def tmc3_dec():
        command = f"{MPEG_PCC_TMC3} {TMC3_DEC_OPTIONS}".replace("INPUT", enc_file).replace("OUTPUT", dec_file)
        os.system(command)

    duration_enc_ns = tmc3_enc()
    duration_dec_ns = tmc3_dec()
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