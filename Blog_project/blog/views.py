from django.shortcuts import render
from datetime import date

# Create your views here.


all_posts = [
    {
        'slug': 'learning-django',
        'title': 'django course',
        'author': 'hoori dahesh',
        'image': 'django.jpg',
        'date': date(2025, 8, 3),
        'short_descripshion': 'This is django course',
        'content': """Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
        """,
    },
    {
        'slug': 'learning-python',
        'title': 'python course',
        'author': 'hoori dahesh',
        'image': 'python.jpg',
        'date': date(2025, 4, 15),
        'short_descripshion': 'This is python course',
        'content': """Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
        """,
    },
    {
        'slug': 'learning-database',
        'title': 'database course',
        'author': 'hoori dahesh',
        'image': 'database.jpg',
        'date': date(2025, 1, 10),
        'short_descripshion': 'This is database course',
        'content': """Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut autem eos est, ipsa magnam maiores
            necessitatibus neque optio possimus saepe, sunt tempora, veritatis vitae? Aspernatur at atque quam
            voluptatum. Consectetur eaque excepturi inventore ipsam nisi obcaecati, praesentium reprehenderit vitae.
            Eum!
        """,
    },
]


def get_data(post):
    return post['date']


def index(request):
    sorted_poste = sorted(all_posts, key=get_data)
    latest_posts = sorted_poste[-2:]
    return render(request, 'blog/index.html', context={
        'latest_posts': latest_posts,
    })


def post(request):
    return render(request, 'blog/post.html', {'all_post': all_posts})


def single_post(request, slug):
    post = next(post for post in all_posts if
                post['slug'] == slug)  # با این نکست می تونیم توی اون لیست بگردیم و هی اسلاگ بعدی رو ببینیم
    return render(request, 'blog/post_detail.html', {'post': post})
