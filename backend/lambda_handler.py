"""Lambda handler for AWS deployment."""
from mangum import Mangum
from app.main import app

handler = Mangum(app)
