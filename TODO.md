# Overview
I want to get openpilot running
* [Setup instructions](https://github.com/commaai/openpilot/blob/master/tools/README.md)
* [Build and run unit tests](https://github.com/commaai/openpilot/blob/master/docs/WORKFLOW.md)
* [openpilot in simulator](https://github.com/commaai/openpilot/blob/master/tools/sim/README.md)

I want to complete this bounty:
* [Get MetaDrive simulator working on macOS](https://github.com/commaai/openpilot/issues/33207)

## To-do:
[x] clone openpilot
~~[x] create flox environment~~ Use devcontainer instead, support already exists
~~[ ] examine `openpilot/tools/install_ubuntu_dependencies.sh` and `flox install` fedora equivalents~~
~~[ ] examine `openpilot/tools/install_python_dependencies.sh` and `flox install` (?) equivalents~~
[x] build from source
[x] run unit tests
[x] run simulator stack
    [x] run openpilot simulator
    [x] run metadrive simulator (pyproject.toml skips install on aarch64. seems like support is limited, but github issues implies it should work)
        ~~[ ] clone metadrive simulator standalone, try to run~~
        [x] modify openpilot (pyproject.toml, run script, etc.) as needed to use aarch64 build of metadrive
[ ] try to reproduce on macOS
[ ] check out the "CTF" (capture the flag) [here](https://github.com/commaai/openpilot/blob/master/tools/CTF.md)

## Usage
1. Launch the devcontainer
    ```bash
    cd ~/projects/openpilot-docker/openpilot
    sudo devcontainer up --workspace-folder .
    ```
2. Determine docker container name
    ```bash
    sudo docker ps
    ```
3. Exec a shell in the container
    ```bash
    sudo docker exec -it <container_name> bash
    ```
4. Navigate to openpilot workspace
    ```bash
    cd /workspaces/openpilot
    ```
5. Source python environment
    ```bash
    source ./venv/bin/activate
    ```
6. Run openpilot (see linked READMEs at the top)

## Notes
Some issues I ran into when getting up and running

* devcontainer uses `batman` user and is assigned UID 1001. If your host user does not have UID
1001 then you run into permission issues when trying to edit files mounted to the container from
the host. See `openpilot/Dockerfile.openpilot_base` for an argument where it sets the user's UID
to 1001. Short-term, reset your user's UID to 1001. Long-term, update this dockerfile so that the
devcontainer will instead just map to your existing user's UID.

* Install the following dependencies not included in openpilot pyproject.toml via `uv pip install`
    * metadrive-simulator @ openpilot custom version
    * pyopencl==2024.1
   ~~* siphash24~~ siphash24 only needed to silence a warning
* Install the following via `apt-get install`
    * pocl-opencl-icd

* Something seems to be wrong with the version of pyopencl we are using and the underlying `pyopencl.cl.Kernel` (does this come from pocl-opencl-icd?)
    ```
    prg_b.rgb_to_nv12
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/workspaces/openpilot/.venv/lib/python3.12/site-packages/pyopencl/__init__.py", line 443, in __getattr__
        knl = Kernel(self, attr)
              ^^^^^^^^^^^^^^^^^^
    TypeError: __init__(): incompatible function arguments. The following argument types are supported:
        1. __init__(self, arg0: pyopencl._cl._Program, arg1: str, /) -> None

    Invoked with types: pyopencl._cl.Kernel, pyopencl.Program, str
    ```

    ```
    print(inspect.getsource(cl.Kernel.__init__))
    def kernel_init(self, prg, name):
        if not isinstance(prg, _cl._Program):
            prg = prg._get_prg()

        kernel_old_init(self, prg, name)

        self._setup(prg)
    ```
    * Next steps:
        * Try uninstalling pocl-opencl-icd (or just restarting the devcontainer) and see if the reproducer script gives the same result
        * Try installing an older version of pyopencl
        * Figure out how to install a version of pyopencl.cl.Kernel that is compatible with the version of pyopencl I am using
        * Do more research to see if there is a devcontainer or dockerfile with this pocl stuff already figured out

