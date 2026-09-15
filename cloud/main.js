// Stack: Node.js 22.x | Parse Server 8.x | File: cloud/main.js
// Validation lives in the backend, so a Python container and a curl command get the same rules.
Parse.Cloud.beforeSave("Task", (request) => {
  const t = request.object;
  const title = t.get("title");
  if (typeof title !== "string" || !title.trim()) throw new Parse.Error(Parse.Error.VALIDATION_ERROR, "title is required.");
  t.set("title", title.trim());
  if (t.get("done") === undefined) t.set("done", false);
});
