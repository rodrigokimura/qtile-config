from typing import NamedTuple


class Command(NamedTuple):
    name: str
    command: str
    description: str

    def as_command_set_dict(self):
        return {self.name: self.command}


commands = [
    Command("code", "code", "Launch VSCode"),
    Command("chrome", "google-chrome", "Launch Chrome"),
    Command(
        "edge",
        'microsoft-edge-stable --proxy-server="http://192.168.0.119:8899;https://192.168.0.119:8899"',
        "Launch Edge using proxy",
    ),
    Command("slack", "flatpak run com.slack.Slack", "Launch Slack"),
    Command("audio", "pavucontrol -t 5", "Launch Audio Settings"),
    Command("spotify", "flatpak run com.spotify.Client", "Launch Spotify"),
]
