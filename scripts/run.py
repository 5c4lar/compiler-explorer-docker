import yaml
import subprocess
import pathlib

C_HEADER = """compilers=&cgcc86:&cclang

defaultCompiler={compiler}{short_version}
demangler=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-cxxfilt
objdumper=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-objdump
needsMulti=false

llvmDisassembler=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-dis

"""

C_GCC_COMPILER = """group.cgcc86.compilers=cg{short_version}
group.cgcc86.groupName=GCC x86-64
group.cgcc86.instructionSet=amd64
group.cgcc86.isSemVer=true
group.cgcc86.baseName=x86-64 gcc
group.cgcc86.supportsPVS-Studio=true
group.cgcc86.supportsSonar=true
group.cgcc86.licenseLink=https://gcc.gnu.org/onlinedocs/gcc/Copying.html
group.cgcc86.licenseName=GNU General Public License
group.cgcc86.licensePreamble=Copyright (c) 2007 Free Software Foundation, Inc. <a href="https://fsf.org/" target="_blank">https://fsf.org/</a>
group.cgcc86.compilerCategories=gcc

compiler.cg{short_version}.exe=/opt/compiler-explorer/gcc-{version}/bin/gcc
compiler.cg{short_version}.semver={version}
"""

C_CLANG_COMPILER= """group.cclang.compilers=cclang{short_version}
group.cclang.intelAsm=-mllvm --x86-asm-syntax=intel
group.cclang.options=--gcc-toolchain=/opt/compiler-explorer/gcc-{gcc_version}
group.cclang.groupName=Clang x86-64
group.cclang.instructionSet=amd64
group.cclang.isSemVer=true
group.cclang.baseName=x86-64 clang
group.cclang.compilerType=clang
group.cclang.supportsPVS-Studio=true
group.cclang.supportsSonar=true
group.cclang.licenseName=LLVM Apache 2
group.cclang.licenseLink=https://github.com/llvm/llvm-project/blob/main/LICENSE.TXT
group.cclang.licensePreamble=The LLVM Project is under the Apache License v2.0 with LLVM Exceptions
group.cclang.compilerCategories=clang
group.cclang.demangler=/opt/compiler-explorer/clang-{version}/bin/llvm-cxxfilt

compiler.cclang{short_version}.exe=/opt/compiler-explorer/clang-{version}/bin/clang
compiler.cclang{short_version}.semver={version}
compiler.cclang{short_version}.options=--gcc-toolchain=/opt/compiler-explorer/gcc-{gcc_version}
"""

CPP_HEADER="""compilers=&gcc86:&clang

defaultCompiler={compiler}{short_version}
demangler=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-cxxfilt
objdumper=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-objdump
needsMulti=false

llvmDisassembler=/opt/compiler-explorer/clang-{clang_version}/bin/llvm-dis
"""

CPP_GCC_COMPILER="""group.gcc86.compilers=g{short_version}
group.gcc86.groupName=GCC x86-64
group.gcc86.instructionSet=amd64
group.gcc86.baseName=x86-64 gcc
group.gcc86.isSemVer=true
group.gcc86.unwiseOptions=-march=native
group.gcc86.supportsPVS-Studio=true
group.gcc86.supportsSonar=true
group.gcc86.licenseLink=https://gcc.gnu.org/onlinedocs/gcc/Copying.html
group.gcc86.licenseName=GNU General Public License
group.gcc86.licensePreamble=Copyright (c) 2007 Free Software Foundation, Inc. <a href="https://fsf.org/" target="_blank">https://fsf.org/</a>
group.gcc86.supportsBinaryObject=true
group.gcc86.compilerCategories=gcc

compiler.g{short_version}.exe=/opt/compiler-explorer/gcc-{version}/bin/g++
compiler.g{short_version}.semver={version}
"""

CPP_CLANG_COMPILER="""group.clang.compilers=clang{short_version}
group.clang.intelAsm=-mllvm --x86-asm-syntax=intel
group.clang.options=--gcc-toolchain=/opt/compiler-explorer/gcc-{gcc_version}
group.clang.groupName=Clang x86-64
group.clang.instructionSet=amd64
group.clang.baseName=x86-64 clang
group.clang.isSemVer=true
group.clang.compilerType=clang
group.clang.unwiseOptions=-march=native
group.clang.supportsPVS-Studio=true
group.clang.supportsSonar=true
group.clang.supportsLlvmCov=true
group.clang.licenseName=LLVM Apache 2
group.clang.licenseLink=https://github.com/llvm/llvm-project/blob/main/LICENSE.TXT
group.clang.licensePreamble=The LLVM Project is under the Apache License v2.0 with LLVM Exceptions
group.clang.supportsBinaryObject=true
group.clang.compilerCategories=clang
group.clang.demangler=/opt/compiler-explorer/clang-{version}/bin/llvm-cxxfilt

compiler.clang{short_version}.exe=/opt/compiler-explorer/clang-{version}/bin/clang++
compiler.clang{short_version}.semver={version}
compiler.clang{short_version}.options=--gcc-toolchain=/opt/compiler-explorer/gcc-{gcc_version}
compiler.clang{short_version}.ldPath=${{exePath}}/../lib|${{exePath}}/../lib/x86_64-unknown-linux-gnu
compiler.clang{short_version}.debugPatched=true
"""

def short_version(version):
    return "".join(version.split("."))

def get_c_properties(config):
    default_compiler=config["default"]["compiler"]
    default_version=config["default"]["version"]
    header = C_HEADER.format(short_version=short_version(default_version), clang_version=default_version, compiler=default_compiler)
    compilers = []
    for compiler, variations in config["compilers"].items():
        for variation in variations:
            version = variation["version"]
            match compiler:
                case "compilers/c++/x86/gcc":
                    compilers.append(C_GCC_COMPILER.format(short_version=short_version(version), version=version))
                case "compilers/c++/clang":
                    gcc_version = variation["gcc_version"]
                    compilers.append(C_CLANG_COMPILER.format(version=version, short_version=short_version(version), gcc_version=gcc_version))
    result = header + "\n" + "\n".join(compilers)
    return result

def get_cpp_properties(config):
    default_compiler=config["default"]["compiler"]
    default_version=config["default"]["version"]
    header = CPP_HEADER.format(short_version=short_version(default_version), clang_version=default_version, compiler=default_compiler)
    compilers = []
    for compiler, variations in config["compilers"].items():
        for variation in variations:
            version = variation["version"]
            match compiler:
                case "compilers/c++/x86/gcc":
                    compilers.append(CPP_GCC_COMPILER.format(short_version=short_version(version), version=version))
                case "compilers/c++/clang":
                    gcc_version = variation["gcc_version"]
                    compilers.append(CPP_CLANG_COMPILER.format(version=version, short_version=short_version(version), gcc_version=gcc_version))
    result = header + "\n" + "\n".join(compilers)
    return result

def compiler_ids(config):
    result = []
    for compiler, variations in config["compilers"].items():
        for variation in variations:
            result.append(f"{compiler} {variation['version']}")
    return result

def build_docker(config):
    cmd = "docker build -t compiler_explorer ./docker"
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if res.returncode != 0:
        exit(-1)

def download_compilers(config):
    ce_install = f"/infra/bin/ce_install --filter-match-any install {' '.join(['\''+ i + '\'' for i in compiler_ids(config)])}"
    cmd = f"docker run -it -v {config['cache_dir']}:/opt/compiler-explorer --rm compiler_explorer {ce_install}"
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if res.returncode != 0:
        exit(-1)
        
def start(config):
    cmd = f"docker run -d -v {config['cache_dir']}:/opt/compiler-explorer -p {config['port']}:10240 --rm --name compiler_explorer compiler_explorer"
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if res.returncode != 0:
        print(res.stderr.decode())
        exit(-1)
    print(f"Compiler Explorer started on port {config['port']}")
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the config file")
    parser.add_argument("--stage", help="Stage of running the script. [config, build, download, start]")
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    with open("docker/c.local.properties", "w") as f:
        f.write(get_c_properties(config))
    with open("docker/c++.local.properties", "w") as f:
        f.write(get_cpp_properties(config))
    if args.stage == "config":
        return
    build_docker(config)
    if args.stage == "build":
        return
    download_compilers(config)
    if args.stage == "download":
        return
    start(config)
    
if __name__ == "__main__":
    main()