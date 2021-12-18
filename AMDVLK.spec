#global debug_package %{nil}
%define _empty_manifest_terminate_build 0

%global amdvlk_version	  v-%{version}
%global amdvlk_core_version	  2.192

# Keep in basic sync with:
# https://github.com/tomkv/packaging-rpm/blob/master/amdvlk/amdvlk.spec
# https://copr.fedorainfracloud.org/coprs/tkov/amdvlk/package/amdvlk-vulkan-driver/

%global amdvlk_commit		8d70d12b7b3887622dddca01ae2d8f0312876d98
%global llvm_commit		63581e1504f3854df7d1ea7aab6af935da1b515d
%global llpc_commit		80b124752f5f689b21d46a3fd459b2df659de187
%global xgl_commit		da1a583a51c69c115f9144b68ec2bdf5b6519056
%global pal_commit		61409c1cea19a2ca5ad00461b1e75b3ab46c4389
%global spvgen_commit		0aa19873514a8272dfdc5cb8861859a52f5de503
%global metrohash_commit	3c566dd9cda44ca7fd97659e0b53ac953f9037d2
%global cwpack_commit		39f8940199e60c44d4211cf8165dfd12876316fa

%global glslang_commit		b9ba4c5743997abbc0df858f2458a86d62af6a25
%global spirv_tools_commit	4578db3c419a9300485155fd8b81f6b1d822b5fb
%global spirv_headers_commit	19e8350415ed9516c8afffa19ae2c58559495a67
%global spirv_cross_commit	e4243b898ca5e1e19e48725a991ada1e5744691c

%global amdvlk_short_commit	%(c=%{amdvlk_commit}; echo ${c:0:7})
%global llvm_short_commit	%(c=%{llvm_commit}; echo ${c:0:7})
%global llpc_short_commit	%(c=%{llpc_commit}; echo ${c:0:7})
%global xgl_short_commit	%(c=%{xgl_commit}; echo ${c:0:7})
%global pal_short_commit	%(c=%{pal_commit}; echo ${c:0:7})
%global spvgen_short_commit	%(c=%{spvgen_commit}; echo ${c:0:7})
%global metrohash_short_commit	%(c=%{metrohash_commit}; echo ${c:0:7})
%global cwpack_short_commit	%(c=%{cwpack_commit}; echo ${c:0:7})
%global glslang_short_commit	%(c=%{glslang_commit}; echo ${c:0:7})
%global spirv_tools_short_commit	%(c=%{spirv_tools_commit}; echo ${c:0:7})
%global spirv_headers_short_commit	%(c=%{spirv_headers_commit}; echo ${c:0:7})
%global spirv_cross_short_commit	%(c=%{spirv_cross_commit}; echo ${c:0:7})
%global commit_date		20210722
%global gitrel			.%{commit_date}.git%{amdvlk_short_commit}
%global khronos_url		https://github.com/KhronosGroup/

%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

Name:		amdvlk-vulkan-driver
Version:	2021.Q4.2
Release:	1
Summary:	AMD Open Source Driver For Vulkan
License:	MIT
Url:		https://github.com/GPUOpen-Drivers
Source0:	https://github.com/GPUOpen-Drivers/AMDVLK/archive/%{amdvlk_version}/AMDVLK-%{amdvlk_version}.tar.gz
Source1:	%url/llvm-project/archive/%{llvm_commit}/llvm-project-%{llvm_commit}.tar.gz
Source2:	%url/llpc/archive/%{llpc_commit}/llpc-%{llpc_commit}.tar.gz
Source3:	%url/xgl/archive/%{xgl_commit}/xgl-%{xgl_commit}.tar.gz
Source4:	%url/pal/archive/%{pal_commit}/pal-%{pal_commit}.tar.gz
Source5:	%url/spvgen/archive/%{spvgen_commit}/spvgen-%{spvgen_commit}.tar.gz
Source6:	%url/MetroHash/archive/%{metrohash_commit}/MetroHash-%{metrohash_commit}.tar.gz
Source7:	%url/CWPack/archive/%{cwpack_commit}/CWPack-%{cwpack_commit}.tar.gz
Source8:	%khronos_url/glslang/archive/%{glslang_commit}/glslang-%{glslang_commit}.tar.gz
Source9:	%khronos_url/SPIRV-Tools/archive/%{spirv_tools_commit}/SPIRV-Tools-%{spirv_tools_commit}.tar.gz
Source10:	%khronos_url/SPIRV-Headers/archive/%{spirv_headers_commit}/SPIRV-Headers-%{spirv_headers_commit}.tar.gz
Source11:	%khronos_url/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz

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

	Radeon RX 400/500 Series
	Radeon RX Vega Series
	Radeon RX 5000 Series
	Radeon RX 6000 Series
	Radeon Pro WX 9100, x200 Series
	Radeon Pro W5700/W5500 Series

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

cd pal
%autopatch -p1
cd ..

%build
%if %{with compat32}
export CMAKE_BUILD_DIR32=xgl/build32
export CFLAGS="%{optflags} -fno-lto -m32 -DNDEBUG"
export CXXFLAGS="%{optflags} -fno-lto -m32 -DNDEBUG"
%cmake32 \
	-DCMAKE_AR=`which llvm-ar` \
	-DCMAKE_NM=`which llvm-nm` \
	-DCMAKE_RANLIB=`which llvm-ranlib` \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_C_FLAGS_RELEASE="%{optflags} -O3 -fno-lto -m32 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -O3 -fno-lto -m32 -DNDEBUG" \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_WAYLAND_SUPPORT=ON \
	-DLLVM_ENABLE_WARNINGS=OFF \
	-G Ninja
%ninja_build && %ninja_build spvgen
cd -
unset CFLAGS
unset CXXFLAGS
%endif

mkdir -p xgl/build && pushd xgl/build

# Using full optimizations breaks 32-bit platforms'
# memory allocation limits -- optimize less there
cmake .. \
	-DCMAKE_AR=`which llvm-ar` \
	-DCMAKE_NM=`which llvm-nm` \
	-DCMAKE_RANLIB=`which llvm-ranlib` \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
%ifarch %{ix86} %{arm}
	-DCMAKE_C_FLAGS_RELEASE="-O2 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="-O2 -DNDEBUG" \
%else
	-DCMAKE_C_FLAGS_RELEASE="%{optflags} -O3 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -O3 -DNDEBUG" \
%endif
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
#mkdir -p %{buildroot}%{_datadir}/vulkan/implicit_layer.d
mkdir -p %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_sysconfdir}/amd
echo "MaxNumCmdStreamsPerSubmit,4" > %{buildroot}%{_sysconfdir}/amd/amdPalSettings.cfg

%if 0%{?__isa_bits} == 64
#	install -m 644 AMDVLK/json/Redhat/amd_icd64.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
#	install -m 644 AMDVLK/json/Redhat/amd_icd64.json %{buildroot}%{_datadir}/vulkan/implicit_layer.d/amd_icd.%{_arch}.json
	install -m 644 xgl/build/icd/amd_icd64.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
	install -m 755 xgl/build/icd/amdvlk64.so %{buildroot}%{_libdir}
%else
#	install -m 644 AMDVLK/json/Redhat/amd_icd32.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
#	install -m 644 AMDVLK/json/Redhat/amd_icd32.json %{buildroot}%{_datadir}/vulkan/implicit_layer.d/amd_icd.%{_arch}.json
	install -m 644 xgl/build/icd/amd_icd32.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
	install -m 755 xgl/build/icd/amdvlk32.so %{buildroot}%{_libdir}
%endif
install -m 755 xgl/build/spvgen/spvgen.so %{buildroot}%{_libdir}

%if %{with compat32}
	mkdir -p %{buildroot}%{_prefix}/lib
	install -m 644 xgl/build32/icd/amd_icd32.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.i686.json
	install -m 755 xgl/build32/icd/amdvlk32.so %{buildroot}%{_prefix}/lib/
	install -m 755 xgl/build32/spvgen/spvgen.so %{buildroot}%{_prefix}/lib/
%endif

%files
%doc AMDVLK/LICENSE.txt AMDVLK/README.md AMDVLK/topLevelArch.png
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
#{_datadir}/vulkan/implicit_layer.d/amd_icd.%{_arch}.json
%{_libdir}/amdvlk*.so
%{_libdir}/spvgen.so

%if %{with compat32}
%package 32
Summary:	32-bit version of the AMD Vulkan drivers
Group:		System/Libraries

%description 32
32-bit version of the AMD Vulkan drivers

%files 32
%{_datadir}/vulkan/icd.d/amd_icd.i686.json
%{_prefix}/lib/amdvlk*.so
%{_prefix}/lib/svpgen.so
%endif
