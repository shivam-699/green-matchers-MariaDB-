import mariadb
try:
    # Connect without specifying database
    conn = mariadb.connect(user="root", password="pass", host="localhost", port=3306)
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS green_jobs")
    cursor.execute("USE green_jobs")

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            role ENUM('job_seeker', 'employer') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            company VARCHAR(100) NOT NULL,
            location VARCHAR(100),
            salary DECIMAL(10, 2),
            posted_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (posted_by) REFERENCES users(user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            favorite_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            job_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (job_id) REFERENCES jobs(job_id),
            UNIQUE (user_id, job_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_demand (
            demand_id INT AUTO_INCREMENT PRIMARY KEY,
            job_title VARCHAR(100) NOT NULL,
            location VARCHAR(100),
            demand_score INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Verify tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("✅ Connected to green_jobs! Tables:", [table[0] for table in tables])

    cursor.close()
    conn.commit()
    conn.close()
except mariadb.Error as e:
    print(f"❌ Error: {e}")