# navikoLAB/runtime/media_identity_layer.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
import uuid


PHASE = "Phase106-3 Naviko Media Identity Layer"

ROOT = Path(__file__).resolve().parents[2]

MEDIA_DIR = ROOT / "runtime" / "media_identity"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = MEDIA_DIR / "media_identity_state.json"
LOG_FILE = MEDIA_DIR / "media_identity_log.json"


# -----------------------------
# Media Identity Model
# -----------------------------

@dataclass
class MediaIdentity:
    identity_id: str
    name: str
    avatar_style: str
    voice_style: str
    model_3d_state: str
    emotion_state: str
    version: int


@dataclass
class IdentityEvent:
    event_id: str
    action: str
    detail: str
    timestamp: str


# -----------------------------
# Media Identity Core
# -----------------------------

class MediaIdentityLayer:

    def __init__(self):

        self.identity = MediaIdentity(
            identity_id=str(uuid.uuid4()),
            name="Naviko",
            avatar_style="default_chibi_core",
            voice_style="soft_jp_female_sim",
            model_3d_state="basic_placeholder",
            emotion_state="neutral",
            version=1
        )

        self.history: list[IdentityEvent] = []

    # -----------------------------
    # Identity Evolution
    # -----------------------------

    def evolve_avatar(self, style: str):

        self.identity.avatar_style = style
        self.identity.version += 1

        self.record("avatar_evolution", style)

    def evolve_voice(self, style: str):

        self.identity.voice_style = style
        self.identity.version += 1

        self.record("voice_evolution", style)

    def evolve_3d(self, state: str):

        self.identity.model_3d_state = state
        self.identity.version += 1

        self.record("3d_evolution", state)

    def set_emotion(self, emotion: str):

        self.identity.emotion_state = emotion

        self.record("emotion_change", emotion)

    # -----------------------------
    # Event Logging
    # -----------------------------

    def record(self, action: str, detail: str):

        event = IdentityEvent(
            event_id=str(uuid.uuid4()),
            action=action,
            detail=detail,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )

        self.history.append(event)

    # -----------------------------
    # Snapshot Save
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps(asdict(self.identity), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        LOG_FILE.write_text(
            json.dumps([asdict(e) for e in self.history], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -----------------------------
    # Summary
    # -----------------------------

    def summary(self):

        return {
            "phase": PHASE,
            "identity": self.identity.name,
            "version": self.identity.version,
            "avatar": self.identity.avatar_style,
            "voice": self.identity.voice_style,
            "model_3d": self.identity.model_3d_state,
            "emotion": self.identity.emotion_state,
            "events": len(self.history),
        }


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    media = MediaIdentityLayer()

    # simulate evolution
    media.evolve_avatar("naviko_style_v2_soft")
    media.evolve_voice("voice_v2_clear_jp")
    media.evolve_3d("3d_base_mesh_v1")
    media.set_emotion("curious")

    media.save()

    print("=== Naviko Media Identity Layer ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("summary:", media.summary())
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()