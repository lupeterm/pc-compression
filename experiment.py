from argparse import ArgumentParser
import os
from experiments.draco import draco
from experiments.pccomp import pccomp
from experiments.Results import AlgorithmResults


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


ALGORITHMS = {"draco": draco, "pccomp": pccomp}


def main(
    folder: str,
    algorithm: str | None = None
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
        if algorithm and not algorithm_name == algorithm:
            continue
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
    parser.add_argument("-a", "--algorithm", help="name of algorithm")
    
    args = parser.parse_args()
    print(f"{args.folder=}")

    main(folder=args.folder, algorithm=args.algorithm)
