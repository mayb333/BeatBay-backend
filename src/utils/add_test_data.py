import asyncio
import random
from datetime import datetime, timedelta

from src.auth.models import Role, User
from src.beats.models import Beat, PurchaseOption
from src.database import async_session_maker
from src.users.models import BeatPlay, Cart, Like


async def add_test_data():
    async with async_session_maker() as session:
        async with session.begin():
            # Создание ролей
            role_producer = Role(
                name="Producer", permissions={"create": True, "update": True}
            )
            role_listener = Role(name="Listener", permissions={"listen": True})
            session.add_all([role_producer, role_listener])
            await session.commit()  # Добавляем роли сразу, чтобы их ID были доступны для связанных пользователей

        async with session.begin():
            # Создание пользователей
            users = [
                User(
                    email=f"user{i}@example.com",
                    username=f"user{i}",
                    profile_photo=f"profile{i}.png",
                    registered_at=datetime.utcnow(),
                    role_id=random.choice(
                        [role_producer.role_id, role_listener.role_id]
                    ),
                    total_likes=random.randint(0, 100),
                    total_plays=random.randint(0, 1000),
                    hashed_password="lol",
                    is_active=True,
                    is_superuser=False,
                    is_verified=bool(random.getrandbits(1)),
                )
                for i in range(5)
            ]
            session.add_all(users)
            await session.commit()

        async with session.begin():
            # Создание треков
            beats = []
            for i in range(50):
                new_beat = Beat(
                    user_id=random.choice(users).id,
                    title=f"Beat Title {i}",
                    price=random.randint(1_000, 30_000),
                    bpm=random.randint(60, 180),
                    mood=random.choice(["happy", "sad", "energetic"]),
                    genre=random.choice(["hip-hop", "rock"]),
                    tags=",".join(random.sample(["chill", "happy", "sad"], 2)),
                    image=f"image{i}.png",
                    mp3_file=f"mp3_file_{i}.mp3",
                    wav_file=f"wav_file_{i}.wav",
                    stems_file=f"stems_file_{i}.zip",
                    added_at=datetime.utcnow(),
                    likes_count=random.randint(0, 100),
                    plays_count=random.randint(0, 1000),
                )
                beats.append(new_beat)

            session.add_all(beats)
            await session.commit()

        async with session.begin():
            purchase_options = []
            for i in range(50):
                # Для каждого трека создаем случайное количество опций покупки
                for _ in range(random.randint(1, 3)):
                    purchase_options.append(
                        PurchaseOption(
                            beat_id=beats[i].beat_id,
                            name=f"Option {_}",
                            price=random.randint(100, 1000),
                            formats=random.choice(["mp3", "mp3,wav", "mp3,wav,stems"]),
                        )
                    )
            session.add_all(purchase_options)
            await session.commit()

        async with session.begin():
            # Добавление элементов в корзины, лайков и воспроизведений
            cart_items = []
            like_items = []
            beat_plays = []
            for i in range(40):
                cart_items.append(
                    Cart(
                        user_id=random.choice(users).id,
                        beat_id=random.choice(beats).beat_id,
                        added_at=datetime.utcnow()
                        + timedelta(minutes=random.randint(5, 150)),
                    )
                )
                like_items.append(
                    Like(
                        user_id=random.choice(users).id,
                        beat_id=random.choice(beats).beat_id,
                        added_at=datetime.utcnow()
                        + timedelta(minutes=random.randint(5, 150)),
                    )
                )
                beat_plays.append(
                    BeatPlay(
                        user_id=random.choice(users).id,
                        beat_id=random.choice(beats).beat_id,
                        played_at=datetime.utcnow()
                        + timedelta(minutes=random.randint(5, 150)),
                    )
                )
            session.add_all(cart_items)
            session.add_all(like_items)
            session.add_all(beat_plays)

            # Подтверждение всех изменений
            await session.commit()


if __name__ == "__main__":
    asyncio.run(add_test_data())
