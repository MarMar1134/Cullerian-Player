# Cullerian Player

A custom music player application that plays daily tracks with associated phrases. Built with Python and CustomTkinter for a modern and clean user interface.

## Features

- Daily track playback system
- Modern and clean user interface
- Track information display (name, author, associated phrase)
- Basic playback controls (play/pause, stop)
- Ability to add new tracks to the collection

## Project Structure

```
├── assets/
│   ├── audio/         # Music tracks organized by months
│   ├── data/          # Configuration files
│   └── phrases/       # Daily phrases organized by months
├── src/
│   ├── core/          # Core functionality
│   ├── data/          # Data management
│   ├── log/           # Logging configuration
│   └── ui/            # User interface components
├── logs/              # Application logs
└── requirements.txt   # Project dependencies
```

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Dependencies

The following Python packages are required:

```
pygame==2.6.1        # For audio playback
customtkinter==5.2.2 # For the modern UI
eyed3==0.9.8        # For audio file metadata
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MarMar1134/Cullerian-Player.git
```

2. Navigate to the project directory:
```bash
cd Cullerian-Player
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run the application:

```bash
python src/main.py
```

### Features:
- **Track selection based on a day/month system**: The user can set the track to be played on a specific date, associating him with a custom phrase.
   - If the day isn't specified by the user, the track will be played randomly across the month to which it belongs.
- **Dinamic management of the track data**: The user only needs to specify a month (needed), a day and a phrase (these are optional fields), alongside with the track.mp3 file to set up the app.
   - The program itself doesn't provide any track natively, is responsability of the user to get the .mp3 files and upload them to the program.
- **Random reproduction if isn't a special day**: If the current day doesn't have an associated track, a random one will be selected from the `tracks.json` file, based on the current month.
   - If there aren't tracks available for the current month, the program will sugest the user to add one.

## File Organization

- Music tracks are organized in the `assets/audio/` directory by months
- Associated phrases are stored in `assets/phrases/` directory
- Track metadata and configuration is managed through `assets/data/tracks.json`
- Application logs are stored in `logs/cullerian_player.log`

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **MarMar1134**

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Uses [Pygame](https://www.pygame.org/) for audio playback
- Uses [eyeD3](https://eyed3.readthedocs.io/) for audio file metadata handling