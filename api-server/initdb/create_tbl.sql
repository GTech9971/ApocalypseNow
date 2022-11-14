/** 的の情報 */
DROP TABLE IF EXISTS target_sites;
CREATE TABLE target_sites(
    id INT NOT NULL PRIMARY KEY,
    img_path VARCHAR(256),
    hit_img_path VARCHAR(256),
    created_at DATETIME,
    updated_at DATETIME,
    trim_x INT,
    trim_y INT,
    trim_w INT,
    trim_h INT
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
        ON DELETE CASCADE
);

/** 未検出画像保存用のテーブル */
DROP TABLE IF EXISTS undetect_target_sites;
CREATE TABLE undetect_target_sites(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    img_path VARCHAR(256) NOT NULL,
    created_at DATETIME
);