import os
import subprocess
import platform
import time

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def run_command(command, shell=False):
    try:
        result = subprocess.run(
            command.split(),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr.strip()}"
    except Exception as e:
        return False, f"Exception: {str(e)}"

def check_adb_devices():
    success, output = run_command("adb devices")
    if not success:
        return False, output
    devices = [line.split('\t')[0] for line in output.split('\n')[1:] if line.strip()]
    return bool(devices), devices

def check_fastboot_devices():
    success, output = run_command("fastboot devices")
    if not success:
        return False, output
    devices = [line.split('\t')[0] for line in output.split('\n') if line.strip()]
    return bool(devices), devices

class ADBTools:
    @staticmethod
    def show_menu():
        while True:
            clear_screen()
            print("""ADB 工具菜单
1. 重启至System
2. 重启至Recovery
3. 重启至Fastboot
4. 重启至Fastbootd
5. 查看已连接设备
6. 安装APK
7. 卸载应用
8. 禁用验证 (dm校验/verity)
9. 启用验证 (dm校验/verity)
0. 返回主菜单""")

            choice = input("请输入选项：")

            if choice == '1':
                ADBTools.reboot_system()
            elif choice == '2':
                ADBTools.reboot_recovery()
            elif choice == '3':
                ADBTools.reboot_fastboot()
            elif choice == '4':
                ADBTools.reboot_fastbootd()
            elif choice == '5':
                ADBTools.list_devices()
            elif choice == '6':
                ADBTools.install_apk()
            elif choice == '7':
                ADBTools.uninstall_app()
            elif choice == '8':
                ADBTools.disable_verification()
            elif choice == '9':
                ADBTools.enable_verification()
            elif choice == '0':
                break
            else:
                print("无效选项！")
            input("\n按回车继续...")

    @staticmethod
    def reboot_system():
        success, output = run_command("adb reboot")
        print("正在进入System..." if success else output)

    @staticmethod
    def reboot_recovery():
        success, output = run_command("adb reboot recovery")
        print("正在进入Recovery..." if success else output)

    @staticmethod
    def reboot_fastboot():
        success, output = run_command("adb reboot bootloader")
        print("正在进入Fastboot..." if success else output)

    @staticmethod
    def reboot_fastbootd():
        success, output = run_command("adb reboot fastboot")
        print("正在进入Fastbootd..." if success else output)

    @staticmethod
    def list_devices():
        success, devices = check_adb_devices()
        if success:
            print("已连接设备：")
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device}")
        else:
            print(devices)

    @staticmethod
    def install_apk():
        apk_path = input("请拖入APK文件：").strip()
        success, output = run_command(f"adb install -r {apk_path}")
        print("安装成功" if success else output)

    @staticmethod
    def uninstall_app():
        package = input("请输入包名：").strip()
        success, output = run_command(f"adb uninstall {package}")
        print("卸载成功" if success else output)

    @staticmethod
    def disable_verification():
        print("警告：此操作可能需要解锁设备！")
        success, output = run_command("adb root")
        if not success:
            print(output)
            return
        success, output = run_command("adb disable-verity")
        print("已禁用验证" if success else output)

    @staticmethod
    def enable_verification():
        print("警告：此操作可能需要解锁设备！")
        success, output = run_command("adb root")
        if not success:
            print(output)
            return
        success, output = run_command("adb enable-verity")
        print("已启用验证" if success else output)

class FastbootTools:
    @staticmethod
    def show_menu():
        while True:
            clear_screen()
            print("""Fastboot 工具菜单:
1. 重启至System
2. 重启至Recovery
3. 重启至Fastboot
4. 重启至Fastbootd
5. 查看已连接设备
6. 解锁Bootloader
7. 重新锁定Bootloader
8. 刷写分区
9. 擦除分区
0. 返回主菜单""")

            choice = input("请输入选项：")

            if choice == '1':
                FastbootTools.reboot_system()
            elif choice == '2':
                FastbootTools.reboot_recovery()
            elif choice == '3':
                FastbootTools.reboot_fastboot()
            elif choice == '4':
                FastbootTools.reboot_fastbootd()
            elif choice == '5':
                FastbootTools.list_devices()
            elif choice == '6':
                FastbootTools.unlock_bootloader()
            elif choice == '7':
                FastbootTools.lock_bootloader()
            elif choice == '8':
                FastbootTools.flash_partition()
            elif choice == '9':
                FastbootTools.erase_partition()
            elif choice == '0':
                break
            else:
                print("无效选项！")
            input("\n按回车继续...")

    @staticmethod
    def reboot_system():
        success, output = run_command("fastboot reboot")
        print("正在进入System..." if success else output)

    @staticmethod
    def reboot_recovery():
        success, output = run_command("fastboot reboot recovery")
        print("正在进入Recovery..." if success else output)

    @staticmethod
    def reboot_fastboot():
        success, output = run_command("fastboot reboot bootloader")
        print("正在进入Fastboot..." if success else output)

    @staticmethod
    def reboot_fastbootd():
        success, output = run_command("fastboot reboot fastboot")
        print("正在进入Fastbootd..." if success else output)

    @staticmethod
    def list_devices():
        success, devices = check_fastboot_devices()
        if success:
            print("Fastboot设备：")
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device}")
        else:
            print(devices)

    @staticmethod
    def unlock_bootloader():
        print("警告：这会清除所有用户数据！")
        confirm = input("确认解锁？(输入YES继续): ")
        if confirm == "YES":
            success, output = run_command("fastboot flashing unlock")
            print("解锁成功" if success else output)
        else:
            print("已取消操作")

    @staticmethod
    def lock_bootloader():
        print("警告：这可能会清除用户数据！")
        confirm = input("确认锁定？(输入YES继续): ")
        if confirm == "YES":
            success, output = run_command("fastboot flashing lock")
            print("锁定成功" if success else output)
        else:
            print("已取消操作")

    @staticmethod
    def flash_partition():
        partition = input("请输入分区名称（如init_boot、boot、recovery等）: ").strip()
        image = input("请拖入镜像文件: ").strip()
        success, output = run_command(f"fastboot flash {partition} {image}")
        print("刷写成功" if success else output)

    @staticmethod
    def erase_partition():
        partition = input("请输入要擦除的分区名称: ").strip()
        success, output = run_command(f"fastboot erase {partition}")
        print("擦除成功" if success else output)

def manual_command():
    clear_screen()
    print("手动执行命令模式（输入'exit'返回）")
    while True:
        cmd = input("\n输入命令：").strip()
        if cmd.lower() == 'exit':
            break
        if not cmd:
            continue

        if cmd.startswith("adb"):
            success, output = run_command(cmd)
        elif cmd.startswith("fastboot"):
            success, output = run_command(cmd)
        else:
            print("只支持adb或fastboot开头的命令")
            continue

        print("\n输出结果：")
        print(output if success else f"命令执行失败: {output}")

def main():
    while True:
        clear_screen()
        print("""
欢迎来到3141Toolbox!
1. ADB类命令
2. Fastboot类命令
3. 手动执行命令
0. 退出
        """)
        choice = input("请输入选项：")

        if choice == '1':
            ADBTools.show_menu()
        elif choice == '2':
            FastbootTools.show_menu()
        elif choice == '3':
            manual_command()
        elif choice == '0':
            print("感谢使用！")
            break
        else:
            print("无效选项！")
            input("按回车继续...")

if __name__ == "__main__":
    main()
