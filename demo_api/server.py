"""A local, in-memory task API: the system under test, not a requests mock."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class TaskHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Keep pytest output readable.

    def respond(self, status, body=None):
        self.send_response(status)
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if body is not None:
            self.wfile.write(payload)

    def handle_request(self):
        if self.headers.get("Authorization") != "Bearer demo-token":
            self.respond(401, {"error": "Unauthorized"})
            return

        parts = self.path.strip("/").split("/")
        if parts[0] != "tasks" or len(parts) > 2:
            self.respond(404, {"error": "Not found"})
            return
        task_id = None
        if len(parts) == 2:
            try:
                task_id = int(parts[1])
            except ValueError:
                self.respond(400, {"error": "Invalid task ID"})
                return
            if task_id not in self.server.tasks:
                self.respond(404, {"error": "Task not found"})
                return

        if self.command == "GET":
            result = list(self.server.tasks.values()) if task_id is None else self.server.tasks[task_id]
            self.respond(200, result)
            return
        if self.command == "DELETE" and task_id is not None:
            del self.server.tasks[task_id]
            self.respond(204)
            return

        if (self.command == "POST" and task_id is None) or (
            self.command in ("PUT", "PATCH") and task_id is not None
        ):
            if self.headers.get("Content-Type") != "application/json":
                self.respond(415, {"error": "Use application/json"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                data = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeDecodeError):
                self.respond(400, {"error": "Invalid JSON"})
                return
            if not isinstance(data, dict):
                self.respond(400, {"error": "JSON must be an object"})
                return
            title_required = self.command in ("POST", "PUT")
            if (title_required or "title" in data) and (
                not isinstance(data.get("title"), str) or not data["title"].strip()
            ):
                self.respond(400, {"error": "Title must be a non-empty string"})
                return
            if "completed" in data and not isinstance(data["completed"], bool):
                self.respond(400, {"error": "Completed must be a boolean"})
                return
            if not data or set(data) - {"title", "completed"}:
                self.respond(400, {"error": "Invalid fields"})
                return
            if self.command == "POST":
                task_id = self.server.next_id
                self.server.next_id += 1
            if self.command == "PATCH":
                task = dict(self.server.tasks[task_id])
                task.update(data)
            else:
                task = {"id": task_id, "title": data["title"], "completed": data.get("completed", False)}
            self.server.tasks[task_id] = task
            self.respond(201 if self.command == "POST" else 200, task)
            return
        self.respond(405, {"error": "Method not allowed"})

    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request
    do_PATCH = handle_request
    do_DELETE = handle_request


def create_server():
    # Port 0 lets the OS choose a free port; only local connections are accepted.
    server = HTTPServer(("127.0.0.1", 0), TaskHandler)
    server.tasks = {}
    server.next_id = 1
    return server
