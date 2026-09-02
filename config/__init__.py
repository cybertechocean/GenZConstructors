# PyMySQL fallback support for cPanel MySQL database hosting
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
