# Exercise answer key (hints, not an automatic submission)

1. `backend/catalogue/data/product.json` is the source of truth. Add an object with `id, name, category, description, price_sen, available, icon`. Update the expected count.
2. Add a view in `backend/catalogue/views.py` that looks up an ID from `read_products()`. If no match, raise `Http404`; register `path("api/products/<str:product_id>/", ...)`. Assert 200 and 404 in `tests/api/`.
3. Introduce `const availableOnly = ref(false)` in `App.vue`; add `(!availableOnly.value || p.available)` to `filtered`. Add a checkbox with a label.
4. Add a button that sets `cart.value = {}`. The existing watcher persists to localStorage.
5. Add one item, clear, assert total RM 0.00, reload, and assert empty. Use `expect` and `data-testid`.
6. In the Actions job, install Firefox using `poetry run playwright install --with-deps chromium firefox` and pass `--browser chromium --browser firefox` to pytest.
7. Existing `Jenkinsfile` uses `junit` and `archiveArtifacts` in `post { always }`. Split build/test into separate stages for easier troubleshooting.
8. Run `poetry lock`, `poetry show --tree`, then `git add poetry.lock && git commit`. Commit `poetry.lock` for a real project.
9. GitHub: repository Settings > Secrets and variables > Actions. Jenkins: Credentials store and `withCredentials`. Never echo tokens.
10. Server derives prices by ID and quantity from JSON; reject duplicate and unknown IDs. WhatsApp redirection drafts a message only and does not prove it was delivered or accepted.
