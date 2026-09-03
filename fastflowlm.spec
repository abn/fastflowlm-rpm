%global debug_package %{nil}

Name:           fastflowlm
Version:        1.0.4
Release:        2%{?dist}
Summary:        FastFlowLM inference runtime for AMD NPU

License:        MIT AND Proprietary
URL:            https://github.com/FastFlowLM/FastFlowLM
Source0:        %{name}-%{version}.tar.gz
Patch0:         0001-install-private-libs-to-lib64-flm.patch
Patch1:         0002-hrx-lm-config-abi-compat.patch
Patch2:         0003-hrx-amdxdna-buffer-alloc.patch

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
BuildRequires:  hrx-devel
BuildRequires:  patchelf

# FastFlowLM runtime dependencies
Requires:       (fastflowlm-xrt or fastflowlm-hrx)
Recommends:     fastflowlm-xrt
Suggests:       fastflowlm-hrx
Recommends:     mesa-va-drivers
Suggests:       ffmpeg-libs

%description
FastFlowLM inference runtime for AMD NPU devices.

%package xrt
Summary:        FastFlowLM inference runtime for AMD NPU (XRT backend)
Requires:       %{name} = %{version}-%{release}
Requires:       xrt-npu
Requires:       xrt-plugin-amdxdna
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:       %{name}-backend = %{version}-%{release}

%description xrt
FastFlowLM backend using Xilinx Run Time (XRT) for AMD NPU devices.

%package hrx
Summary:        FastFlowLM inference runtime for AMD NPU (HRX backend)
Requires:       %{name} = %{version}-%{release}
Requires:       hrx
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:       %{name}-backend = %{version}-%{release}

%description hrx
FastFlowLM backend using Hip Runtime Extended (HRX) for AMD NPU devices.

%prep
%autosetup -p1

%build
# Build XRT backend
%define _vpath_builddir build-xrt
%cmake -S FastFlowLM/src \
    -GNinja \
    -DFLM_VERSION=%{version} \
    -DNPU_VERSION=32.0.203.304 \
    -DXRT_INCLUDE_DIR=/opt/xilinx/xrt/include \
    -DXRT_LIB_DIR=/opt/xilinx/xrt/lib64 \
    -DCMAKE_XCLBIN_PREFIX=%{_datadir}/flm \
    -DFLM_USE_HRX=OFF \
    -DFLM_BIN_NAME=flm-xrt
%cmake_build

# Build HRX backend
%define _vpath_builddir build-hrx
%cmake -S FastFlowLM/src \
    -GNinja \
    -DFLM_VERSION=%{version} \
    -DNPU_VERSION=32.0.203.304 \
    -DCMAKE_XCLBIN_PREFIX=%{_datadir}/flm \
    -DFLM_USE_HRX=ON \
    -DFLM_SYSTEM_HRX=ON \
    -DFLM_BIN_NAME=flm-hrx
%cmake_build

%install
# Install XRT backend
%define _vpath_builddir build-xrt
%cmake_install

# Install HRX backend
%define _vpath_builddir build-hrx
%cmake_install

# Ghost file for alternatives link
mkdir -p %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/flm

%post xrt
%{_sbindir}/update-alternatives --install %{_bindir}/flm flm %{_bindir}/flm-xrt 10

%postun xrt
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove flm %{_bindir}/flm-xrt
fi

%post hrx
%{_sbindir}/update-alternatives --install %{_bindir}/flm flm %{_bindir}/flm-hrx 20

%postun hrx
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove flm %{_bindir}/flm-hrx
fi

%files
%license FastFlowLM/LICENSE_RUNTIME.txt FastFlowLM/TERMS.md
%doc FastFlowLM/README.md
%dir %{_libdir}/flm
%{_datadir}/flm/

%files xrt
%{_bindir}/flm-xrt
%{_libdir}/flm/xrt/
%ghost %{_bindir}/flm

%files hrx
%{_bindir}/flm-hrx
%{_libdir}/flm/hrx/
%ghost %{_bindir}/flm


%changelog
* Wed Sep 02 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.4-1
- Update to v1.0.4 (arun.neelicattu@gmail.com)

* Wed Sep 02 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.4-1
- Update to v1.0.4

* Sun Aug 23 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.2-1
- Update to v1.0.2 (arun.neelicattu@gmail.com)

* Sat Aug 22 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.2-1
- Update to v1.0.2

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-3
- Fix CMake patch for FastFlowLM v1.0.0 (arun.neelicattu@gmail.com)

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-3
- Fix CMake patch for FastFlowLM v1.0.0

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-2
- 

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-2
- Fix CMake patch for FastFlowLM v1.0.0

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-1
- 

* Tue Aug 11 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 1.0.0-1
- Update to v1.0.0

* Sat Aug 01 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.46-1
- feat(fastflowlm): upgrade to v0.9.46 (arun.neelicattu@gmail.com)

* Sat Aug 01 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.9.46-1
- Update to v0.9.46

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
