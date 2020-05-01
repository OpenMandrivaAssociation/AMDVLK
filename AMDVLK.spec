
%global amdvlk_commit       c59322aa302c4378fbca62f0a2f06553d4c01cab
%global llvm_commit         50077fcc15e5844dacd820dcdb02edb23fc00330
%global llpc_commit         9889f54c9a31743b48f3dafcb8ca0c106ed15da4
%global xgl_commit          1f6143fb951622e06fe7b9396957976fc9feddc7
%global pal_commit          8b2381a1d05cd2c9c4e7cc2eeda053e76d8c9a4a
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
Version:       2.140
#Release:       0%{gitrel}%{?dist}
Release:       1
Summary:       AMD Open Source Driver For Vulkan
License:       MIT
Url:           https://github.com/GPUOpen-Drivers
Source0:       https://github.com/GPUOpen-Drivers/AMDVLK/archive/v-2020.Q2.2/%{name}-%{version}.tar.gz
Source1:       %url/llvm-project/archive/%{llvm_commit}.tar.gz#/llvm-project-%{llvm_short_commit}.tar.gz
Source2:       %url/llpc/archive/%{llpc_commit}.tar.gz#/llpc-%{llpc_short_commit}.tar.gz
Source3:       %url/xgl/archive/%{xgl_commit}.tar.gz#/xgl-%{xgl_short_commit}.tar.gz
Source4:       %url/pal/archive/%{pal_commit}.tar.gz#/pal-%{pal_short_commit}.tar.gz
Source5:       %url/spvgen/archive/%{spvgen_commit}.tar.gz#/spvgen-%{spvgen_short_commit}.tar.gz
Source6:       %url/MetroHash/archive/%{metrohash_commit}.tar.gz#/MetroHash-%{metrohash_short_commit}.tar.gz
Source7:       %url/CWPack/archive/%{cwpack_commit}.tar.gz#/CWPack-%{cwpack_short_commit}.tar.gz

#Requires:      vulkan
Requires:      vulkan-loader
Requires:      lib%{_lib}vulkan1

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: make
BuildRequires: python
BuildRequires: perl
BuildRequires: curl
BuildRequires: glibc-devel
BuildRequires: libstdc++-devel
BuildRequires: libxcb-devel
BuildRequires: libX11-devel
BuildRequires: libxshmfence-devel
BuildRequires: libXrandr-devel
BuildRequires: gtest-devel
BuildRequires: wayland-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel

%description
The AMD Open Source Driver for VulkanÂŽ is an open-source Vulkan driver
for Radeonâ˘ graphics adapters on LinuxÂŽ. It is designed to support the
following AMD GPUs:

    Radeonâ˘ HD 7000 Series
    Radeonâ˘ HD 8000M Series
    Radeonâ˘ R5/R7/R9 200/300 Series
    Radeonâ˘ RX 400/500 Series
    Radeonâ˘ M200/M300/M400 Series
    Radeonâ˘ RX Vega Series
    Radeonâ˘ RX 5700 Series
    AMD FireProâ˘ Workstation Wx000/Wx100/Wx300 Series
    Radeonâ˘ Pro WX x100 Series
    Radeonâ˘ Pro 400/500 Series
    Radeonâ˘ W5700/W5500 Series

%prep
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7
ln -s AMDVLK-%{version} AMDVLK
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
  sed -i "s/-Werror/-Wno-error=deprecated -Wno-error=deprecated-copy -Wno-redundant-move/g" $i
done

%build
mkdir -p xgl/build && pushd xgl/build

cmake .. -DCMAKE_AR=`which gcc-ar` \
    -DCMAKE_NM=`which gcc-nm` \
    -DCMAKE_RANLIB=`which gcc-ranlib` \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
    -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_WAYLAND_SUPPORT=ON \
    -DLLVM_ENABLE_WARNINGS=OFF

%make_build
popd

%clean
rm -rf %{buildroot}

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
