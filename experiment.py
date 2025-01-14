from argparse import ArgumentParser, Namespace
import inspect
import sys
import json
from dataclasses import dataclass
from pprint import pprint
from enum import Enum
import os
import datetime
from collections.abc import Callable

class CloudCompressionConfigMode(Enum):
    BAG = 1
    TXT = 2
    PCD = 3


@dataclass
class CloudCompressionConfig:
    algorithms: list[str]
    scenes: list[str]
    scene_root: str  # path to dataset root
    destination_root: str  # path to result root: root -> <datetime> -> scene -> algo
    mode: CloudCompressionConfigMode

    @staticmethod
    def from_json(path: str) -> "CloudCompressionConfig":
        with open(path, "r") as json_file:
            json_obj = json.loads(json_file.read())
            return CloudCompressionConfig(
                algorithms=json_obj["algorithms"], 
                scenes=json_obj["scenes"], 
                scene_root=json_obj["scene_root"], 
                destination_root=json_obj["destination_root"], 
                mode=CloudCompressionConfigMode(json_obj["mode"])
            )

class AlgorithmBase:
    def __init__(self,config: CloudCompressionConfig) -> None:
        self.config = config

    def __call__(self, algorithm: str):
        assert isinstance(algorithm, str), f"algorithm, is of {type(algorithm)}"
        if not hasattr(self, algorithm):
            raise NotImplementedError(f"Passed algorithm '{algorithm}' has not been implemented yet.")
        assert callable(self.__getattribute__(algorithm)), f"Passed algorithm '{algorithm}' is not callable"
        return self.__getattribute__(algorithm)()
    
    def _create_results_dir(self, algo: str):
        if not os.path.exists(algo):
                os.mkdir(algo)
        dir_name = datetime.datetime.now()
        print(f"Creating {os.getcwd()}/{algo}/{dir_name}")
        os.mkdir(os.path.join(algo, f"{dir_name}"))

    def _process_txt(self, callable_enc: Callable | str, callable_dec: Callable | str):
        assert list(filter(lambda s: s.endswith(".txt"), os.listdir())), f"No processable .txt files found in {os.getcwd}."
        if isinstance(callable_enc, str) and os.path.exists(callable_enc):
            print(f"Executable encoder binary at {callable_enc} found.")
        if isinstance(callable_dec, str) and os.path.exists(callable_dec):
            print(f"Executable decoder binary at {callable_dec} found.")
        print("Start Processing .txt files.")
        txtfiles = sorted([f for f in os.listdir() if f.endswith('.txt')])
        for file in os
        command = f'{callable_enc} {} {result_file}'
        os.system(command)



    def draco(self) -> None: 
        print(f"Using Algorithm 'draco'")
        for scene in self.config.scenes:
            print(f"Processing {scene=}")
            print(f"chdir'ing to {self.config.scene_root}/{scene}")
            os.chdir(os.path.join(self.config.scene_root, scene))
            self._create_results_dir("DRACO")
            draco_funcs = self.config.algorithms["draco"]
            if self.config.mode == CloudCompressionConfigMode.TXT:
                self._process_txt(callable_enc=draco_funcs["encoder"], callable_dec=draco_funcs["decoder"])
            elif self.config.mode == CloudCompressionConfigMode.PCD:
                ...
            else:
                ...

        
def main(config: CloudCompressionConfig):
    algorithm_base = AlgorithmBase(config=config)
    for algorithm in config.algorithms:
        print(algorithm)
        algorithm_base(algorithm=algorithm)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-c", "--config", help="Path to config.json file.", required=True, type=str)
    args = parser.parse_args()
    print(f"Reading configuration at {args.config}")
    config = CloudCompressionConfig.from_json(args.config)
    pprint(config)
    main(config=config)