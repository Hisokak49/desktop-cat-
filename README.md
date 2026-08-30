# 🐱 Desktop Cat

A pixel-art desktop companion built with **Python** and **Tkinter**. Desktop Cat reacts to your activity and provides small productivity and interaction features while staying lightweight.

## ✨ Features

- 🐾 Animated pixel-art virtual pet
- 🖱️ Real-time mouse tracking and interaction
- ⌨️ Keyboard activity tracking
- 🧠 State-based cat behavior (`idle`, `follow`, `watch`, `thinking`, `typing`, `pomodoro`, `break`, `play`, `zoomies`, `sleep`, `stretch`)
- 🍅 Pomodoro/productivity support
- ⏰ Reminders
- 🔊 Speech interactions
- 🧸 Interactive toys
- 🎨 Sprite loading and animation system
- 🧪 Automated tests for core state definitions
- ⚙️ GitHub Actions CI for Python syntax and tests

## 🏗️ Project Structure

```text
.
├── animations.py       # Animation handling
├── cat_engine.py       # Main virtual-pet behavior and engine
├── cat_states.py       # Cat state definitions
├── config.py            # Application configuration
├── keyboard_tracker.py  # Keyboard activity tracking
├── main.py              # Application entry point
├── mouse_tracker.py     # Mouse activity tracking
├── reminders.py         # Reminder functionality
├── speech.py            # Speech interactions
├── sprite_loader.py     # Sprite loading utilities
├── toys.py              # Toy/interaction system
└── tests/               # Automated tests
```

## 🚀 Getting Started

### Requirements

- Python 3.10+ recommended
- Tkinter (usually included with standard Python installations; Linux users may need their distribution's Tk package)

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Hisokak49/desktop-cat-.git
cd desktop-cat-
```

Run the application:

```bash
python main.py
```

## 🧪 Running Tests

The project includes tests for the cat state model and a GitHub Actions workflow that validates Python files and runs the test suite.

Install the test dependency if needed:

```bash
python -m pip install pytest
```

Run tests locally:

```bash
python -m pytest
```

## 🛠️ Development

Keep changes focused and avoid coupling UI behavior directly to the state model. New cat states should be added to `cat_states.py` with stable, lowercase string values and accompanied by tests when behavior changes.

Before opening a pull request, run:

```bash
python -m pytest
```

## 🤝 Contributing

Bug fixes, behavior improvements, animation ideas, tests, and documentation improvements are welcome. For contribution guidelines, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## 📌 Project Status

Desktop Cat is an evolving personal desktop-assistant/virtual-pet project. The codebase is intentionally modular so new behaviors, interactions, and productivity features can be added incrementally.

## 👨‍💻 Author

**Amit Yadav** — [GitHub](https://github.com/Hisokak49)
