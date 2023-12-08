from selenium import webdriver
from scraper import Profiles
import duckdb
import os
import time

conn = duckdb.connect(database=':memory:', read_only=False)

if os.path.exists('mydb.db'):
    result = conn.execute("SELECT * FROM my_table").fetchdf()
    
else:
    driver = webdriver.Edge()
    url = "https://ocimpact.app.swapcard.com/widget/event/oc2023/people/RXZlbnRWaWV3XzQ1NTQwOA==?showActions=true"
    time.sleep(3)
    profiles = Profiles()
    driverr, links = profiles.get_profiles(url, driver)
    output = profiles.json_output(driver, links[:5])
    
    schema_definition = ', '.join([f'"{col}" VARCHAR(30)' for col in output.columns])
    conn.execute(f"CREATE TABLE my_table ({schema_definition})")

    conn.register('my_table', output)
    result = conn.execute("SELECT * FROM my_table").fetchdf()

print(result)