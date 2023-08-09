from enum import Enum
from pydantic import BaseModel

# criar classe ENUM para os tipos de TVI
class ServerTVI(str, Enum):
    brasil = 'tvi'
    indonesia = 'tvi-indonesia'