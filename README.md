# Game Controller Database

A curated and automatically updated game controller mapping database for Linux platforms, based on the [SDL_GameControllerDB](https://github.com/mdqinc/SDL_GameControllerDB) project.

## Overview

This repository provides a filtered and enhanced version of the SDL Game Controller Database specifically optimized for Linux gaming. It automatically monitors the upstream repository for updates and maintains a clean, Linux-focused database with custom controller mappings.

The database is published as **two files** so that controllers work correctly with `SDL_JOYSTICK_HIDAPI` enabled under **both SDL2 and SDL3**. The HIDAPI backend numbers a pad differently between the two SDL majors (SDL2 maps the d-pad to buttons, SDL3 to a hat), and over USB the two mappings share a GUID — so they cannot coexist in one file. The workflow therefore splits them:

- **`gamecontrollerdb.txt`** — joydev mappings + SDL3-HIDAPI mappings (the default file).
- **`gamecontrollerdb-SDL2.txt`** — SDL2-HIDAPI mappings only, loaded *in addition* by SDL2 consumers so they override the colliding SDL3 row.

## Features

- 🐧 **Linux-focused**: Field-anchored on the `platform:Linux` token (keeps Linux rows and platform-less custom rows; never drops a pad just because its *name* contains "Windows", "Android", etc.)
- 🎚️ **Two-lane output**: SDL2-HIDAPI mappings split into a separate file so HIDAPI stays usable on both SDL2 and SDL3
- 🔄 **Auto-updated**: Daily automated checks for upstream changes
- 🎮 **Custom mappings**: Includes additional controller configurations for specialized hardware
- 🧹 **Duplicate-free**: Removes duplicate entries by GUID, per lane (newest wins)

## Files

- **`gamecontrollerdb.txt`** - Main database: joydev + SDL3-HIDAPI mappings
- **`gamecontrollerdb-SDL2.txt`** - SDL2-HIDAPI mappings, loaded in addition by SDL2 consumers
- **`add_gamecontrollerdb.txt`** - Custom controller mappings, merged in and routed to the correct lane automatically by d-pad style
- **`.github/workflows/gamecontrollerdb.yaml`** - Automated workflow configuration

## Supported Controllers

The database includes mappings for a wide variety of controllers including:

- Xbox controllers (360, One, Series X/S)
- PlayStation controllers (PS3, PS4, PS5)
- Nintendo controllers (Pro Controller, Wii Remote)
- Generic USB gamepads
- Arcade controllers (X-Arcade, IPAC)
- Racing wheels (Logitech G25/G27/G29, Thrustmaster)
- Retro gaming controllers (8BitDo, RetroFlag)
- Handheld device controllers (Anbernic, PiBoy DMG)

## Usage

### Direct Download

Download the `gamecontrollerdb.txt` file directly from this repository and place it in your application's directory.

### Integration with SDL2

```c
#include <SDL2/SDL.h>

int main() {
    SDL_Init(SDL_INIT_GAMECONTROLLER);

    // Load the controller database. Load the main file first, then — because
    // this is SDL2 with HIDAPI on — also load the SDL2-HIDAPI lane so its rows
    // override the colliding SDL3-HIDAPI rows. (An SDL3 app loads only the
    // main file.)
    SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
    SDL_GameControllerAddMappingsFromFile("gamecontrollerdb-SDL2.txt");

    // Your game code here

    SDL_Quit();
    return 0;
}
```

## Automation Workflow

The repository uses GitHub Actions to automatically:

1. **Monitor** the upstream SDL_GameControllerDB repository daily
2. **Merge** custom controller mappings from `add_gamecontrollerdb.txt` into the upstream database
3. **Filter** to Linux only, field-anchored on the `platform:` token (keeps Linux + platform-less custom rows)
4. **Split** the SDL2-HIDAPI lane (driver-sig `h`, d-pad as buttons) into `gamecontrollerdb-SDL2.txt`; joydev and SDL3-HIDAPI (d-pad as hat) mappings stay in `gamecontrollerdb.txt`
5. **Deduplicate** each lane by controller GUID (newest wins)
6. **Commit** and push both files automatically

### Workflow Features

- ⏰ **Scheduled execution**: Runs daily at midnight UTC
- 🔧 **Manual trigger**: Can be triggered manually via GitHub Actions
- 📝 **Automated commits**: Updates are committed with timestamps
- 🧹 **Cleanup**: Temporary files are automatically removed

## Contributing

### Adding Custom Controllers

To add support for a new controller:

1. Fork this repository
2. Add your controller mapping to `add_gamecontrollerdb.txt`
3. Follow the SDL mapping format:
   ```
   GUID,Controller Name,button mappings,platform:Linux,
   ```
4. Submit a pull request

### Mapping Format

Each controller mapping follows this structure:
```
GUID,Name,a:button,b:button,x:button,y:button,...,platform:Linux,
```

**Example:**
```
030000005e0400008e02000021010000,Microsoft X-Box 360 pad,a:b0,b:b1,x:b2,y:b3,back:b6,start:b7,guide:b8,leftshoulder:b4,rightshoulder:b5,leftstick:b9,rightstick:b10,leftx:a0,lefty:a1,rightx:a3,righty:a4,lefttrigger:a2,righttrigger:a5,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,platform:Linux,
```

## Compatibility

This database is compatible with:

- SDL2 (2.0.0+) and SDL3 — load `gamecontrollerdb-SDL2.txt` in addition only under SDL2
- Games using SDL2/SDL3 for input handling
- Emulators (RetroArch, MAME, etc.)
- Game engines with SDL integration

## License

This project follows the same licensing as the original SDL_GameControllerDB project. Controller mappings are community-contributed and freely available for use in both commercial and non-commercial projects.

## Support

- 🐛 **Issues**: Report problems via GitHub Issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📖 **Documentation**: Check SDL2 documentation for mapping details

## Related Projects

- [SDL_GameControllerDB](https://github.com/mdqinc/SDL_GameControllerDB) - Original database
- [SDL2](https://www.libsdl.org/) - Simple DirectMedia Layer

---
