import pandas as pd
from typing import Tuple, Union

from debr.randomuser.api import RandomUser
from debr.constructors.types import Users, Timezones, Media, AltIDs, Logins, Countries


def random_user_data_to_csv(df: pd.DataFrame, data_class) -> None:
    output_df = pd.DataFrame(
        list(df.apply(lambda row: data_class.from_dict(row.to_dict()), axis=1))
    )


    output_df.to_csv(f"../../data/{data_class.__name__.lower()}.csv", index=False)


def generate_country_table(df: pd.DataFrame) -> pd.DataFrame:
    only_country_features = df.loc[:, ["nat", "location_country"]]

    grouped_countries = only_country_features.groupby(
        ["nat"]).agg(
        ["unique"]
    ).reset_index()

    grouped_countries.columns = grouped_countries.columns.get_level_values(0)
    grouped_countries["location_country"] = grouped_countries["location_country"].map(lambda a: a[0])

    return grouped_countries


# Note: Ideally, these codes would be generated by the database as a serialized value. This function is *not* guaranteed
# to produce idempotent results, but just mimics the process of creating a timezone_code
def generate_timezone_codes(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    only_tz_features = df.loc[:, ["location_timezone_offset", "location_timezone_description"]]

    # resets index twice to produce artificial timezone code
    grouped_timezones = only_tz_features.groupby(
        ["location_timezone_offset"]).agg(
        ["unique"]).sort_values(
        by="location_timezone_offset", ascending=True).reset_index().reset_index()

    grouped_timezones.columns = grouped_timezones.columns.get_level_values(0)

    grouped_timezones["location_timezone_description"] = [", ".join(
        map(str, location)) for location in grouped_timezones["location_timezone_description"]
    ]

    grouped_timezones = grouped_timezones.rename(
        columns={
            "index": "timezone_code"
        }
    )

    return grouped_timezones, dict(zip(grouped_timezones["location_timezone_offset"], grouped_timezones["timezone_code"]))


def append_timezone_col(df: pd.DataFrame, tz_codes: dict) -> pd.DataFrame:
    df["timezone_code"] = df["location_timezone_offset"].map(lambda a: tz_codes.get(a))
    return df


def main():
    random_user = RandomUser()
    ru_df = random_user.get_data_as_df()

    # generating timezone codes, timezone table output, and appending timezone_code to users table
    tz_table, tz_code_dict = generate_timezone_codes(ru_df)
    random_user_data_to_csv(df=tz_table, data_class=Timezones)
    ru_df = append_timezone_col(df=ru_df, tz_codes=tz_code_dict)

    # generating countries table
    country_table = generate_country_table(ru_df)
    random_user_data_to_csv(df=country_table, data_class=Countries)

    # generating User-level output
    output_file_type_list = [Users, Media, AltIDs, Logins]

    for data_type in output_file_type_list:
        random_user_data_to_csv(ru_df, data_type)


if __name__ == '__main__':
    main()
