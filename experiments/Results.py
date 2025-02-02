from dataclasses import dataclass, asdict
import csv
import os
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

