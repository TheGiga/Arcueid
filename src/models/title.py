import discord
from pydantic import BaseModel, validator
from pydantic.schema import Optional


class Title(BaseModel):
    id: int
    code: str
    names: dict
    status: dict
    announce: Optional[str]
    posters: dict
    type: dict  # {full_string, code, string, series, length}
    genres: list
    player: dict
    description: Optional[str]

    class Config:
        validate_assignment = True

    @validator('announce', 'description')
    def float_validator(cls, v):
        if v is None:
            return ""
        return v

    def form_embed(self) -> discord.Embed:
        embed = discord.Embed(colour=discord.Colour.red(), timestamp=discord.utils.utcnow())

        genres = ""
        for x in self.genres:
            genres += f'`{x}` '

        title_desc = self.description
        description = (title_desc[:200] + '..') if len(title_desc) > 200 else title_desc

        embed.description = f"""
                        {description}

                        **Жанры: {genres}**
                        {f'⚠ **{self.announce}**' if len(self.announce) >= 1 else ''}
                        """

        embed.title = f'{self.names.get("ru")}'

        embed.add_field(
            name='🧾 Серия',
            value=f"{self.player['series'].get('last')}/{self.type.get('series')} "
                  f"`({self.type.get('length')} мин.)`"
        )
        embed.add_field(name='ℹ️ Статус', value=str(self.status.get('string')))

        embed.set_image(url=f'https://anilibria.tv/{self.posters["original"].get("url")}')

        return embed
