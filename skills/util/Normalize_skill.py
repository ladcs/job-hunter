import re
import unicodedata


class Normalize_skill:

    ALIASES = {
        "reactjs": "react",
        "react.js": "react",
        "nodejs": "node",
        "node.js": "node",
        "restful api": "rest api",
        "rest apis": "rest api",
        "apis": "api",
        "dotnet": ".net",
        "dotnet core": ".net core",
        "c sharp": "c#",
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        skill = skill.strip().lower()

        skill = unicodedata.normalize("NFKD", skill)\
            .encode("ascii", "ignore")\
            .decode("ascii")

        skill = re.sub(r"\s+", " ", skill)

        return cls.ALIASES.get(skill, skill)