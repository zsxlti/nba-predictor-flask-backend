from marshmallow import Schema, fields

class PlainPlayerSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    country = fields.Str(required=True)
    jersey = fields.Int()
    position = fields.Str()
    from_year = fields.Int()
    to_year = fields.Int()

class PlainTeamSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    abbreviation = fields.Str(required=True)
    year_founded = fields.Int(required=True)
    has_previous_name = fields.Bool()

class PlayerSchema(PlainPlayerSchema):
    team_id = fields.Int(required=True, load_only=True)
    team = fields.Nested(PlainTeamSchema(), dump_only=True)

class PlayerUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    country = fields.Str()
    jersey = fields.Int()
    position = fields.Str()
    from_year = fields.Int()
    to_year = fields.Int()

class TeamSchema(PlainTeamSchema):
    players = fields.List(fields.Nested(PlainPlayerSchema()), dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    team_id_home = fields.Int()
    season_id = fields.Int(required=True)
    date = fields.Date()
    fgm_home = fields.Decimal()
    fga_home = fields.Decimal()
    fg_pct_home = fields.Decimal()
    fg3m_home = fields.Decimal()
    fg3a_home = fields.Decimal()
    fg3_pct_home = fields.Decimal()
    ftm_home = fields.Decimal()
    fta_home = fields.Decimal()
    ft_pct_home = fields.Decimal()
    oreb_home = fields.Decimal()
    dreb_home = fields.Decimal()
    reb_home = fields.Decimal()
    ast_home = fields.Decimal()
    stl_home = fields.Decimal()
    blk_home = fields.Decimal()
    tov_home = fields.Decimal()
    pf_home = fields.Decimal()
    pts_home = fields.Decimal()
    team_id_away = fields.Int()
    fgm_away = fields.Decimal()
    fga_away = fields.Decimal()
    fg_pct_away = fields.Decimal()
    fg3m_away = fields.Decimal()
    fg3a_away = fields.Decimal()
    fg3_pct_away = fields.Decimal()
    ftm_away = fields.Decimal()
    fta_away = fields.Decimal()
    ft_pct_away = fields.Decimal()
    oreb_away = fields.Decimal()
    dreb_away = fields.Decimal()
    reb_away = fields.Decimal()
    ast_away = fields.Decimal()
    stl_away = fields.Decimal()
    blk_away = fields.Decimal()
    tov_away = fields.Decimal()
    pf_away = fields.Decimal()
    pts_away = fields.Decimal()
    home_win = fields.Bool()

class SeasonSchema(Schema):
    id = fields.Int(dump_only=True)
    season_number = fields.Int()