function deleteArticle(ArticleId) {
  fetch("/delete-article", {
    method: "POST",
    body: JSON.stringify({ ArticleId: ArticleId }),
  }).then((_res) => {
    window.location.href = "/admin";
  });
}
