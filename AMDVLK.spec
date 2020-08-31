%global debug_package %{nil}

%global amdvlk_version      v-2020.Q3.4

# Keep in basic sync with:
# https://github.com/tomkv/packaging-rpm/blob/master/amdvlk/amdvlk.spec
# https://copr.fedorainfracloud.org/coprs/tkov/amdvlk/package/amdvlk-vulkan-driver/

%global amdvlk_commit       0fad196737d36523c6c2fe18987e64a5716412b6
%global llvm_commit         30cb97a1d0efebb4317f9abeec8d90a5a83d4837
%global llpc_commit         9b5cb15acc8ff789420ed9ed593e35c81303d10c
%global xgl_commit          598c6832a4983f5b75b38a589fca5be80a2f3bb0
%global pal_commit          609b2b8ad982f4f2028cf4411cc2e55fc5e6fcf3
%global spvgen_commit       c054813a9a894e32aaaa04c6717a667c15f60cfd
%global metrohash_commit    712f76fee75d69b23a1ea8f6465752c3ccaaf9a2
%global cwpack_commit       7387247eb9889ddcabbc1053b9c2052e253b088e

%global glslang_commit              b99a6a7273181deeb08859c0fdb0c77c7e8a4500
%global spirv_tools_commit          7a1af5878594cec2992a1bb00565b4c712490239
%global spirv_headers_commit        11d7637e7a43cd88cfd4e42c99581dcb682936aa
%global spirv_cross_commit          6575e451f5bffded6e308988362224dd076b0f2b

%global amdvlk_short_commit %(c=%{amdvlk_commit}; echo ${c:0:7})
%global llvm_short_commit   %(c=%{llvm_commit}; echo ${c:0:7})
%global llpc_short_commit   %(c=%{llpc_commit}; echo ${c:0:7})
%global xgl_short_commit    %(c=%{xgl_commit}; echo ${c:0:7})
%global pal_short_commit    %(c=%{pal_commit}; echo ${c:0:7})
%global spvgen_short_commit %(c=%{spvgen_commit}; echo ${c:0:7})
%global metrohash_short_commit %(c=%{metrohash_commit}; echo ${c:0:7})
%global cwpack_short_commit %(c=%{cwpack_commit}; echo ${c:0:7})
%global glslang_short_commit        %(c=%{glslang_commit}; echo ${c:0:7})
%global spirv_tools_short_commit    %(c=%{spirv_tools_commit}; echo ${c:0:7})
%global spirv_headers_short_commit  %(c=%{spirv_headers_commit}; echo ${c:0:7})
%global spirv_cross_short_commit    %(c=%{spirv_cross_commit}; echo ${c:0:7})
%global commit_date                 20200821
%global gitrel                      .%{commit_date}.git%{amdvlk_short_commit}
%global khronos_url                 https://github.com/KhronosGroup/

Name:          amdvlk-vulkan-driver
Version:       2.155
Release:       1
Summary:       AMD Open Source Driver For Vulkan
License:       MIT
Url:           https://github.com/GPUOpen-Drivers
Source0:       https://github.com/GPUOpen-Drivers/AMDVLK/archive/%{amdvlk_version}/AMDVLK-%{amdvlk_version}.tar.gz
Source1:       %url/llvm-project/archive/%{llvm_commit}.tar.gz/llvm-project-%{llvm_commit}.tar.gz
Source2:       %url/llpc/archive/%{llpc_commit}.tar.gz/llpc-%{llpc_commit}.tar.gz
Source3:       %url/xgl/archive/%{xgl_commit}.tar.gz/xgl-%{xgl_commit}.tar.gz
Source4:       %url/pal/archive/%{pal_commit}.tar.gz/pal-%{pal_commit}.tar.gz
Source5:       %url/spvgen/archive/%{spvgen_commit}.tar.gz/spvgen-%{spvgen_commit}.tar.gz
Source6:       %url/MetroHash/archive/%{metrohash_commit}.tar.gz/MetroHash-%{metrohash_commit}.tar.gz
Source7:       %url/CWPack/archive/%{cwpack_commit}.tar.gz/CWPack-%{cwpack_commit}.tar.gz
Source8:       %khronos_url/glslang/archive/%{glslang_commit}.tar.gz/glslang-%{glslang_commit}.tar.gz
Source9:       %khronos_url/SPIRV-Tools/archive/%{spirv_tools_commit}.tar.gz/SPIRV-Tools-%{spirv_tools_commit}.tar.gz
Source10:      %khronos_url/SPIRV-Headers/archive/%{spirv_headers_commit}.tar.gz/SPIRV-Headers-%{spirv_headers_commit}.tar.gz
Source11:      %khronos_url/SPIRV-Cross/archive/%{spirv_cross_commit}.tar.gz#/SPIRV-Cross-%{spirv_cross_commit}.tar.gz

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
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(openssl)

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
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9 -a 10 -a 11
ln -s AMDVLK-%{amdvlk_version} AMDVLK
ln -s llvm-project-%{llvm_commit} llvm-project
ln -s llpc-%{llpc_commit} llpc
ln -s xgl-%{xgl_commit} xgl
ln -s pal-%{pal_commit} pal
ln -s spvgen-%{spvgen_commit} spvgen
mkdir third_party
ln -s ../MetroHash-%{metrohash_commit} third_party/metrohash
ln -s ../CWPack-%{cwpack_commit} third_party/cwpack

ln -s ../../glslang-%{glslang_commit} spvgen/external/glslang
ln -s ../../SPIRV-Tools-%{spirv_tools_commit} spvgen/external/SPIRV-tools
ln -s ../../SPIRV-Headers-%{spirv_headers_commit} spvgen/external/SPIRV-tools/external/SPIRV-Headers
ln -s ../../SPIRV-Cross-%{spirv_cross_commit} spvgen/external/SPIRV-cross

# workaround for AMDVLK#89, AMDVLK#117
#for i in xgl/icd/CMakeLists.txt llpc/llpc/CMakeLists.txt third_party/metrohash/CMakeLists.txt \
#  llvm-project/llvm/utils/benchmark/CMakeLists.txt llvm-project/llvm/utils/benchmark/test/CMakeLists.txt \
#  pal/src/core/imported/addrlib/CMakeLists.txt pal/src/core/imported/vam/CMakeLists.txt \
#  pal/shared/gpuopen/cmake/AMD.cmake
#do
#	sed -i "s/-Werror/-Wno-error=deprecated -Wno-error=deprecated-copy -Wno-error=redundant-move/g" $i
#done

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

%ninja && ninja spvgen
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

install -m 755 xgl/build/spvgen/spvgen.so %{buildroot}%{_libdir}

%files
%doc AMDVLK/LICENSE.txt AMDVLK/README.md AMDVLK/topLevelArch.png
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
%{_libdir}/amdvlk*.so
%{_libdir}/spvgen.so
