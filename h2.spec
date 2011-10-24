Name:           h2
Version:        1.2.145
Release:        4
Summary:        Java SQL database

Group:          Development/Java
License:        EPL
URL:            http://www.h2database.com
Source0:        http://www.h2database.com/h2-2010-11-02.zip
Patch0:         add-javadoc-target.patch
Patch1:         fix-for-servlet25.patch
Patch2:         fix_manifest.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: java-devel >= 0:1.5.0
BuildRequires:  ant
BuildRequires:  lucene >= 2.4
BuildRequires:  slf4j >= 1.5
BuildRequires:  felix-osgi-core >= 1.2
BuildRequires:  servlet25
Requires: java >= 0:1.5.0

%description
H2 is a the Java SQL database. The main features of H2 are:
* Very fast, open source, JDBC API
* Embedded and server modes; in-memory databases
* Browser based Console application
* Small footprint: around 1 MB jar file size 

%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p0
pushd src/test/org/h2/test/unit
%patch1 -p0
popd
%patch2 -p0 -b .orig
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
sed -i -e "s|bin\/META-INF\/MANIFEST.MF|src\/main\/META-INF\/MANIFEST.MF|g" build.xml
sed -i -e 's|<manifest file="src/main/META-INF/MANIFEST.MF">|<manifest file="src/main/META-INF/MANIFEST.MF" mode="update">|g' build.xml

%build
export CLASSPATH=$(build-classpath servlet lucene slf4j/api felix/org.osgi.core)
ant -Dext.present=true all javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p bin/h2.jar   \
$RPM_BUILD_ROOT%{_javadir}/%{name}.jar


mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp javadoc  \
$RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc src/docsrc/html/license.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc src/docsrc/html/license.html

