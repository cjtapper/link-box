import requests
from flask import Blueprint, render_template, request, url_for

from . import database as db
from .database import Article
from .save import extract_article

bp = Blueprint("articles", __name__, url_prefix="/articles")

Article.url_for = lambda article: url_for(
    "articles.show_article", article_id=article.id
)


@bp.route("/save", methods=("GET", "POST"))
def save():
    if request.method == "POST":
        url = request.form.get("url")

        res = requests.get(url, headers={"user-agent": "Link Box/0.1.0"})

        article = extract_article(res.text, url)

        db_article = Article(
            title=article.title, source_url=article.url, html=article.content
        )
        db.session.add(db_article)
        db.session.commit()

    return render_template("articles/save.html.jinja2")


@bp.route("/", methods=("GET",))
def index():
    return render_template("articles/index.html.jinja2", articles=Article.query.all())


@bp.route("/<int:article_id>", methods=("GET",))
def show_article(article_id):
    return render_template(
        "articles/article.html.jinja2", article=Article.query.get(article_id)
    )
