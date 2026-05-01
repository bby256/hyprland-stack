%global debug_package %{nil}

Name:           glaze
Version:        7.5.0
Release:        %autorelease
Summary:        Extremely fast, in memory, JSON and interface library

# Glaze itself is MIT, but bundles dragonbox which is Apache-2.0 OR BSL-1.0
License:        MIT AND (Apache-2.0 OR BSL-1.0)
URL:            https://github.com/stephenberry/glaze
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
# Required for header-only library cmake detection
BuildRequires:  cmake-filesystem
BuildRequires:  fast_float-devel
BuildRequires:  xxhashct-static

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}
Provides:       bundled(zmij)
Requires:       cmake-filesystem
Requires:       fast_float-devel
Requires:       xxhashct-static

# Glaze uses heavily modified, namespace-wrapped versions of these
# libraries for performance. Upstream historically bundled Dragonbox,
# but upstream now uses `zmij` for float formatting; do not claim
# bundled(dragonbox).

Patch0:         0001-use-system-fast-float.patch

%description    devel
Glaze is a high performance C++ library. This package contains the 
header-only files for developing applications that use %{name}.

%prep
%autosetup -p1

# Replace the bundled fast_float header with a wrapper around the system version.
cat > include/glaze/util/fast_float.hpp <<'EOF'
#pragma once
#include <fast_float/fast_float.h>
namespace glz { namespace fast_float = ::fast_float; }
EOF

# Replacing the bundled xxhash header with a wrapper pointing to the system version
cat > include/glaze/api/xxh64.hpp <<'EOF'
#include <xxh64.hpp>
EOF

%build
%cmake \
    -Dglaze_INSTALL_CMAKEDIR=%{_datadir}/cmake/%{name} \
    -Dglaze_DEVELOPER_MODE:BOOL=OFF \
    -Dglaze_ENABLE_FUZZING:BOOL=OFF \
    -DBUILD_TESTING:BOOL=OFF
%cmake_build

%install
%cmake_install

%check
# Tests are currently disabled as they require openalgz/ut 
# which is not yet packaged in Fedora.
# %%ctest

%files devel
%license LICENSE
%doc README.md
# Own the directory and its contents
%{_includedir}/%{name}/
%{_datadir}/cmake/%{name}/

%changelog
%autochangelog