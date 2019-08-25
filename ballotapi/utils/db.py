import re

# PostgreSQL connection uri (https://www.postgresql.org/docs/11/libpq-connect.html#id-1.7.3.8.3.6)
# (i.e. postgresql://[user[:password]@][netloc][:port][,...][/dbname][?param1=value1&...])
DB_URI_REGEX = re.compile(
    "^postgresql://"
    "(?P<user>[^:]+):(?P<password>[^@]+)"
    "@(?P<host>[^:]+):(?P<port>[0-9]+)"
    "/(?P<dbname>.+)$"
)

class DatabaseConfigurationError(ValueError):
    """ Exception for known database-related errors """
    pass

