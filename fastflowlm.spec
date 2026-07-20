%global debug_package %{nil}

Name:           fastflowlm
Version:        0.9.45
Release:        2%{?dist}
Summary:        FastFlowLM inference runtime for AMD NPU

License:        MIT AND Proprietary
URL:            https://github.com/FastFlowLM/FastFlowLM
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-install-private-libs-to-lib64-flm.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fftw3f)
BuildRequires:  pkgconfig(fftw3l)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  readline-devel
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  libuuid-devel
BuildRequires:  xrt-devel

# FastFlowLM runtime dependencies
Requires:       xrt-npu
Requires:       xrt-plugin-amdxdna
Recommends:     mesa-va-drivers
Suggests:       ffmpeg-libs


%description
FastFlowLM inference runtime for AMD NPU devices.

%prep
%autosetup -p1

%build
# Configure CMake to use the bundled XRT package headers and libraries
%cmake -S FastFlowLM/src -B %{_vpath_builddir} \
    -GNinja \
    -DFLM_VERSION=%{version} \
    -DNPU_VERSION=32.0.203.304 \
    -DXRT_INCLUDE_DIR=/opt/xilinx/xrt/include \
    -DXRT_LIB_DIR=/opt/xilinx/xrt/lib64 \
    -DCMAKE_XCLBIN_PREFIX=%{_datadir}/flm

%cmake_build

%install
%cmake_install

%files
%license FastFlowLM/LICENSE_RUNTIME.txt FastFlowLM/TERMS.md
%doc FastFlowLM/README.md
%{_bindir}/flm
%{_libdir}/flm/
%{_datadir}/flm/

%changelog
* Mon Jul 20 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.45-2
- feat(fastflowlm): upgrade to v0.9.45 (arun.neelicattu@gmail.com)

* Mon Jul 20 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.45-1
- Update to v0.9.45

* Tue Jul 07 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.44-2
- Use patch for CMakeLists instead of dirty submodule

* Tue Jul 07 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.44-1
- Update to v0.9.44

* Sat Jul 04 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.43-3
- Recommend mesa-va-drivers and suggest ffmpeg-libs for dynamic multimedia dependencies

* Wed Jun 03 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.43-2
- Fix runtime search path for xclbins by setting CMAKE_XCLBIN_PREFIX

* Tue Jun 02 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.43-1
- Initial packaging of FastFlowLM
