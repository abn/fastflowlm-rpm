# FastFlowLM-rpm

Fedora RPM packages for [FastFlowLM](https://github.com/FastFlowLM/FastFlowLM), a high-performance local inference engine designed for AMD Ryzen AI NPU devices.

The source is integrated via git submodule from [FastFlowLM/FastFlowLM](https://github.com/FastFlowLM/FastFlowLM).

## Dependencies

FastFlowLM integrates directly with XRT (Xilinx Runtime) for executing hardware-accelerated LLM inference:
- **Build-Time**: Requires `xrt-devel` (provides headers and libraries in `/opt/xilinx/xrt`).
- **Runtime**: Requires `xrt-base` and `xrt-plugin-amdxdna` (to map instructions to the kernel driver).

## Installation

These packages target Fedora 44+.

```bash
# Enable the Copr repository (substitute your repository name)
sudo dnf copr enable abn/amd-npu

# Install the FastFlowLM runtime
sudo dnf install fastflowlm
```

## Usage

Verify the installation by running a query with a supported model:

```bash
flm --model Gemma-4-E2B-it-GGUF --prompt "Hello NPU"
```

> **Note:** Ensure your host limits are configured for memory locking as described in `xrt-rpm` post-install steps.

## Development

This project uses [tito](https://github.com/rpm-software-management/tito) for versioning and package release management.

### Containerized Builds (Recommended)

To compile the RPM package inside the `quay.io/abn/rpmbuilder:fedora-44` container:

1. **Start the builder container**:
   ```bash
   podman run -d --rm -i --name rpmbuilder-flm \
     -v ${PWD}:/sources:z \
     quay.io/abn/rpmbuilder:fedora-44 sleep inf
   ```

2. **Install local build dependencies**:
   Before building, you must install the locally built `xrt-base` and `xrt-devel` RPM packages inside the container:
   ```bash
   # Copy the built XRT RPMs into the container (assuming xrt-rpm is a peer directory)
   podman cp ../xrt-rpm/output/. rpmbuilder-flm:/tmp/xrt/

   # Install the packages
   podman exec -u 0 rpmbuilder-flm dnf install -y /tmp/xrt/xrt-base-*.rpm /tmp/xrt/xrt-devel-*.rpm
   ```

3. **Run tito build**:
   ```bash
   podman exec rpmbuilder-flm rpmbuilder
   ```

Output RPMs are placed in the container `/output/` folder and can be copied back:
```bash
podman cp rpmbuilder-flm:/output/. ./output/
```

### Tagging a Release

To tag a new version:
```bash
tito tag
```
