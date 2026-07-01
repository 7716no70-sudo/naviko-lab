# service_installer.py

import os


class ServiceInstaller:

    def install_startup(self):
        """
        Windowsスタートアップ登録（簡易版）
        """
        startup_path = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )

        bat_file = os.path.join(startup_path, "naviko_start.bat")

        with open(bat_file, "w") as f:
            f.write(
                "cd C:\\Users\\7716n\\OneDrive\\デスクトップ\\naviko_lab\n"
                "python -m navikoLAB.service.service_runner\n"
            )

        print("[Installer] Startup registered")