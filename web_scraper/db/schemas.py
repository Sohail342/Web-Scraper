from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from pydantic import constr, field_validator
from typing import Annotated


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20, example="username32", pattern="^[a-zA-Z0-9_]+$")]
    password: Annotated[str, Field(min_length=8, max_length=20, example="password123")]
    email: Annotated[EmailStr, Field(example="user@example.com")]
    
class UserLogin(BaseModel):
    username_or_email: Annotated[str, Field(example="Username or email")] 
    password: Annotated[str, Field(example="Password")]
    
    @classmethod
    def validate_one(cls, values):
        if not any([values.get("username"), values.get("email")]):
            raise ValueError("Either username or email must be provided")
        return values
    

class ScrapTags(BaseModel):
    url: Annotated[str, Field(examples="https://example.com/")]
    target_tag: Annotated[
        str, 
        constr(strip_whitespace=True, to_lower=True, min_length=1, max_length=50)
    ] 
    
    target_attribute: Annotated[
        str, 
        constr(strip_whitespace=True, to_lower=True, min_length=1, max_length=50)
    ]

    # Validate `target_tag` to allow only valid HTML tags
    @field_validator("target_tag")
    @classmethod
    def check_valid_tag(cls, value):
        valid_tags = {
            "a", "div", "span", "p", "img", "input", "button", "meta", "script", "link", "table",
            "tr", "td", "th", "ul", "li", "ol", "form", "label", "option", "select"
        }
        if value not in valid_tags:
            raise ValueError(f"Invalid tag '{value}'. Must be a valid HTML tag.")
        return value

    # Validate `target_attribute` to allow only valid HTML attributes
    @field_validator("target_attribute")
    @classmethod
    def check_valid_attribute(cls, value):
        valid_attributes = {
            "href", "src", "alt", "title", "class", "id", "name", "type", "value",
            "placeholder", "style", "data-*", "role", "aria-*", "rel", "target"
        }
        if value not in valid_attributes and not value.startswith("data-") and not value.startswith("aria-"):
            raise ValueError(f"Invalid attribute '{value}'. Must be a valid HTML attribute.")
        return value
    

class ScrapedData(BaseModel):
    job_id: int
    url: str
    status: str
    completed_at: str
    results: str
        
    
class UpdateUser(BaseModel):
    email: Annotated[EmailStr, Field(example="user@example.com")]

class MFAVerify(BaseModel):
    username_or_email: Annotated[str, Field(example="Username or email")]
    otp_code: str
    
class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    