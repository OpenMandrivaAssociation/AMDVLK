%global amdvlk_version      v-2020.Q2.3

%global amdvlk_commit       c59322aa302c4378fbca62f0a2f06553d4c01cab
%global llvm_commit         53692d985a53a336e07907c2d4b86bf2deb66908
%global llpc_commit         61b5d58e8891dc37e473064d429f0496d5254e52
%global xgl_commit          877b773000248dffa025c42d9c4074d1a07b9e47
%global pal_commit          a83f67db9f0d2f16bbc698aeefa9c5e9476c993a
%global spvgen_commit       a223c8636f8306697f6fdc86f742b99fbd8c5dbd
%global metrohash_commit    2b6fee002db6cc92345b02aeee963ebaaf4c0e2f
%global cwpack_commit       b601c88aeca7a7b08becb3d32709de383c8ee428
%global amdvlk_short_commit %(c=%{amdvlk_commit}; echo ${c:0:7})
%global llvm_short_commit   %(c=%{llvm_commit}; echo ${c:0:7})
%global llpc_short_commit   %(c=%{llpc_commit}; echo ${c:0:7})
%global xgl_short_commit    %(c=%{xgl_commit}; echo ${c:0:7})
%global pal_short_commit    %(c=%{pal_commit}; echo ${c:0:7})
%global spvgen_short_commit %(c=%{spvgen_commit}; echo ${c:0:7})
%global metrohash_short_commit %(c=%{metrohash_commit}; echo ${c:0:7})
%global cwpack_short_commit %(c=%{cwpack_commit}; echo ${c:0:7})
%global commit_date         20200416
%global gitrel              .%{commit_date}.git%{amdvlk_short_commit}

Name:          amdvlk-vulkan-driver
Version:       2.145
Release:       1
Summary:       AMD Open Source Driver For Vulkan
License:       MIT
Url:           https://github.com/GPUOpen-Drivers
Source0:       https://github.com/GPUOpen-Drivers/AMDVLK/archive/v-2020.Q2.2/AMDVLK-%{amdvlk_version}.tar.gz
Source1:       %url/llvm-project/archive/%{llvm_commit}.tar.gz/llvm-project-%{llvm_commit}.tar.gz
Source2:       %url/llpc/archive/%{llpc_commit}.tar.gz/llpc-%{llpc_commit}.tar.gz
Source3:       %url/xgl/archive/%{xgl_commit}.tar.gz/xgl-%{xgl_commit}.tar.gz
Source4:       %url/pal/archive/%{pal_commit}.tar.gz/pal-%{pal_commit}.tar.gz
Source5:       %url/spvgen/archive/%{spvgen_commit}.tar.gz/spvgen-%{spvgen_commit}.tar.gz
Source6:       %url/MetroHash/archive/%{metrohash_commit}.tar.gz/MetroHash-%{metrohash_commit}.tar.gz
Source7:       %url/CWPack/archive/%{cwpack_commit}.tar.gz/CWPack-%{cwpack_commit}.tar.gz

Provides:	amdvlk
Requires:	vulkan-loader
Requires:	%{_lib}vulkan1

BuildRequires: llvm
BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: python
BuildRequires: perl
BuildRequires: curl
BuildRequires: glibc-devel
BuildRequires: libstdc++-devel
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(xrandr)
BuildRequires: gtest-devel
BuildRequires: wayland-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel

%description
The AMD Open Source Driver for Vulkan is an open-source Vulkan driver
for Radeon graphics adapters on Linux. It is designed to support the
following AMD GPUs:

    Radeon HD 7000 Series
    Radeon HD 8000M Series
    Radeon R5/R7/R9 200/300 Series
    Radeon RX 400/500 Series
    Radeon M200/M300/M400 Series
    Radeon RX Vega Series
    Radeon RX 5700 Series
    AMD FirePro Workstation Wx000/Wx100/Wx300 Series
    Radeon Pro WX x100 Series
    Radeon Pro 400/500 Series
    Radeon W5700/W5500 Series

%prep
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7
ln -s AMDVLK-%{amdvlk_version} AMDVLK
ln -s llvm-project-%{llvm_commit} llvm-project
ln -s llpc-%{llpc_commit} llpc
ln -s xgl-%{xgl_commit} xgl
ln -s pal-%{pal_commit} pal
ln -s spvgen-%{spvgen_commit} spvgen
mkdir third_party
ln -s ../MetroHash-%{metrohash_commit} third_party/metrohash
ln -s ../CWPack-%{cwpack_commit} third_party/cwpack

# workaround for AMDVLK#89, AMDVLK#117
for i in xgl/icd/CMakeLists.txt llpc/llpc/CMakeLists.txt third_party/metrohash/CMakeLists.txt \
  llvm-project/llvm/utils/benchmark/CMakeLists.txt llvm-project/llvm/utils/benchmark/test/CMakeLists.txt \
  pal/src/core/imported/addrlib/CMakeLists.txt pal/src/core/imported/vam/CMakeLists.txt \
  pal/shared/gpuopen/cmake/AMD.cmake
do
	sed -i "s/-Werror/-Wno-error=deprecated -Wno-error=deprecated-copy -Wno-error=redundant-move/g" $i
done

%build
mkdir -p xgl/build && pushd xgl/build

cmake .. \
	-DCMAKE_AR=`which llvm-ar` \
	-DCMAKE_NM=`which llvm-nm` \
	-DCMAKE_RANLIB=`which llvm-ranlib` \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
	-DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_WAYLAND_SUPPORT=ON \
	-DLLVM_ENABLE_WARNINGS=OFF \
	-G Ninja

%ninja_build
popd

%install
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d
mkdir -p %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_sysconfdir}/amd
echo "MaxNumCmdStreamsPerSubmit,4" > %{buildroot}%{_sysconfdir}/amd/amdPalSettings.cfg

%if 0%{?__isa_bits} == 64
    install -m 644 AMDVLK/json/Redhat/amd_icd64.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
    install -m 755 xgl/build/icd/amdvlk64.so %{buildroot}%{_libdir}
%else
    install -m 644 AMDVLK/json/Redhat/amd_icd32.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
    install -m 755 xgl/build/icd/amdvlk32.so %{buildroot}%{_libdir}
%endif

%files
%doc AMDVLK/LICENSE.txt AMDVLK/README.md AMDVLK/topLevelArch.png
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
%{_libdir}/amdvlk*.so
