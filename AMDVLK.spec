%undefine _debugsource_packages

# Workaround for the build process eating way too much RAM
%define _disable_lto 1

%global amdvlk_version	  v-%{version}
%global amdvlk_core_version	  2.192

# Keep in basic sync with:
# https://github.com/tomkv/packaging-rpm/blob/master/amdvlk/amdvlk.spec
# https://copr.fedorainfracloud.org/coprs/tkov/amdvlk/package/amdvlk-vulkan-driver/

%global amdvlk_commit		cab8f8631d99240a6503872083bd544fe85f628f
%global gpurt_commit		a1103572dfcc29c7baee04e2ececedca8fda86d7
%global llvm_dialects_commit	6b6568db81d5a03002d99db9a83101cad1938cb3
%global llvm_commit		02394516f587d6bdb606b068fe604284f5c6a007
%global llpc_commit		f44e737f5e13eca803f465fc86532c24608c4daf
%global xgl_commit		6288905587fafc221b60045bceba73cf26e433ad
%global pal_commit		f01505f7fe4b38b573a41cb4d9d66d00e0c256f0
%global spvgen_commit		fd49f1d477a203379f6557e9c74edfadc10b7672
%global metrohash_commit	18893fb28601bb9af1154cd1a671a121fff6d8d3
%global cwpack_commit		4f8cf0584442a91d829d269158567d7ed926f026

%global glslang_commit		d9c3c7538b2449e39cfb0d793702d218ed58ff03
%global spirv_tools_commit	51892874ba08f3ac0d9b1fcf3893c8516693a88e
%global spirv_headers_commit	268a061764ee69f09a477a695bf6a11ffe311b8d
%global spirv_cross_commit	54b48a2f3afd9bbaaddc9f876f85a0fbfad9c7fa

%global amdvlk_short_commit	%(c=%{amdvlk_commit}; echo ${c:0:7})
%global gpurt_short_commit	%(c=%{gpurt_commit}; echo ${c:0:7})
%global llvm_dialects_short_commit	%(c=%{llvm_dialects_commit}; echo ${c:0:7})
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
%global commit_date		20211227
%global gitrel			.%{commit_date}.git%{amdvlk_short_commit}
%global khronos_url		https://github.com/KhronosGroup/

%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

Name:		amdvlk-vulkan-driver
Version:	2023.Q2.3
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
Source12:	%url/gpurt/archive/%{gpurt_commit}/gpurt-%{gpurt_commit}.tar.gz
Source14:	%url/llvm-dialects/archive/%{llvm_dialects_commit}/llvm-dialects-%{llvm_dialects_commit}.tar.gz

#Patch0:		add-missing-include.patch

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
BuildRequires: dxc
BuildRequires: dxc-libdxcompiler-devel
BuildRequires: glslang
BuildRequires: libstdc++-devel
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(xrandr)
BuildRequires: gtest-devel
BuildRequires: wayland-devel
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libdrm)
%if %{with compat32}
BuildRequires: libc6
BuildRequires: devel(libXau)
BuildRequires: devel(libXdmcp)
BuildRequires: devel(libXext)
BuildRequires: devel(libXrender)
BuildRequires: devel(libxcb)
BuildRequires: devel(libX11)
BuildRequires: devel(libxshmfence)
BuildRequires: devel(libXrandr)
BuildRequires: devel(libwayland-client)
BuildRequires: devel(libz)
BuildRequires: devel(libssl)
BuildRequires: devel(libffi)
BuildRequires: devel(libdrm)
%endif

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
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9 -a 10 -a 11 -a 12 -a 14
ln -s AMDVLK-%{amdvlk_version} AMDVLK
ln -s llvm-project-%{llvm_commit} llvm-project
ln -s llpc-%{llpc_commit} llpc
ln -s xgl-%{xgl_commit} xgl
ln -s pal-%{pal_commit} pal
ln -s spvgen-%{spvgen_commit} spvgen
ln -s gpurt-%{gpurt_commit} gpurt
ln -s llvm-dialects-%{llvm_dialects_commit} llvm-dialects
rmdir llpc/imported/llvm-dialects
ln -s $(pwd)/llvm-dialects llpc/imported/
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

%autopatch -p1

%build
%if %{with compat32}
# Make sure we don't get --color-diagnostics on ld.bfd -- the checks
# seem to use ld.lld...
# The check seems to be broken, whatever flag is set is passed. So let's
# set it to something we actually want.
sed -i -e 's/--color-diagnostics/-O2/g' ./llvm-project-*/llvm/cmake/modules/HandleLLVMOptions.cmake
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
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -O3 -fno-lto -m32 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -O3 -fno-lto -m32 -DNDEBUG" \
	-DCMAKE_EXE_LINKER_FLAGS_INIT="%{optflags} -Wl,--build-id=sha1" \
	-DCMAKE_SHARED_LINKER_FLAGS_INIT="%{optflags} -Wl,--build-id=sha1" \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_WAYLAND_SUPPORT=ON \
	-DLLVM_ENABLE_WARNINGS=OFF \
	-G Ninja
%ninja_build
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
	-DCMAKE_C_FLAGS_RELEASE="%{optflags} -flto=thin -O3 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -flto=thin -O3 -DNDEBUG" \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -flto=thin -O3 -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -flto=thin -O3 -DNDEBUG" \
%endif
	-DCMAKE_EXE_LINKER_FLAGS_INIT="%{optflags} -Wl,--build-id=sha1" \
	-DCMAKE_SHARED_LINKER_FLAGS_INIT="%{optflags} -Wl,--build-id=sha1" \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_WAYLAND_SUPPORT=ON \
	-DLLVM_ENABLE_WARNINGS=OFF \
	-G Ninja

%ninja
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
#install -m 755 xgl/build/spvgen/spvgen.so %{buildroot}%{_libdir}

%if %{with compat32}
	mkdir -p %{buildroot}%{_prefix}/lib
	install -m 644 xgl/build32/icd/amd_icd32.json %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.i686.json
	install -m 755 xgl/build32/icd/amdvlk32.so %{buildroot}%{_prefix}/lib/
#	install -m 755 xgl/build32/spvgen/spvgen.so %{buildroot}%{_prefix}/lib/
%endif

# Workaround for lld generating an 8-byte build-id that breaks debugedit
find %{buildroot} -name "*.so" |xargs strip -R .comment --strip-unneeded 

%files
%doc AMDVLK/LICENSE.txt AMDVLK/README.md AMDVLK/topLevelArch.png
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
#{_datadir}/vulkan/implicit_layer.d/amd_icd.%{_arch}.json
%{_libdir}/amdvlk*.so
#{_libdir}/spvgen.so

%if %{with compat32}
%package 32
Summary:	32-bit version of the AMD Vulkan drivers
Group:		System/Libraries

%description 32
32-bit version of the AMD Vulkan drivers

%files 32
%{_datadir}/vulkan/icd.d/amd_icd.i686.json
%{_prefix}/lib/amdvlk*.so
#{_prefix}/lib/spvgen.so
%endif
