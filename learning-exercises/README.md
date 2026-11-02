# Exercises: TODOs are separate from working source

The application in `frontend/` and `backend/` is the reference implementation. Work in your own `exercise/` branch; compare each finished exercise with `docs/answer-key.md`.

1. **JSON data** — add one fictional catalogue entry with a unique ID, nonnegative price in sen, category and availability. Write an API test.
2. **Django** — add `GET /api/products/<id>/` and return 404 when unknown. Cover it with two tests.
3. **Vue** — implement an "Available only" filter and add an accessible toggle.
4. **Cart** — add a "Clear basket" control, preserving the current persistence behavior.
5. **Playwright** — write a test that checks clearing the basket and reloads the page; capture evidence of failure.
6. **CI** — add a second browser project (Firefox) and explain what increases run time.
7. **Jenkins** — create a second stage to publish a test report and identify the failure output.
8. **Poetry** — generate a lockfile, inspect `poetry show --tree`, then commit the lockfile.
9. **Environments** — document how secrets are configured in GitHub Actions and Jenkins without putting them in Git.
10. **Safety review** — explain why client-supplied totals must never be trusted and why a WhatsApp link is not an order confirmation.

Acceptance: existing checks remain green and new tests cover expected + failure cases. Do not remove validations just to make tests pass.
