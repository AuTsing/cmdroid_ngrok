import os
import local

pkg_name = "cmdroid_ngrok"
working_dir = f"/data/local/tmp/{pkg_name}"
profile = "debug"
ndk_dir = "/home/autsing/Apps/AndroidSdk/ndk/26.2.11394342"
cc_filename = "aarch64-linux-android28-clang"
ar_filename = "llvm-ar"
cc = f"{ndk_dir}/toolchains/llvm/prebuilt/linux-x86_64/bin/{cc_filename}"
ar = f"{ndk_dir}/toolchains/llvm/prebuilt/linux-x86_64/bin/{ar_filename}"

os.environ["ANDROID_NDK_ROOT"] = ndk_dir
os.environ["CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER"] = cc
os.environ["CC_aarch64_linux_android"] = cc
os.environ["AR_aarch64_linux_android"] = ar

build_cmd = "cargo build --target=aarch64-linux-android"

exit_code = os.system(build_cmd)
if exit_code != 0:
    raise Exception(f"Build failed, exit with code: {exit_code}.")

executor_filename = pkg_name
executor_src_path = f"./target/aarch64-linux-android/{profile}/{executor_filename}"
executor_dst_path = f"{working_dir}/{executor_filename}"
os.system(f"adb shell rm -r {working_dir}")
os.system(f"adb shell mkdir {working_dir}")
os.system(f"adb push {executor_src_path} {executor_dst_path}")
os.system(
    f'adb shell "NGROK_AUTHTOKEN={local.NGROK_AUTHTOKEN} URL={local.URL} {executor_dst_path}"'
)
