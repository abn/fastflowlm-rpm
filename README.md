# FastFlowLM-rpm

Fedora RPM packages for [FastFlowLM](https://github.com/FastFlowLM/FastFlowLM), a high-performance local inference engine designed for AMD Ryzen AI NPU devices.

The source is integrated via git submodule from [FastFlowLM/FastFlowLM](https://github.com/FastFlowLM/FastFlowLM).

---

## Backends & Architecture

FastFlowLM-rpm packages two hardware execution backends:

1. **XRT Backend (`fastflowlm-xrt`)**:
   - Uses Xilinx Runtime (`xrt-base`, `xrt-plugin-amdxdna`).
   - Installs `/usr/bin/flm-xrt` with engine libraries isolated under `%{_libdir}/flm/xrt/`.
   - Priority 10 in alternatives.

2. **HRX Backend (`fastflowlm-hrx`)**:
   - Uses Hip Runtime Extended (`libhrx.so` from `hrx`).
   - Installs `/usr/bin/flm-hrx` with engine libraries isolated under `%{_libdir}/flm/hrx/`.
   - Targets the Linux KMQ `amdxdna` driver (`/dev/accel/accel0`).
   - Priority 20 in alternatives.

Both backends can be co-installed on the same system. The common entrypoint `/usr/bin/flm` is managed using Fedora's `update-alternatives` mechanism.

---

## Installation

These packages target Fedora 44+ from the `abn/amd-npu` Copr repository.

```bash
# Enable the Copr repository
sudo dnf copr enable abn/amd-npu

# Install FastFlowLM with the default backend
sudo dnf install fastflowlm

# Or install specific backends
sudo dnf install fastflowlm-hrx
sudo dnf install fastflowlm-xrt
```

---

## Managing Backends (`update-alternatives`)

When both backends are installed, `/usr/bin/flm` points dynamically to the selected backend.

### Check Current Active Backend

```bash
update-alternatives --display flm
```

### Switch to HRX Backend

```bash
sudo update-alternatives --set flm /usr/bin/flm-hrx
```

### Switch to XRT Backend

```bash
sudo update-alternatives --set flm /usr/bin/flm-xrt
```

### Reset to Automatic Mode

In auto mode, the backend with the highest priority (`flm-hrx`, priority 20) is selected:

```bash
sudo update-alternatives --auto flm
```

### Direct Backend Invocation

You can also run either backend directly without altering system-wide alternatives:

```bash
# Run with HRX
flm-hrx serve gemma4-it:e4b

# Run with XRT
flm-xrt serve gemma4-it:e4b
```

---

## Usage

`flm` is the command-line utility for the FastFlowLM inference engine.

```
Usage: flm <command> [options] [model_tag]

Commands:
  run <model_tag>     - Run the model interactively
  serve <model_tag>   - Start the server
  pull <model_tag>    - Download model files if not present
  remove <model_tag>  - Remove a model
  check <model_tag>   - Check a model
  list                - List all available models
  version             - Show version information
  help                - Show this help message
  port                - Show the default server port
  validate            - Validate the NPU stack
```

### Examples

* **Run a model interactively**:
  ```bash
  flm run llama3.2:1b
  ```
* **Run a model with ASR (Automatic Speech Recognition) enabled**:
  ```bash
  flm run llama3.2:1b --asr 1
  ```
* **Serve a model**:
  ```bash
  flm serve gemma4-it:e4b --port 8001
  ```
* **Validate the NPU stack**:
  ```bash
  flm validate
  ```
* **List installed models**:
  ```bash
  flm list --filter installed
  ```

---

## Development & Packaging

This project uses [tito](https://github.com/rpm-software-management/tito) and containerized `rpmbuilder` environments.

### Containerized Builds

To compile the RPM packages inside `quay.io/abn/rpmbuilder:fedora-44`:

```bash
# Start a persistent container with volume mounts
podman run -d --name flm-builder \
  -v ${PWD}:/sources:z \
  -v ${PWD}/output:/output:z \
  quay.io/abn/rpmbuilder:fedora-44 sleep inf

# Run rpmbuilder with the amd-npu copr repository enabled
podman exec -e COPR_REPOS="abn/amd-npu" \
  -e SOURCES=/sources \
  -e OUTPUT=/output \
  -e OUTPUT_USER=$UID \
  flm-builder /bin/rpmbuilder /sources
```

Output RPMs are placed in `./output/`:
- `fastflowlm-<version>-<release>.src.rpm`
- `fastflowlm-<version>-<release>.<arch>.rpm`
- `fastflowlm-xrt-<version>-<release>.<arch>.rpm`
- `fastflowlm-hrx-<version>-<release>.<arch>.rpm`

### Tagging a Release

To tag a new version with Tito:
```bash
tito tag
```
