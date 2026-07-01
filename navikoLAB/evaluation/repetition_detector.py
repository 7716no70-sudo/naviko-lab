class RepetitionDetector:

    def detect(self, history):

        if len(history) < 3:
            return False

        last = history[-3:]

        # ★ flatten対応
        flat = []
        for h in last:
            if isinstance(h, list):
                flat.extend(h)
            else:
                flat.append(h)

        if len(set(flat)) == 1:
            return True

        return False