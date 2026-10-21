from models import CaregiverAssignment, Device, DevicePairing, Patient, User
from setup_demo_devices import DEMO_DEVICES, setup_demo_data, setup_demo_devices


def test_setup_demo_devices_is_idempotent(db_session):
    first = setup_demo_devices(db_session)
    second = setup_demo_devices(db_session)

    assert second.id == first.id
    assert {device.device_identifier for device in db_session.query(Device).all()} == {
        identifier for identifier, _ in DEMO_DEVICES
    }
    assert db_session.query(DevicePairing).count() == len(DEMO_DEVICES)


def test_setup_demo_data_creates_real_directory_and_caregiver(db_session):
    caregiver, patients = setup_demo_data(db_session)
    again, repeated = setup_demo_data(db_session)

    assert again.id == caregiver.id
    assert len(patients) == len(repeated) == 3
    assert db_session.query(User).filter_by(email="caregiver@caretrack.health").count() == 1
    assert db_session.query(Patient).count() == 3
    assert db_session.query(CaregiverAssignment).count() == 3
