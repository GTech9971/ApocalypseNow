/** 的の情報 */
DROP TABLE IF EXISTS target_sites;
CREATE TABLE target_sites(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    img_path VARCHAR(256),
    created_at DATETIME    
);

/** 的のヒットポイント */
DROP TABLE IF EXISTS target_site_hit_points;
CREATE TABLE target_site_hit_points(
    target_site_id INT NOT NULL,
    x INT NOT NULL,
    y INT NOT NULL,
    hit_point INT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (target_site_id) REFERENCES target_sites(id) 
        ON UPDATE CASCADE
);