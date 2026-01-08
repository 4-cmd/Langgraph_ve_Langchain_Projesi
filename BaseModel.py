from pydantic import BaseModel,Field
from typing import Optional


class Adding_to_Document_Database(BaseModel):
    "* Dosya ismi ve içeriği buraya girilmelidir"
    file_name : Optional[str] = Field(None,description="Dosya ismi buraya girilmelidir")
    file_content : Optional[str] = Field(None,description="Dosya içeriği buraya girilmelidir")

class Removing_from_Document_Database(BaseModel):
    "* Silinecek dosya ismi buraya girilmelidir"
    name_of_file_that_will_be_removed : Optional[str] = Field(None,description="Silinecek dosya ismi buraya girilmelidir")


