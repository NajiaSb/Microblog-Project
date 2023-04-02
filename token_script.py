import random
from app.models import User
from app import db, create_app

app = create_app()
with app.app_context():
    def generate_unique_token(existing_tokens):
        token = random.randint(100000, 999999)
        while token in existing_tokens:
            token = random.randint(100000, 999999)
        return token

    users = User.query.all()
    existing_tokens = {user.token for user in users if user.token is not None}

    for user in users:
        user.token = generate_unique_token(existing_tokens)
        existing_tokens.add(user.token)

    db.session.commit()

