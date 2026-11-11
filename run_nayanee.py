"""Nayanee Production & Demonstration Server Launcher.
"""

import uvicorn
from core.config import settings


def main():
    print("=" * 60)
    print("  NAYANEE (ನಯनी) — NO-DEVICE VISION INTELLIGENCE")
    print("  ZEISS Hackathon — Theme 2: No-Device Vision Intelligence (Theme 1: AFI)")
    print(f"  Supported Languages: {', '.join(settings.SUPPORTED_LANGUAGES)}")
    print(f"  Starting server at: http://localhost:{settings.API_PORT}")
    print("=" * 60)

    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
