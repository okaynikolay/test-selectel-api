CREATE_TABLE = """CREATE TABLE IF NOT EXISTS events (
         id SERIAL,	
	 city VARCHAR(80),
         date DATE,
         device VARCHAR(14),
	 "user" cidr);
     """

DROP = """drop table events"""
