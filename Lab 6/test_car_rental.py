import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

# Example test case:
def test_single_economy_rental():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100]
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!
def test_invalid_arguments():
    with pytest.raises(ValueError):
        process_rental_fleet("not_a_list", 10.0)

    with pytest.raises(ValueError):
        process_rental_fleet([], -5.0)


def test_unconfirmed_rental():
    result = process_rental_fleet(
        [{"is_confirmed": False}], 10.0
    )
    assert result["status"] == "EMPTY_BATCH"


def test_invalid_rental_days():
    result = process_rental_fleet(
        [{"is_confirmed": True, "days": 0}], 10.0
    )
    assert result["status"] == "EMPTY_BATCH"


def test_luxury_rental():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 30,
        "days": 2,
        "trip_segments": []
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 250.0


def test_suv_rental():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "suv",
        "driver_age": 30,
        "days": 2,
        "trip_segments": []
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 150.0


def test_unknown_vehicle_type():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "other",
        "driver_age": 30,
        "days": 1,
        "trip_segments": []
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0


def test_young_luxury_driver():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 22,
        "days": 2,
        "trip_segments": []
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 350.0


def test_young_non_luxury_driver():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "economy",
        "driver_age": 22,
        "days": 2,
        "trip_segments": []
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 130.0


def test_negative_trip_miles():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-10]
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["status"] == "STANDARD"


def test_long_trip_miles():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 25,
        "days": 1,
        "trip_segments": [350]
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 190.0


def test_young_driver_long_trip():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 20,
        "days": 1,
        "trip_segments": [350]
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 320.0


def test_high_risk_audit():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-1, -2, -3, -4, -5]
    }]
    result = process_rental_fleet(rentals, 10.0)
    assert result["status"] == "HIGH_RISK_AUDIT"


def test_empty_batch():
    result = process_rental_fleet([], 10.0)
    assert result == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH"
    }


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_safe():
    assert check_fleet_telematics([[60, 80, 100]]) == "SAFE"


def test_telematics_speeding_reset():
    assert check_fleet_telematics([[110, 90, 110]]) == "SAFE"


def test_telematics_ground_vehicle():
    assert check_fleet_telematics([[110, 120]]) == "GROUND_VEHICLE"


def test_telematics_multiple_vehicles():
    assert check_fleet_telematics([[110], [120, 130]]) == "GROUND_VEHICLE"

