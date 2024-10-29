from .. import create_app, db

from app.user.models import User

app = create_app()

with app.app_context():
    user = User(
        id=6,
        login="vir",
        blocked=False,
        role="manager",
        fullname="Валиев Ильшат Рашатович",
        email="vir@lkmb-rt.ru",
        url_photo="",
        worknumber="8-000-000-00",
        mobilenumber="8-927-245-86-15",
        telegram="8-927-245-86-15",
    )
    user.set_password("vir123123")
    db.session.add(user)
    db.session.commit()
