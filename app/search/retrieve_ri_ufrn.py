from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from typing_extensions import Annotated
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from datetime import datetime
from urllib.parse import urlencode
import os, time, rispy, json
import cryptography.fernet as fernet

intpk = Annotated[int, mapped_column(primary_key=True)]
str_link_100 = Annotated[str, mapped_column(String(100))]
str_user = Annotated[str, mapped_column(String(60))]
user_fk = Annotated[int, mapped_column(ForeignKey("user_account.id"))]
category_fk = Annotated[int, mapped_column(ForeignKey("category.id"))]
pwdhash = Annotated[str, mapped_column(String(100), unique=True)]

class User(DeclarativeBase, MappedAsDataclass):
    __tablename__ = 'user_account'
    name: Mapped[str_user]
    password_hash: Mapped[pwdhash] = ""

    def generate_password(self, new_password:str):
        code = fernet.Fernet(new_password)
        self.password_hash = str(code.generate_key())

    def set_password(self, new_password:str, old_password:str):
        pass

class Article(DeclarativeBase, MappedAsDataclass):
    __tablename__ = 'article'
    id: Mapped[intpk] = mapped_column(init=True)
    category: Mapped[category_fk]

class Category(DeclarativeBase, MappedAsDataclass):
    __tablename__ = 'category'
    id: Mapped[intpk] = mapped_column(init=False)


# CODE FROM 'SunariaAI' REPO FOR RETRIEVING DATA FROM OPEN ARTICLES
# ALL THE CODE IS AWARE AND RESPECTFUL FOR THE LAW

RI_SEARCH_PATH = "/html/body/ds-app/ds-themed-root/ds-root/div/div/main/div/ds-themed-home-page/ds-home-page/ds-themed-home-news/ds-home-news/div/div/div/ds-themed-search-form/ds-search-form/form/div/div/input"
RI_ARTICLES = "/html/body/ds-app/ds-themed-root/ds-root/div/div/main/div/ds-themed-search-page/ds-search-page/ds-themed-search/ds-search/div/ds-page-with-sidebar/div/div/div/div[2]/div/div[2]/ds-themed-search-results/ds-search-results/div[2]/ds-viewable-collection/ds-themed-object-list/ds-object-list/ds-pagination/div/ul/li[1]/ds-listable-object-component-loader/ds-item-search-result-list-element/div/div[2]/ds-truncatable/div/a"
RI_DONWLOAD_BUTTON = "/html/body/ds-app/ds-themed-root/ds-root/div/div/main/div/ds-themed-item-page/ds-item-page/div/div/div/ds-item-details/div[2]/div[1]/ds-themed-item-page-full-file-section/ds-item-page-full-file-section/ds-metadata-field-wrapper/div/div/div[1]/div/ds-pagination/div/div[2]/div[3]/ds-themed-file-download-link/ds-file-download-link/a"

current_year = datetime.today().year
download_dir = os.path.join(os.path.abspath(os.getcwd()), 'data')
