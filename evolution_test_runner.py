# evolution_test_runner.py

from navikoLAB.service.naviko_service import NavikoServiceRunner


def run_test():

    service = NavikoServiceRunner()

    print("[TEST] Evolution Loop Start")

    service.start()


if __name__ == "__main__":
    run_test()