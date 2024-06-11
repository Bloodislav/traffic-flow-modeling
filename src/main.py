from data.dto import ImgPath, FrontRuntime, BackRuntime, Runtime
from frontend.front import init_game_screen
from backend.init_objects import init_objects
from controllers.controller import game_loop


def main() -> None:
    """Основная функция игры."""
    width: int = 500
    height: int = 1200

    back_runtime: BackRuntime = init_objects()
    imgs_path: ImgPath = ImgPath(
        "data/imgs/red-car.png", "data/imgs/road.png", "data/imgs/white-car.png"
    )
    front_runtime: FrontRuntime = init_game_screen(
        back_runtime, imgs_path, width, height
    )
    runtime: Runtime = Runtime(front_runtime, back_runtime)

    game_loop(runtime)


if __name__ == "__main__":
    main()
