from models.dto import FrontRuntime, BackRuntime, Runtime
from frontend.front import init_game_screen
from backend.back import init_objects
from .controller import game_loop


def main() -> None:
    """Основная функция игры."""
    width: int = 500
    height: int = 1200

    front_runtime: FrontRuntime = init_game_screen(width, height)
    back_runtime: BackRuntime = init_objects(height, width)
    runtime: Runtime = Runtime(front_runtime, back_runtime)

    game_loop(runtime)


if __name__ == "__main__":
    main()
