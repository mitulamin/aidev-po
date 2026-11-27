# Feedback in a pull request comment

Review a product's Markdown in a pull request in your products repo and comment on the line. Then ask `po`: `/po-feedback --pr <pull request URL>`. It takes in each comment once and never replies on the pull request.

Start the comment with a severity and what's wrong, if you know them:

```
P1 wrong-or-invented: admins never delete bookings, they archive them.
```

```
[P2 unclear-or-untestable] "fast" needs a number.
```

Without a tag, `po` proposes a severity and category and asks you to confirm.

## Severity

- **P0** blocks use: acting on it would cause real harm or a wrong build
- **P1** wrong
- **P2** weak: right, but thin, vague or poorly argued
- **P3** polish

## What's wrong

`wrong-or-invented`, `missing`, `misunderstood-intent`, `wrong-scope-or-priority`, `unclear-or-untestable`, `inconsistent`, `wrong-for-audience`, `process`, `not-sure`.

Comment on the line with the item ID (`REQ-012`, `ACT-003`, `PRS-004`) or the line you mean inside that item. To flag something missing, comment where it should be.
