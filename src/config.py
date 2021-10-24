from pydantic import BaseSettings


class Settings(BaseSettings):
    db_connection_string: str = "postgresql://szbbimktemtmxp:abb783d6b84c1f607061d64dacb901af10cae40d24a2b6d96110d7efe477b5c4@ec2-54-174-172-218.compute-1.amazonaws.com:5432/d3vhnlg19iblmb"


settings = Settings()
