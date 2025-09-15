from app.database import SessionLocal
from app.crud_scripts import (
    add_users, add_posts, get_all_users, get_all_posts_with_users, get_posts_by_username,
    update_user_email, update_post_content, delete_post, delete_user_and_posts
)

if __name__ == "__main__":
    from app.database import engine, Base
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # Добавление
        add_users(db, [
            ("alice", "alice@example.com", "apwd"),
            ("bob", "bob@example.com", "bpwd"),
        ])
        add_posts(db, [
            ("Hello", "First post by Alice", 1),
            ("Tips", "Second post by Alice", 1),
            ("Hi", "Bob's post", 2),
        ])

        # Извлечение
        print("Users:", get_all_users(db))
        print("Posts+Users:", get_all_posts_with_users(db))
        print("Alice posts:", get_posts_by_username(db, "alice"))

        # Обновление
        print("Update email bob ->", update_user_email(db, "bob", "bobby@example.com"))
        print("Update post content id=1 ->", update_post_content(db, 1, "Updated content"))

        # Удаление
        print("Delete post id=2 ->", delete_post(db, 2))
        print("Delete user 'alice' (+posts) ->", delete_user_and_posts(db, "alice"))
