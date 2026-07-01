# naviko_service.py

from navikoLAB.service.service_runner import NavikoServiceRunner


def main():
    service = NavikoServiceRunner()
    service.start()


if __name__ == "__main__":
    main()