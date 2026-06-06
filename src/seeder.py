import asyncio
from src.database import async_session_maker
from src.models import Film
from faker import Faker


fake = Faker(["en_US"])

async def seed_films(session, count = 300):
    print("Seeding films...")

    films = []
    for _ in range(count):
        film = Film(
            title=fake.sentence(nb_words=4),
            description=fake.sentence(nb_words=10),
            release_date=fake.date_object(),
            rating=fake.random_int(min=0, max=10),
            genre=fake.random_element(["Action", "Comedy", "Drama", "Sci-Fi", "Thriller"])
        )

        films.append(film)

    session.add_all(films)


async def main():
    async with async_session_maker() as session:
        async with session.begin():

            await seed_films(session)

if __name__ == "__main__":
    asyncio.run(main())
