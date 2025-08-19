# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

# LAME build script: cleans previous source configure before re-configuring

def run(cmd, cwd=None):
    """명령 실행 헬퍼 (예외 발생 시 스크립트 중단)"""
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, cwd=cwd, check=True)


def clean_build_dir(build_path):
    """build 디렉토리 내부만 삭제하되, *.rxt 마커는 보존"""
    if os.path.isdir(build_path):
        print(f"🧹 Cleaning build dir (preserve *.rxt): {build_path}")
        for item in os.listdir(build_path):
            if item.endswith(".rxt"):
                continue
            p = os.path.join(build_path, item)
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
    else:
        os.makedirs(build_path, exist_ok=True)


def clean_install_dir(path):
    """install 디렉토리 전체 삭제"""
    if os.path.isdir(path):
        print(f"🧹 Removing install dir: {path}")
        shutil.rmtree(path, ignore_errors=True)


def ensure_source(version, source_path):
    """소스 준비: 없으면 get_source.sh 실행"""
    src = os.path.join(source_path, "source", f"lame-{version}")
    if not os.path.isdir(src):
        print(f"🔁 Source missing: {src}, running get_source.sh")
        run(f"bash {os.path.join(source_path, 'get_source.sh')}", cwd=source_path)
    else:
        print(f"✅ Source ready: {src}")
    return src


def build(source_path, build_path, install_path, targets):
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", "3.100")

    # 1) 소스 디렉토리 확보 및 클린업
    src_dir = ensure_source(version, source_path)
    # 이전 configure 결과물(distclean) 처리
    print(f"🧹 Cleaning previous source configuration in: {src_dir}")
    subprocess.run("make distclean", shell=True, cwd=src_dir, check=False)

    # 2) build 디렉토리 초기화
    clean_build_dir(build_path)

    # 3) install 타겟이면 install_root override 및 전체 클린업
    if "install" in targets:
        install_root = f"/core/Linux/APPZ/packages/lame/{version}"
        clean_install_dir(install_root)
    else:
        install_root = install_path

    # 4) configure → build → install
    run(f"{src_dir}/configure --prefix={install_root} --enable-shared --disable-static")
    run("make -j$(nproc)")

    if "install" in targets:
        run("make install")
        # pkg-config 파일 생성 (lame.pc)
        pc_dir = os.path.join(install_root, "lib", "pkgconfig")
        os.makedirs(pc_dir, exist_ok=True)
        pc_path = os.path.join(pc_dir, "lame.pc")
        with open(pc_path, "w") as f:
            f.write(f"""prefix={install_root}
exec_prefix=${{prefix}}
libdir=${{exec_prefix}}/lib
includedir=${{prefix}}/include

Name: lame
Description: LAME MP3 Encoder
Version: {version}
Libs: -L${{libdir}} -lmp3lame
Cflags: -I${{includedir}}""")
        print(f"📄 Generated lame.pc → {pc_path}")
        # package.py 복사
        pkg_src = os.path.join(source_path, "package.py")
        pkg_dst = os.path.join(install_root, "package.py")
        if os.path.isfile(pkg_src):
            print(f"📄 Copying package.py → {pkg_dst}")
            shutil.copy(pkg_src, pkg_dst)

    print(f"✅ lame-{version} build & install completed: {install_root}")


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:]
    )

