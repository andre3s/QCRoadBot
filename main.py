from extractor.road_status_extractor import road_status
from extractor.weather_forecast import weather_forecast


def main():
    """Execute main functions of this project."""
    weather_forecast()
    road_status()


if __name__ == "__main__":
    main()
