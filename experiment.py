from argparse import ArgumentParser
import os
from time_it import metrics
from dataclasses import dataclass, asdict
import csv

DRACO_ENC = "encoders/draco_encoder"
DRACO_DEC = "decoders/draco_decoder"
DRACO_ENC_OPTIONS = "-qp 11 -qt 10 -qn 8 -qg 8 -cl 7"  # default values

@dataclass
class SingleResult:
    file: str
    bpp: float
    time_enc_ns: int
    time_dec_ns: int
    enc_file_size_bits: int
    num_points: int

    def __init__(
        self,
        file: str,
        bpp: float,
        time_enc_ns: int,
        time_dec_ns: int,
        enc_file_size_bits: int,
        num_points: int,
    ):
        self.file = file
        self.bpp = bpp
        self.time_enc_ns = time_enc_ns
        self.time_dec_ns = time_dec_ns
        self.enc_file_size_bits = enc_file_size_bits
        self.num_points = num_points


@dataclass
class AlgorithmResults:
    algorithm: str
    dataset: str
    singleResults: list[SingleResult]

    def __init__(self, algorithm: str, dataset: str):
        assert algorithm != ""
        assert dataset != ""
        self.algorithm = algorithm
        self.dataset = dataset
        self.singleResults = []

    def to_csv(self, folder: str):
        assert os.path.exists(folder)
        assert len(self.singleResults) > 0
        file = f"{self.algorithm}-{self.dataset}.csv"
        path = os.path.join(folder, file)
        fieldnames = {
            "file",
            "bpp",
            "time_enc_ns",
            "time_dec_ns",
            "enc_file_size_bits",
            "num_points",
        }
        with open(path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for single_result in self.singleResults:
                writer.writerow(asdict(single_result))


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
    print(f"{enc_file=}, {dec_file=}")

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
        time_enc_ns=duration_enc_ns,
        time_dec_ns=duration_dec_ns,
        enc_file_size_bits=enc_size,
        num_points=num_points,
    )


def prepare_folders(base: str, algorithm_name: str) -> tuple[str, str, str]:
    algorithm_base_folder = os.path.join(base, algorithm_name)
    if not os.path.exists(algorithm_base_folder):
        os.mkdir(algorithm_base_folder)
    output_enc = os.path.join(algorithm_base_folder, "encoded")
    output_dec = os.path.join(algorithm_base_folder, "decoded")
    metric_dir = os.path.join(algorithm_base_folder, "metrics")
    if not os.path.exists(output_enc):
        os.mkdir(output_enc)
    if not os.path.exists(output_dec):
        os.mkdir(output_dec)
    if not os.path.exists(metric_dir):
        os.mkdir(metric_dir)
    return output_enc, output_dec, metric_dir


ALGORITHMS = {"draco": draco}


def main(
    folder: str,
):
    assert os.path.exists(folder)
    dataset_name = folder.rsplit("/", 1)[-1]
    plys = sorted(
        [
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if file.endswith(".ply")
        ],
        key=lambda x: int(x.rsplit("/", 1)[1].split("-")[0][1:]),
    )
    for algorithm_name, algorithm_func in ALGORITHMS.items():
        output_enc, output_dec, metric_dir = prepare_folders(
            base=folder, algorithm_name=algorithm_name
        )
        metrics = AlgorithmResults(algorithm=algorithm_name, dataset=dataset_name)
        for ply in plys:
            metrics.singleResults.append(
                algorithm_func(
                    path_to_ply=ply,
                    output_folder_enc=output_enc,
                    output_folder_dec=output_dec,
                )
            )
        metrics.to_csv(metric_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--folder", help="path to dataset folder, e.g. auditorium")
    args = parser.parse_args()
    print(f"{args.folder=}")

    main(folder=args.folder)
