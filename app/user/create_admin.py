from .. import create_app, db

from app.user.models import User

app = create_app()

with app.app_context():
    user = User(
        login="admin",
        blocked=False,
        role="admin",
        fullname="Админ Админов Админович",
        email="admin@mail.ru",
        url_photo="",
        worknumber="8-000-000-00",
        mobilenumber="8-000-000-00",
    )
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
