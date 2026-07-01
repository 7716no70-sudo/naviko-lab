from navikoLAB.daemon.loop_daemon import LoopDaemon


def main():
    daemon = LoopDaemon()

    print("[Daemon A2] Stabilized Mode Start")

    daemon.start()


if __name__ == "__main__":
    main()