"""Function to generate tokens"""
import jwt

class TokenGenerator:
  """Class to handle token generator functions"""

  @classmethod
  def generate_jwt_token(cls, payload, headers, secret) -> str:
    """Generates a JWT token with provided payload, headers and secret"""
    jwt_token = jwt.encode(payload, secret, headers=headers)
    return jwt_token
