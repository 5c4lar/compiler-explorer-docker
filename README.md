# compiler-explorer-docker
Deploy compiler explorer locally with docker

## Usage

Config with yaml file following the example in `config/compilers.yaml`.

Start the docker with the following command:
```bash
python3 scripts/run.py --config config/compilers.yaml --stage start
```
Can be stopped with:
```bash
docker stop compiler_explorer   
```