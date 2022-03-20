#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Capture the outcome of Python function calls
Summary(pl.UTF-8):	Przechwytywanie wyników wywołań funkcji pythonowych
Name:		python-outcome
# keep 1.0.x here for python2 support
Version:	1.0.1
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/outcome/
Source0:	https://files.pythonhosted.org/packages/source/o/outcome/outcome-%{version}.tar.gz
# Source0-md5:	17e511c2bd1ee3cdd7a1aad29fe0133b
URL:		https://pypi.org/project/outcome/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-attrs >= 19.2.0
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-async_generator
BuildRequires:	python3-attrs >= 19.2.0
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capture the outcome of Python function calls.

%description -l pl.UTF-8
Przechwytywanie wyników wywołań funkcji pythonowych.

%package -n python3-outcome
Summary:	Capture the outcome of Python function calls
Summary(pl.UTF-8):	Przechwytywanie wyników wywołań funkcji pythonowych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-outcome
Capture the outcome of Python function calls.

%description -n python3-outcome -l pl.UTF-8
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
%setup -q -n outcome-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py_sitescriptdir}/outcome
%{py_sitescriptdir}/outcome-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-outcome
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/outcome
%{py3_sitescriptdir}/outcome-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
