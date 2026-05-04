import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_API_IDENTIFIER = os.getenv("AUTH0_API_IDENTIFIER")
AUTH0_ALGORITHMS = ["RS256"]

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

PUSHER_APP_ID = os.getenv("PUSHER_APP_ID")
PUSHER_KEY = os.getenv("PUSHER_KEY")
PUSHER_SECRET = os.getenv("PUSHER_SECRET")
PUSHER_CLUSTER = os.getenv("PUSHER_CLUSTER")

TEST_DB_URI = os.getenv("TEST_DB_URI")

UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", os.path.join(BASE_DIR, "uploads"))
MAX_ATTACHMENTS_PER_MESSAGE = int(os.getenv("MAX_ATTACHMENTS_PER_MESSAGE", 5))
MAX_ATTACHMENT_SIZE_BYTES = int(
    os.getenv("MAX_ATTACHMENT_SIZE_BYTES", 10 * 1024 * 1024)
)
MAX_MESSAGE_UPLOAD_SIZE_BYTES = (
    MAX_ATTACHMENTS_PER_MESSAGE * MAX_ATTACHMENT_SIZE_BYTES
) + (1024 * 1024)

ALLOWED_ATTACHMENT_MIME_TYPES = {
    "application/json",
    "application/msword",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "text/csv",
    "text/markdown",
    "text/plain",
}

ALLOWED_ATTACHMENT_EXTENSIONS = {
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".jpeg",
    ".jpg",
    ".json",
    ".md",
    ".pdf",
    ".png",
    ".txt",
    ".webp",
}
