from datetime import datetime, timedelta

DELIVERY_DAYS = 2

def _is_holiday(date: datetime) -> bool:
    return date.weekday() >= 5

def get_eta(purchase_date: datetime) -> datetime:
    current_date = purchase_date
    remaining_days = DELIVERY_DAYS

    while remaining_days > 0:
        current_date += timedelta(days=1)
        if not _is_holiday(current_date):
            remaining_days -= 1

    return current_date

def test_get_eta_2025_8_19() -> None:
    result = get_eta(datetime(2025,8,19))
    assert result == datetime(2025,8,21)

def test_get_dta_2025_12_31() -> None:
    result = get_eta(datetime(2025,12,31))
    assert result == datetime(2026,1,2)

def test_get_dta_2025_2_28() -> None:
    result = get_eta(datetime(2025,2,28))
    assert result == datetime(2025,3,4)
