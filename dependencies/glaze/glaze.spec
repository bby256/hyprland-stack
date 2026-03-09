%global debug_package %{nil}

Name:           glaze
Version:        7.1.1
Release:        %autorelease
Summary:        Extremely fast, in memory, JSON and interface library

# Glaze itself is MIT, but bundles dragonbox which is Apache-2.0 OR BSL-1.0
License:        MIT AND BSD-2-Clause AND (Apache-2.0 OR BSL-1.0)
URL:            https://github.com/stephenberry/glaze
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
# Required for header-only library cmake detection
BuildRequires:  cmake-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}
Requires:       cmake-filesystem

# Glaze uses heavily modified, namespace-wrapped versions of these 
# libraries for performance. Upstream does not support system versions.
Provides:       bundled(fast_float) = 6.1.1
Provides:       bundled(dragonbox) = 1.1.3
Provides:       bundled(xxhash) = 0.8.2

%description    devel
Glaze is a high performance C++ library. This package contains the 
header-only files for developing applications that use %{name}.

%prep
%autosetup -p1

%build
%cmake \
    -Dglaze_INSTALL_CMAKEDIR=%{_datadir}/cmake/%{name} \
    -Dglaze_DISABLE_SIMD_WHEN_SUPPORTED:BOOL=ON \
    -Dglaze_DEVELOPER_MODE:BOOL=OFF \
    -Dglaze_ENABLE_FUZZING:BOOL=OFF \
    -DBUILD_TESTING:BOOL=OFF
%cmake_build

%install
%cmake_install

%check
# Tests are currently disabled as they require openalgz/ut 
# which is not yet packaged in Fedora.
# %ctest

%files devel
%license LICENSE
%doc README.md
# Own the directory and its contents
%{_includedir}/%{name}/
%{_datadir}/cmake/%{name}/

%changelog
%autochangelog