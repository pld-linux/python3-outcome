#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Capture the outcome of Python function calls
Summary(pl.UTF-8):	Przechwytywanie wyników wywołań funkcji pythonowych
Name:		python3-outcome
Version:	1.3.0
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/outcome/
Source0:	https://files.pythonhosted.org/packages/source/o/outcome/outcome-%{version}.post0.tar.gz
# Source0-md5:	3a626832ac864c95f6054958d0da3011
URL:		https://pypi.org/project/outcome/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-attrs >= 19.2.0
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capture the outcome of Python function calls.

%description -l pl.UTF-8
Przechwytywanie wyników wywołań funkcji pythonowych.

%package apidocs
Summary:	API documentation for Python outcome module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona outcome
Group:		Documentation

%description apidocs
API documentation for Python outcome module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona outcome.

%prep
%setup -q -n outcome-%{version}.post0

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/outcome
%{py3_sitescriptdir}/outcome-%{version}*-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
