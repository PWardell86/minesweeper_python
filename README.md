# Minesweeper

A minesweeper clone made using Pygame.

## Running the game

### Get Python

You need something around [Python 3.10](https://www.python.org/downloads/release/python-3109/#:~:text=Full%20Changelog-,Files,-Version). You can probably get away with 3.9, and 3.11 but the most recent versions do not work.

### Running the Game

Before you can play, you must run the `Dependencies.ps1` file to download all the libraries (2) that this needs.

Then you should be able to run `Minesweeper.ps1` and you will be able to play.

### Playing the Game

It is minesweeper, just click anywhere to get started.

#### Changing Game Settings

1. Click the top left button, by default it is R2-D2
2. Fill in the fields. Both "Game Size" and "Window Size" must be two comma separated values.
3. Difficulty can be changed with the slider. It is the fraction of tiles that will be bombs. So anything above 0.2 or 0.3 is very hard, most of the time impossible (without guessing).

#### Options

`--dev`: Enables debug logging as well as some other dev features  
`--bot=?`: ? Is the level of bot you want to play with (1 -> 3)

### Bots

TODO

### Themes

You can add your own themes to the `src/themes` folder if you would like.

| Image           | File name               |
| --------------- | ----------------------- |
| "one" tile      | _one.png_               |
| "two" tile      | _two.png_               |
| ...             | _..._                   |
| "eight" tile    | _eight.png_             |
| Unrevealed tile | _blank.png_             |
| Bomb            | _bomb.png_              |
| Button (rest)   | _button-rest.png_       |
| Button (press)  | _button-press.png_      |
| New game icon   | _new-game.png_          |
| Game over icon  | _new-game-gameover.png_ |
| Settings icon   | _settings.png_          |
| Top bar         | _topbar.png_            |
